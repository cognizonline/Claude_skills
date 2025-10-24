#!/usr/bin/env python3
"""
Generate an executive-ready account briefing by querying the Cogniz Memory Platform.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402


KEYWORD_BUCKETS: Dict[str, Tuple[str, ...]] = {
    "highlights": (
        "win",
        "launched",
        "delivered",
        "adopted",
        "positive",
        "success",
        "celebrate",
        "complete",
    ),
    "risks": (
        "risk",
        "blocker",
        "concern",
        "issue",
        "churn",
        "delay",
        "escalat",
        "downgrade",
    ),
    "actions": (
        "next step",
        "follow up",
        "todo",
        "action",
        "assign",
        "due",
        "schedule",
    ),
    "metrics": (
        "arr",
        "mrr",
        "usage",
        "metric",
        "kpi",
        "adoption",
        "renewal",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an account briefing from Cogniz memories."
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to Cogniz configuration JSON (see config_template in memory manager).",
    )
    parser.add_argument(
        "--account",
        required=True,
        help="Account identifier used in memory tagging (e.g. account:acme-corp).",
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=30,
        help="Number of days to look back when searching memories.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=40,
        help="Maximum number of memories to retrieve for analysis.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the generated briefing (Markdown).",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
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


def build_query(account: str, lookback_days: int) -> str:
    cutoff = (datetime.utcnow() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    return f"{account} date>={cutoff}"


def bucket_memory(content: str) -> str:
    lowered = content.lower()
    for bucket, keywords in KEYWORD_BUCKETS.items():
        if any(term in lowered for term in keywords):
            return bucket
    return "notes"


def summarise(memories: List[Dict]) -> Dict[str, List[Dict]]:
    summary: Dict[str, List[Dict]] = {bucket: [] for bucket in KEYWORD_BUCKETS}
    summary["notes"] = []
    for item in memories:
        content = item.get("content") or ""
        bucket = bucket_memory(content)
        summary.setdefault(bucket, []).append(item)
    return summary


def format_markdown(account: str, grouped: Dict[str, List[Dict]]) -> str:
    lines = [
        f"# Account Briefing: {account}",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
    ]
    order = ("highlights", "risks", "actions", "metrics", "notes")
    for section in order:
        entries = grouped.get(section, [])
        if not entries:
            continue
        title = section.capitalize()
        lines.append(f"## {title}")
        for mem in entries:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            memory_id = mem.get("id", "unknown")
            lines.append(f"- [{memory_id}] {snippet[:220]}{'...' if len(snippet) > 220 else ''}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def format_json(account: str, grouped: Dict[str, List[Dict]]) -> str:
    payload = {
        "account": account,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "sections": {
            section: [
                {
                    "memory_id": mem.get("id"),
                    "category": mem.get("category"),
                    "summary": (mem.get("content") or "").strip(),
                    "created_at": mem.get("created_at"),
                }
                for mem in entries
            ]
            for section, entries in grouped.items()
            if entries
        },
    }
    return json.dumps(payload, indent=2)


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("account_briefing")

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    logger.debug("Loaded config for base_url=%s project_id=%s", config.get("base_url"), config.get("project_id"))
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )

    query = build_query(account=args.account, lookback_days=args.lookback_days)
    logger.info("Searching memories with query '%s' (limit=%s)", query, args.limit)
    memories = api.search(query=query, project_id=config.get("project_id"), limit=args.limit)

    if not memories:
        logger.warning("No memories found for the provided query.")
        return

    grouped = summarise(memories)
    if args.format == "json":
        output = format_json(args.account, grouped)
    else:
        output = format_markdown(args.account, grouped)

    print(output)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        logger.info("Saved briefing to %s", args.output)


if __name__ == "__main__":  # pragma: no cover
    main()

