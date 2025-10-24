#!/usr/bin/env python3
"""
Compile a project handoff packet by gathering recent Cogniz memories and
structuring them into state, tasks, and risk sections.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a project handoff summary from Cogniz memories."
    )
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument("--project", required=True, help="Project identifier or tag.")
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=14,
        help="Number of days to include in the summary.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=80,
        help="Max number of memories to retrieve.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the handoff packet (Markdown).",
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


def build_query(project: str, lookback_days: int) -> str:
    cutoff = (datetime.utcnow() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    return f"project:{project} date>={cutoff}"


def format_packet(project: str, memories: List[Dict]) -> str:
    header = [
        f"# Handoff Packet: {project}",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
    ]

    state_lines = ["## Current State", ""]
    tasks_lines = ["## Outstanding Tasks", ""]
    risk_lines = ["## Risks and Blockers", ""]

    for mem in memories:
        content = (mem.get("content") or "").strip().replace("\n", " ")
        memory_id = mem.get("id", "unknown")
        lowered = content.lower()
        if any(word in lowered for word in ("todo", "next step", "follow up", "action", "owner")):
            tasks_lines.append(f"- [{memory_id}] {content[:200]}{'...' if len(content) > 200 else ''}")
        elif any(word in lowered for word in ("risk", "blocker", "issue", "blocked", "dependency")):
            risk_lines.append(f"- [{memory_id}] {content[:200]}{'...' if len(content) > 200 else ''}")
        else:
            state_lines.append(f"- [{memory_id}] {content[:200]}{'...' if len(content) > 200 else ''}")

    sections = header + state_lines + [""] + tasks_lines + [""] + risk_lines
    return "\n".join(sections).strip() + "\n"


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("project_handoff")

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    logger.debug("Loaded base_url=%s project_id=%s", config.get("base_url"), config.get("project_id"))
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )

    query = build_query(args.project, args.lookback_days)
    logger.info("Searching memories with query '%s' (limit=%s)", query, args.limit)
    memories = api.search(query=query, project_id=config.get("project_id"), limit=args.limit)

    if not memories:
        logger.warning("No memories found for the provided project and lookback window.")
        return

    packet = format_packet(args.project, memories)
    print(packet)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(packet, encoding="utf-8")
        logger.info("Saved handoff to %s", args.output)


if __name__ == "__main__":  # pragma: no cover
    main()

