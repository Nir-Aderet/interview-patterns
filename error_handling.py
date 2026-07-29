"""
=============================================================
  ERROR HANDLING — Exceptions, Fail-Fast, and Recovery
=============================================================

Goal:
  Build a mindset for structuring error handling in Python so your
  interview solutions and real code are robust, readable, and testable.

Core ideas:
  - Use exceptions for exceptional situations, not for normal flow
  - Fail fast near the source; catch at boundaries (e.g. CLI, HTTP)
  - Wrap risky blocks; keep the "happy path" clear
=============================================================
"""

from __future__ import annotations

import logging
from typing import Any


logger = logging.getLogger(__name__)


# =============================================================
# 1. CUSTOM EXCEPTIONS
# =============================================================

class AppError(Exception):
    """Base exception for your application.

    Why this works:
      - Single inheritance root makes catching "expected" errors easy.
      - Distinguishes your domain errors from generic Python errors.
    """


class HTTPError(AppError):
    """Represents an HTTP-level failure (non-2xx or transport error)."""


class ValidationError(AppError):
    """Represents invalid user input or JSON payloads."""


# =============================================================
# 2. VALIDATION WITH EXCEPTIONS
# =============================================================

def parse_age(age_str: str) -> int:
    """Example of converting user input to a valid integer age.

    Why this works:
      - We keep parsing and validation local, raising ValidationError.
      - Callers can clearly distinguish "invalid input" from other errors.
    """
    try:
        age = int(age_str)
    except ValueError as exc:
        raise ValidationError(f"Age must be an integer: {age_str}") from exc
    if age <= 0:
        raise ValidationError("Age must be positive")
    return age


# =============================================================
# 3. BOUNDARY LAYER — CATCH AND LOG
# =============================================================

def run_cli(argv: list[str]) -> int:
    """Minimal CLI-style boundary.

    Pattern: "catch at the edge, not in the middle".
    """
    try:
        # Happy path: parse args, call business functions.
        if len(argv) != 2:
            raise ValidationError("Usage: script.py AGE")
        age = parse_age(argv[1])
        print(f"You are {age} years old")
        return 0
    except ValidationError as exc:
        logger.error("User input error: %s", exc)
        return 1
    except Exception as exc:
        # Last-resort catch: log and terminate.
        logger.exception("Unexpected error: %s", exc)
        return 2


# =============================================================
# 4. CONTEXT MANAGER FOR RESOURCE SAFETY
# =============================================================

class SafeFile:
    """Context manager for file operations.

    Why this works:
      - Ensures file is closed even if an exception occurs.
      - Centralizes error handling for file IO.
    """

    def __init__(self, path: str, mode: str = "r"):
        self.path = path
        self.mode = mode
        self._fh = None

    def __enter__(self):
        try:
            self._fh = open(self.path, self.mode, encoding="utf-8")
        except OSError as exc:
            raise AppError(f"Failed to open file {self.path}") from exc
        return self._fh

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self._fh:
            self._fh.close()
        # Returning False propagates any exceptions to caller.
        return False


# =============================================================
# 5. EXAMPLE USAGE
# =============================================================

def read_config(path: str) -> str:
    """Read a config file safely.

    Pattern: use SafeFile to handle IO errors consistently.
    """
    with SafeFile(path, "r") as fh:
        return fh.read()


# =============================================================
# 6. PATTERN SUMMARY
# =============================================================
#
# Signal in problem statement       → Error-handling pattern
# ────────────────────────────────────────────────────────────
# "invalid user input"             → ValidationError with clear message
# "wrap resources"                 → context manager (__enter__/__exit__)
# "log and continue"               → catch AppError at boundary, log, return code
# "multiple error types"           → custom exception hierarchy
# "cleanup on error"               → finally block or context manager
