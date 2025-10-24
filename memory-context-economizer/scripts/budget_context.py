#!/usr/bin/env python3
"""
Analyze text files or stdin content to estimate token usage and highlight trimming opportunities.

Claude Code can execute this script locally to identify bulky sections before sending them to Claude.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Tuple

AVERAGE_CHARS_PER_TOKEN = 4


def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s | %(message)s")


def read_content(path: Path | None) -> str:
    if path:
        return path.read_text(encoding="utf-8")
    return sys.stdin.read()


def estimate_tokens(text: str) -> int:
    return max(1, round(len(text) / AVERAGE_CHARS_PER_TOKEN))


def largest_blocks(text: str, block_size: int, limit: int) -> List[Tuple[int, int, str]]:
    blocks = []
    lines = text.splitlines()
    for idx in range(0, len(lines), block_size):
        chunk = "\n".join(lines[idx : idx + block_size])
        blocks.append((idx + 1, estimate_tokens(chunk), chunk))
    blocks.sort(key=lambda item: item[1], reverse=True)
    return blocks[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate token usage and identify heavy sections before sending context to Claude."
    )
    parser.add_argument("--input-file", type=Path, help="Path to a text file. Reads stdin when omitted.")
    parser.add_argument("--block-lines", type=int, default=50, help="Line interval for block analysis.")
    parser.add_argument("--top", type=int, default=5, help="Number of heaviest blocks to display.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    args = parser.parse_args()

    configure_logging(args.verbose)
    logger = logging.getLogger("budget_context")

    text = read_content(args.input_file)
    total_tokens = estimate_tokens(text)
    logger.info("Approximate length: %s characters (~%s tokens)", len(text), total_tokens)

    blocks = largest_blocks(text, args.block_lines, args.top)
    print(f"Top {len(blocks)} heavy segments (approx tokens):")
    for start_line, tokens, chunk in blocks:
        preview = chunk.replace("\n", " ")[:160]
        print(f"- Lines {start_line}-{start_line + args.block_lines - 1}: ~{tokens} tokens :: {preview}")

    print("\nTip: Remove or summarize these blocks before pasting into Claude to stay within context budgets.")


if __name__ == "__main__":  # pragma: no cover
    main()

