#!/usr/bin/env python3
"""
Scan Cogniz memories for potential compliance issues such as PII exposure or policy keywords.
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
from typing import Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _shared import configure_logging, ensure_memory_api  # noqa: E402

DEFAULT_RULES = [
    {
        "name": "email",
        "description": "Email address detected",
        "pattern": r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}",
        "flags": ["IGNORECASE"],
        "severity": "medium",
    },
    {
        "name": "ssn",
        "description": "US Social Security Number format",
        "pattern": r"\b\d{3}-\d{2}-\d{4}\b",
        "severity": "high",
    },
    {
        "name": "credit_card",
        "description": "13-16 digit sequence (potential card number)",
        "pattern": r"\b(?:\d[ -]*?){13,16}\b",
        "severity": "high",
    },
    {
        "name": "secret",
        "description": "Credential keyword (api key, token, secret, password)",
        "pattern": r"(api[_-]?key|token|secret|password)",
        "flags": ["IGNORECASE"],
        "severity": "high",
    },
    {
        "name": "pii_terms",
        "description": "Regulated PII keywords",
        "pattern": r"(social security|passport|driver'?s license|patient)",
        "flags": ["IGNORECASE"],
        "severity": "medium",
    },
]

FLAG_MAP = {
    "IGNORECASE": re.IGNORECASE,
    "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a compliance sweep on Cogniz memories.")
    parser.add_argument("--config", required=True, help="Path to Cogniz config JSON.")
    parser.add_argument(
        "--query",
        default="category:support-notes OR category:implementation-logs",
        help="Search query defining the scope of the audit.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Max number of memories to review.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional file path to write the findings (Markdown).",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Optional path to write findings as JSON.",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        help="Path to a JSON file defining compliance rules.",
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


def load_rules(path: Optional[Path], logger: logging.Logger) -> List[Dict]:
    if not path:
        logger.debug("Using default compliance rule set.")
        return DEFAULT_RULES

    logger.info("Loading compliance rules from %s", path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Rules file must contain a list of rule definitions.")
    return data


def compile_rules(rules: List[Dict]) -> List[Dict]:
    compiled = []
    for rule in rules:
        flags_value = 0
        for flag in rule.get("flags", []):
            flags_value |= FLAG_MAP.get(flag.upper(), 0)
        compiled.append(
            {
                "name": rule["name"],
                "description": rule.get("description", ""),
                "severity": rule.get("severity", "medium"),
                "pattern": re.compile(rule["pattern"], flags=flags_value),
            }
        )
    return compiled


def inspect_memory(mem: Dict, compiled_rules: List[Dict]) -> List[Dict]:
    issues: List[Dict] = []
    content = mem.get("content") or ""
    for rule in compiled_rules:
        if rule["pattern"].search(content):
            issues.append(
                {
                    "rule": rule["name"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                }
            )
    return issues


def format_report(scope: str, findings: Dict[str, List[Dict]]) -> str:
    lines = [
        "# Compliance Audit Findings",
        "",
        f"Scope Query: {scope}",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
    ]

    totals = {label: len(items) for label, items in findings.items() if items}
    lines.append("## Summary")
    if totals:
        for label, count in sorted(totals.items(), key=lambda item: item[0]):
            lines.append(f"- {label}: {count} potential matches")
    else:
        lines.append("- No issues detected for configured patterns.")

    for label, items in sorted(findings.items(), key=lambda item: item[0]):
        if not items:
            continue
        lines.extend(["", f"## {label.title()}"])
        for mem in items:
            snippet = (mem.get("content") or "").strip().replace("\n", " ")
            lines.append(f"- [{mem.get('id', 'unknown')}] {snippet[:200]}{'...' if len(snippet) > 200 else ''}")

    return "\n".join(lines).strip() + "\n"


def serialize_findings(findings: Dict[str, List[Dict]], rules: List[Dict], scope: str) -> Dict:
    return {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "scope_query": scope,
        "rules": [
            {"name": rule["name"], "description": rule.get("description"), "severity": rule.get("severity")}
            for rule in rules
        ],
        "findings": {
            label: [
                {
                    "memory_id": mem.get("id"),
                    "category": mem.get("category"),
                    "severity": mem.get("severity"),
                    "description": mem.get("description"),
                    "content_snippet": (mem.get("content") or "").strip()[:500],
                }
                for mem in items
            ]
            for label, items in findings.items()
        },
    }


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logger = logging.getLogger("compliance_audit")

    CognizMemoryAPI, load_config, manager_path = ensure_memory_api(SCRIPT_DIR, args.memory_api_path)
    logger.debug("Using Cogniz memory manager from %s", manager_path)

    config = load_config(args.config)
    logger.debug("Loaded base_url=%s project_id=%s", config.get("base_url"), config.get("project_id"))
    api = CognizMemoryAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        project_id=config.get("project_id"),
    )

    raw_rules = load_rules(args.rules, logger)
    compiled_rules = compile_rules(raw_rules)

    logger.info("Running compliance query '%s' (limit=%s)", args.query, args.limit)
    memories = api.search(
        query=args.query,
        limit=args.limit,
        project_id=config.get("project_id"),
    )

    findings: Dict[str, List[Dict]] = defaultdict(list)
    for mem in memories:
        matches = inspect_memory(mem, compiled_rules)
        for match in matches:
            findings[match["rule"]].append({**mem, **match})

    report = format_report(args.query, findings)
    print(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        logger.info("Saved Markdown findings to %s", args.output)

    if args.output_json:
        payload = serialize_findings(findings, raw_rules, args.query)
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        logger.info("Saved JSON findings to %s", args.output_json)


if __name__ == "__main__":  # pragma: no cover
    main()

