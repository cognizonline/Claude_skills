#!/usr/bin/env python3
"""
Log learning session notes and optional review reminders into the Cogniz Memory Platform.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log a learning session and optional reminder.")
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument("--topic", required=True, help="Learning topic or skill.")
    parser.add_argument(
        "--notes-file",
        required=True,
        help="Path to a Markdown or text file with session notes.",
    )
    parser.add_argument(
        "--review-in-days",
        type=int,
        default=7,
        help="Days until the next review reminder.",
    )
    parser.add_argument(
        "--no-reminder",
        action="store_true",
        help="Disable automatic reminder creation.",
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


def build_session_content(topic: str, notes: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    return (
        f"# Learning Session: {topic}\n"
        f"Date: {timestamp}\n\n"
        f"{notes.strip()}\n"
    )


def build_reminder_content(topic: str, due_date: datetime) -> str:
    return (
        f"# Learning Reminder\n"
        f"Topic: {topic}\n"
        f"Review On: {due_date.strftime('%Y-%m-%d')}\n"
        f"Focus: revisit key exercises and unanswered questions.\n"
    )


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("learning_tracker")

    notes_path = Path(args.notes_file)
    if not notes_path.exists():
        raise FileNotFoundError(f"Notes file not found: {notes_path}")

    notes_text = notes_path.read_text(encoding="utf-8")
    session_content = build_session_content(args.topic, notes_text)

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )

    api.store(
        content=f"@learning-session\n{session_content}",
        project_id=config.get("project_id"),
        category="learning",
    )
    logger.info("Stored learning session for topic '%s'.", args.topic)

    if not args.no_reminder:
        review_date = datetime.utcnow() + timedelta(days=args.review_in_days)
        reminder_content = build_reminder_content(args.topic, review_date)
        api.store(
            content=f"@learning-reminder\n{reminder_content}",
            project_id=config.get("project_id"),
            category="learning-reminders",
        )
        logger.info("Created reminder for %s.", review_date.strftime("%Y-%m-%d"))


if __name__ == "__main__":  # pragma: no cover
    main()

