"""
Common utilities for Cogniz Memory Skills helper scripts.

Provides logging configuration and robust loading of the Cogniz memory manager API.
This module is shared across all Cogniz Memory Skills for consistent functionality.

Version: 2.0.0 (Commercial Grade)
License: Apache 2.0
"""

from __future__ import annotations

import importlib
import logging
import os
import sys
from pathlib import Path
from typing import Optional, Tuple, Type


def configure_logging(verbose: bool = False) -> None:
    """
    Configure CLI logging with sensible defaults.

    Args:
        verbose: If True, sets logging level to DEBUG; otherwise INFO
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def ensure_memory_api(
    requester_path: Path,
    memory_api_path: Optional[str] = None,
) -> Tuple[Type, callable, Path]:
    """
    Ensure `memory_api` from the Cogniz memory manager is importable.

    Searches for the memory_api module in the following order:
    1. Path provided via memory_api_path parameter
    2. Path from COGNIZ_MEMORY_MANAGER_PATH environment variable
    3. Default relative path (../cogniz-memory-manager-local/scripts)

    Args:
        requester_path: Path of the script requesting the dependency
        memory_api_path: Optional override path to the memory manager scripts directory

    Returns:
        Tuple of (CognizMemoryAPI class, load_config function, resolved path)

    Raises:
        ModuleNotFoundError: If the dependency cannot be located in any search path

    Example:
        >>> from pathlib import Path
        >>> script_dir = Path(__file__).resolve().parent
        >>> CognizMemoryAPI, load_config, path = ensure_memory_api(script_dir)
    """
    logger = logging.getLogger("memory_api_loader")
    candidates = []

    # Priority 1: Explicit path parameter
    if memory_api_path:
        candidates.append(Path(memory_api_path))

    # Priority 2: Environment variable
    env_path = os.getenv("COGNIZ_MEMORY_MANAGER_PATH")
    if env_path:
        candidates.append(Path(env_path))

    # Priority 3: Default relative path
    default_path = requester_path.resolve().parents[2] / "cogniz-memory-manager-local" / "scripts"
    candidates.append(default_path)

    tried = []
    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        tried.append(str(candidate))

        if (candidate / "memory_api.py").exists():
            if str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
            logger.debug("Using memory_api from %s", candidate)

            try:
                memory_api = importlib.import_module("memory_api")
                return (
                    getattr(memory_api, "CognizMemoryAPI"),
                    getattr(memory_api, "load_config"),
                    candidate
                )
            except (ImportError, AttributeError) as e:
                logger.error("Found memory_api.py but failed to import: %s", e)
                continue

    message = (
        "Unable to locate or import memory_api.py. "
        f"Checked: {', '.join(tried)}. "
        "Please install cogniz-memory-manager-local or set COGNIZ_MEMORY_MANAGER_PATH."
    )
    raise ModuleNotFoundError(message)


__all__ = ["configure_logging", "ensure_memory_api"]
