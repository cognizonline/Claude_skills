#!/usr/bin/env python3
"""
Log a creative idea into the Cogniz Memory Platform with consistent metadata.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log a new idea to the Cogniz idea vault.")
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument("--title", required=True, help="Short title for the idea.")
    parser.add_argument("--summary", required=True, help="One or two sentence summary.")
    parser.add_argument("--topic", required=True, help="Topic or theme tag.")
    parser.add_argument(
        "--impact",
        default="medium",
        help="Impact level (low, medium, high).",
    )
    parser.add_argument(
        "--effort",
        default="medium",
        help="Effort estimate (low, medium, high).",
    )
    parser.add_argument(
        "--next-step",
        help="Optional immediate next step.",
    )
    parser.add_argument(
        "--reference",
        help="Optional link or memory ID providing inspiration.",
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


def build_content(args: argparse.Namespace) -> str:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    lines = [
        f"# Idea: {args.title}",
        f"Date Captured: {timestamp}",
        f"Topic: {args.topic}",
        f"Impact: {args.impact}",
        f"Effort: {args.effort}",
        "",
        "## Summary",
        args.summary.strip(),
    ]
    if args.reference:
        lines.extend(["", f"## Inspiration\n- {args.reference}"])
    if args.next_step:
        lines.extend(["", "## Next Step", f"- {args.next_step}"])
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("idea_vault")

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )
    content = build_content(args)
    api.store(
        content=f"@idea\n{content}",
        project_id=config.get("project_id"),
        category="idea-vault",
    )
    logger.info("Idea '%s' stored successfully.", args.title)


if __name__ == "__main__":  # pragma: no cover
    main()

