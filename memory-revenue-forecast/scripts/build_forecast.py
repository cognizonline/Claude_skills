#!/usr/bin/env python3
"""
Build baseline, conservative, and stretch revenue scenarios using Cogniz memories.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Dict, Iterable, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402

AMOUNT_KEY_PATTERN = re.compile(
    r"(arr|mrr|revenue|amount|value|uplift|delta)\s*[:=]\s*\$?\s*([\d,]+(?:\.\d+)?)\s*(k|m|mm|b)?",
    re.IGNORECASE,
)
VALUE_PATTERN = re.compile(r"\$?\s*([\d,]+(?:\.\d+)?)\s*(k|m|mm|b)?", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate multi-scenario revenue forecasts from Cogniz memories."
    )
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument(
        "--baseline-mrr",
        type=float,
        help="Baseline Monthly Recurring Revenue (defaults to value inferred from memories).",
    )
    parser.add_argument(
        "--horizon",
        type=int,
        default=6,
        help="Forecast horizon in months.",
    )
    parser.add_argument(
        "--pipeline-query",
        default="category:sales-notes OR category:renewal-risks",
        help="Search query used to retrieve pipeline notes.",
    )
    parser.add_argument(
        "--metrics-query",
        default="category:revenue-metrics",
        help="Search query used to retrieve baseline revenue metrics.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=80,
        help="Maximum results for each search query.",
    )
    parser.add_argument(
        "--memory-api-path",
        help="Override path to the cogniz-memory-manager scripts directory.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    return parser.parse_args()


def coerce_value(raw: str, suffix: Optional[str]) -> float:
    value = float(raw.replace(",", ""))
    if suffix:
        suffix = suffix.lower()
        if suffix == "k":
            value *= 1_000
        elif suffix in {"m", "mm"}:
            value *= 1_000_000
        elif suffix == "b":
            value *= 1_000_000_000
    return value


def parse_json_amounts(content: str) -> List[float]:
    """Attempt to read JSON objects/dicts for numeric fields."""
    matches: List[float] = []
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return matches

    def collect(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (int, float)) and key.lower() in {"arr", "mrr", "revenue", "amount"}:
                    matches.append(float(value))
                else:
                    collect(value)
        elif isinstance(obj, list):
            for item in obj:
                collect(item)

    collect(data)
    return matches


def extract_amounts(content: str) -> Tuple[List[float], bool]:
    """Return numeric amounts and flag whether detection was heuristic."""
    amounts = parse_json_amounts(content)
    heuristic = False

    if not amounts:
        for match in AMOUNT_KEY_PATTERN.finditer(content):
            heuristic = True
            amounts.append(coerce_value(match.group(2), match.group(3)))

    if not amounts:
        for match in VALUE_PATTERN.finditer(content):
            heuristic = True
            value = coerce_value(match.group(1), match.group(2))
            if value:
                amounts.append(value)

    return amounts, heuristic


def detect_stage(content: str) -> str:
    lowered = content.lower()
    if any(term in lowered for term in ("churn", "downgrade", "attrition", "cancel")):
        return "churn"
    if any(term in lowered for term in ("best case", "stretch", "upside", "whitespace")):
        return "best_case"
    if any(term in lowered for term in ("commit", "signed", "contract", "closed won", "billing start")):
        return "committed"
    if any(term in lowered for term in ("expansion", "upsell", "add-on", "upgrade")):
        return "expansion"
    return "pipeline"


def summarise_amounts(memories: Iterable[Dict], logger: logging.Logger) -> Tuple[float, List[str]]:
    total = 0.0
    warnings = []
    for mem in memories:
        content = (mem.get("content") or "")
        amounts, heuristic = extract_amounts(content)
        if not amounts:
            warnings.append(mem.get("id", "unknown"))
            continue
        total += mean(amounts)
        if heuristic:
            logger.debug("Heuristic amount extraction used for memory %s", mem.get("id"))
    return total, warnings


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("revenue_forecast")

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    logger.debug("Loaded base_url=%s project_id=%s", config.get("base_url"), config.get("project_id"))
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )

    logger.info("Fetching baseline metrics with query '%s'", args.metrics_query)
    baseline_results = api.search(
        query=args.metrics_query,
        project_id=config.get("project_id"),
        limit=args.limit,
    )
    logger.info("Fetching pipeline notes with query '%s'", args.pipeline_query)
    pipeline_results = api.search(
        query=args.pipeline_query,
        project_id=config.get("project_id"),
        limit=args.limit,
    )

    stage_groups: Dict[str, List[Dict]] = defaultdict(list)
    for mem in pipeline_results:
        stage_groups[detect_stage(mem.get("content") or "")].append(mem)

    baseline_mrr = args.baseline_mrr
    baseline_warnings: List[str] = []
    if baseline_mrr is None and baseline_results:
        baseline_mrr, baseline_warnings = summarise_amounts(baseline_results, logger)
        logger.debug("Baseline MRR inferred as %.2f from %d memories", baseline_mrr, len(baseline_results))

    baseline_mrr = baseline_mrr or 0.0
    committed, committed_warnings = summarise_amounts(stage_groups["committed"], logger)
    best_case, best_case_warnings = summarise_amounts(stage_groups["best_case"], logger)
    churn, churn_warnings = summarise_amounts(stage_groups["churn"], logger)
    expansion, expansion_warnings = summarise_amounts(stage_groups["expansion"], logger)

    conservative = baseline_mrr + committed - churn
    standard = baseline_mrr + committed + 0.5 * expansion - churn
    stretch = baseline_mrr + committed + expansion + best_case - churn

    header = (
        f"Baseline MRR: ${baseline_mrr:,.2f}\n"
        f"Committed Uplift: ${committed:,.2f}\n"
        f"Expansion Uplift: ${expansion:,.2f}\n"
        f"Best Case Uplift: ${best_case:,.2f}\n"
        f"Expected Churn: -${churn:,.2f}\n"
    )
    print(header)

    print("Forecast Summary (MRR)")
    print(f"{'Period':<12}{'Conservative':>15}{'Baseline':>15}{'Stretch':>15}")
    for month in range(1, args.horizon + 1):
        label = f"Month {month}"
        cons_val = baseline_mrr + ((conservative - baseline_mrr) / max(args.horizon, 1)) * month
        base_val = baseline_mrr + ((standard - baseline_mrr) / max(args.horizon, 1)) * month
        stretch_val = baseline_mrr + ((stretch - baseline_mrr) / max(args.horizon, 1)) * month
        print(f"{label:<12}{cons_val:>15,.2f}{base_val:>15,.2f}{stretch_val:>15,.2f}")

    print("\nGenerated:", datetime.utcnow().isoformat(timespec="seconds"), "Z")
    print("Review stage breakdown below and cross-check with source memories.\n")

    for stage, memories in stage_groups.items():
        if not memories:
            continue
        print(f"[{stage.upper()}] {len(memories)} items:")
        for mem in memories:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            print(f"- {mem.get('id', 'unknown')}: {snippet[:160]}{'...' if len(snippet) > 160 else ''}")
        print("")

    def warn(label: str, warnings: List[str]) -> None:
        if warnings:
            logger.warning(
                "No numeric amounts detected for %s memories: %s",
                label,
                ", ".join(warnings),
            )

    warn("baseline", baseline_warnings)
    warn("committed", committed_warnings)
    warn("best_case", best_case_warnings)
    warn("churn", churn_warnings)
    warn("expansion", expansion_warnings)


if __name__ == "__main__":  # pragma: no cover
    main()

