#!/usr/bin/env python3
"""
Generate a sales operations snapshot by aggregating Cogniz deal notes and usage analytics.
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a sales ops analytics snapshot."
    )
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument(
        "--quarter",
        help="Quarter label (e.g. 2025-Q4) to filter pipeline notes.",
    )
    parser.add_argument(
        "--segment",
        help="Optional segment filter (e.g. enterprise, smb).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=80,
        help="Max memories per category.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the snapshot (Markdown).",
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


def build_pipeline_query(args: argparse.Namespace) -> str:
    terms = ["category:deal-notes"]
    if args.quarter:
        terms.append(f"quarter:{args.quarter}")
    if args.segment:
        terms.append(f"segment:{args.segment}")
    return " ".join(terms)


def build_usage_query(args: argparse.Namespace) -> str:
    terms = ["category:usage-analytics"]
    if args.segment:
        terms.append(f"segment:{args.segment}")
    return " ".join(terms)


def categorise_pipeline(memories: List[Dict]) -> Dict[str, List[Dict]]:
    groups: Dict[str, List[Dict]] = defaultdict(list)
    for mem in memories:
        content = (mem.get("content") or "").lower()
        if any(term in content for term in ("closed won", "signed", "contract start", "won")):
            groups["closed_won"].append(mem)
        elif any(term in content for term in ("stalled", "blocked", "stuck", "awaiting")):
            groups["stalled"].append(mem)
        elif any(term in content for term in ("expansion", "upsell", "add-on", "upgrade")):
            groups["expansion"].append(mem)
        elif any(term in content for term in ("churn", "downgrade", "cancel", "at risk")):
            groups["churn"].append(mem)
        else:
            groups["active"].append(mem)
    return groups


def format_snapshot(pipeline_groups: Dict[str, List[Dict]], usage_memories: List[Dict], args: argparse.Namespace) -> str:
    lines = [
        "# Sales Ops Snapshot",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
    ]
    if args.quarter:
        lines.append(f"Quarter: {args.quarter}")
    if args.segment:
        lines.append(f"Segment: {args.segment}")
    lines.append("")

    lines.append("## Pipeline Overview")
    for stage in ("active", "stalled", "expansion", "churn", "closed_won"):
        count = len(pipeline_groups.get(stage, []))
        lines.append(f"- {stage.replace('_', ' ').title()}: {count}")

    lines.extend(["", "## Pipeline Details"])
    for stage, memories in pipeline_groups.items():
        if not memories:
            continue
        lines.append(f"### {stage.replace('_', ' ').title()}")
        for mem in memories:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            lines.append(f"- [{mem.get('id', 'unknown')}] {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
        lines.append("")

    lines.append("## Usage Signals")
    if usage_memories:
        for mem in usage_memories:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            lines.append(f"- [{mem.get('id', 'unknown')}] {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
    else:
        lines.append("- No usage analytics memories match the query.")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("sales_ops_snapshot")

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    logger.debug("Loaded base_url=%s project_id=%s", config.get("base_url"), config.get("project_id"))
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )

    pipeline_query = build_pipeline_query(args)
    usage_query = build_usage_query(args)

    logger.info("Querying pipeline memories: '%s'", pipeline_query)
    pipeline_memories = api.search(
        query=pipeline_query,
        limit=args.limit,
        project_id=config.get("project_id"),
    )
    logger.info("Querying usage analytics: '%s'", usage_query)
    usage_memories = api.search(
        query=usage_query,
        limit=args.limit,
        project_id=config.get("project_id"),
    )

    groups = categorise_pipeline(pipeline_memories)
    snapshot = format_snapshot(groups, usage_memories, args)
    print(snapshot)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(snapshot, encoding="utf-8")
        logger.info("Saved snapshot to %s", args.output)


if __name__ == "__main__":  # pragma: no cover
    main()

