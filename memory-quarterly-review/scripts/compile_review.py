#!/usr/bin/env python3
"""
Compile a quarterly review outline by aggregating Cogniz memories across goal, metric,
and narrative categories.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402

DEFAULT_CATEGORIES = (
    "okr-updates",
    "metrics-digest",
    "launch-notes",
    "customer-story",
    "risk-log",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile a quarterly review outline from Cogniz memories."
    )
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument("--quarter", required=True, help="Quarter label, e.g. 2025-Q3.")
    parser.add_argument(
        "--categories",
        nargs="+",
        default=list(DEFAULT_CATEGORIES),
        help="Memory categories to include.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Max memories per category.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the compiled outline (Markdown).",
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


def gather_memories(api, quarter: str, categories: List[str], limit: int, logger: logging.Logger) -> Dict[str, List[Dict]]:
    collected: Dict[str, List[Dict]] = {}
    for category in categories:
        query = f"category:{category} quarter:{quarter}"
        logger.info("Fetching category '%s' with query '%s'", category, query)
        collected[category] = api.search(query=query, limit=limit, project_id=api.project_id)
    return collected


def format_outline(quarter: str, memories: Dict[str, List[Dict]]) -> str:
    lines = [
        f"# Quarterly Review Outline: {quarter}",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
    ]

    sections = {
        "okr-updates": "Goals vs Outcomes",
        "metrics-digest": "Key Metrics",
        "launch-notes": "Product and Launch Highlights",
        "customer-story": "Customer Impact",
        "risk-log": "Risks and Mitigations",
    }

    for category, title in sections.items():
        entries = memories.get(category, [])
        if not entries:
            continue
        lines.append(f"## {title}")
        for mem in entries:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            lines.append(f"- [{mem.get('id', 'unknown')}] {snippet[:220]}{'...' if len(snippet) > 220 else ''}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("quarterly_review")

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    logger.debug("Loaded base_url=%s project_id=%s", config.get("base_url"), config.get("project_id"))
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )

    memories = gather_memories(api, args.quarter, args.categories, args.limit, logger)
    outline = format_outline(args.quarter, memories)

    print(outline)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(outline, encoding="utf-8")
        logger.info("Saved outline to %s", args.output)


if __name__ == "__main__":  # pragma: no cover
    main()

