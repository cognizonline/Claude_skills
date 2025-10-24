#!/usr/bin/env python3
"""
Generate a customer onboarding plan by combining Cogniz memories containing playbooks,
discovery notes, and progress updates.
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Cogniz-backed onboarding plan."
    )
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument("--account", required=True, help="Account identifier or tag.")
    parser.add_argument(
        "--industry",
        default="general",
        help="Optional industry tag to select the best playbook.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the onboarding plan (Markdown).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=40,
        help="Max memories to fetch per query.",
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


def fetch_playbooks(api, industry: str, limit: int, logger: logging.Logger) -> List[Dict]:
    query = f"category:onboarding-playbook industry:{industry}"
    logger.info("Fetching onboarding playbooks with query '%s'", query)
    results = api.search(query=query, limit=limit, project_id=api.project_id)
    if not results and industry != "general":
        fallback = "category:onboarding-playbook industry:general"
        logger.warning("No playbooks found for industry '%s'. Falling back to '%s'.", industry, fallback)
        results = api.search(query=fallback, limit=limit, project_id=api.project_id)
    return results


def fetch_account_notes(api, account: str, limit: int, logger: logging.Logger) -> Dict[str, List[Dict]]:
    queries = {
        "discovery": f"account:{account} category:discovery-notes",
        "progress": f"account:{account} category:onboarding-progress",
        "blockers": f"account:{account} category:onboarding-blockers",
    }
    results = {}
    for label, query in queries.items():
        logger.info("Fetching %s notes with query '%s'", label, query)
        results[label] = api.search(query=query, limit=limit, project_id=api.project_id)
    return results


def format_plan(account: str, industry: str, playbooks: List[Dict], notes: Dict[str, List[Dict]]) -> str:
    lines = [
        f"# Onboarding Plan: {account}",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        f"Industry Template: {industry}",
        "",
        "## Playbook References",
    ]
    if playbooks:
        for mem in playbooks[:3]:
            snippet = (mem.get("content") or "").strip().split("\n")[0]
            lines.append(f"- [{mem.get('id', 'unknown')}] {snippet}")
    else:
        lines.append("- No playbook memories found. Capture a template before proceeding.")

    lines.extend(["", "## Key Discovery Insights"])
    discovery = notes.get("discovery", [])
    if discovery:
        for mem in discovery:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            lines.append(f"- [{mem.get('id', 'unknown')}] {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
    else:
        lines.append("- No discovery notes stored. Prompt the team to capture objectives and constraints.")

    lines.extend(["", "## Current Progress"])
    progress = notes.get("progress", [])
    if progress:
        for mem in progress:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            lines.append(f"- [{mem.get('id', 'unknown')}] {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
    else:
        lines.append("- No progress updates recorded yet.")

    lines.extend(["", "## Blockers"])
    blockers = notes.get("blockers", [])
    if blockers:
        for mem in blockers:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            lines.append(f"- [{mem.get('id', 'unknown')}] {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
    else:
        lines.append("- No blockers logged. Confirm with the implementation team.")

    lines.extend(
        [
            "",
            "## Suggested Phases",
            "1. Kickoff and success criteria alignment",
            "2. Technical integration and configuration",
            "3. Enablement and training",
            "4. Launch readiness and validation",
            "5. Post-launch review and expansion planning",
        ]
    )

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("customer_onboarding")

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    logger.debug("Loaded base_url=%s project_id=%s", config.get("base_url"), config.get("project_id"))
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )

    playbooks = fetch_playbooks(api, args.industry, args.limit, logger)
    notes = fetch_account_notes(api, args.account, args.limit, logger)
    plan = format_plan(args.account, args.industry, playbooks, notes)

    print(plan)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(plan, encoding="utf-8")
        logger.info("Saved onboarding plan to %s", args.output)


if __name__ == "__main__":  # pragma: no cover
    main()

