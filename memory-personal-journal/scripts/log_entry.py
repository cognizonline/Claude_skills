#!/usr/bin/env python3
"""
Format and store a personal journal entry in the Cogniz Memory Platform.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log a personal journal entry to Cogniz.")
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument("--content-file", required=True, help="Path to a text file containing the entry.")
    parser.add_argument(
        "--date",
        help="Entry date in YYYY-MM-DD format (defaults to today).",
    )
    parser.add_argument(
        "--store",
        action="store_true",
        help="Store the formatted entry in Cogniz.",
    )
    parser.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="Optional additional tags (for example gratitude, health).",
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


def format_entry(content: str, entry_date: str, tags: List[str]) -> str:
    lines = [
        f"# Journal Entry - {entry_date}",
        f"Tags: {', '.join(tags)}",
        "",
    ]
    if "highlights" not in content.lower():
        lines.append("## Highlights")
        lines.append("- " + content.strip().split("\n")[0])
        lines.append("")
    lines.append(content.strip())
    if "next actions" not in content.lower():
        lines.extend(["", "## Next Actions", "- Reflect tomorrow on progress."])
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("personal_journal")

    content_path = Path(args.content_file)
    if not content_path.exists():
        raise FileNotFoundError(f"Entry file not found: {content_path}")

    entry_date = args.date or datetime.utcnow().strftime("%Y-%m-%d")
    raw_content = content_path.read_text(encoding="utf-8")
    base_tags = ["personal-journal", f"date:{entry_date}"] + args.tags
    formatted = format_entry(raw_content, entry_date, base_tags)

    print(formatted)

    if args.store:
        CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
        logger.debug("Using Cogniz memory manager from %s", manager_path)

        config = load_config(args.config)
        api = CognizMemoryAPI(
            base_url=config["base_url"],
            api_key=config["api_key"],
            project_id=config.get("project_id"),
        )
        api.store(
            content=f"@journal\n{formatted}",
            project_id=config.get("project_id"),
            category="personal-journal",
        )
        logger.info("Stored entry for %s with tags: %s", entry_date, ", ".join(base_tags))


if __name__ == "__main__":  # pragma: no cover
    main()

