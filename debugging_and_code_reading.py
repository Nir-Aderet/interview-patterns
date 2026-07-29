"""
=============================================================
  DEBUGGING & READING LARGE CODEBASES
=============================================================

Goal:
  Train habits for understanding and debugging unfamiliar or large
  amounts of code quickly — crucial both in interviews (reading the
  starter code) and on the job.

Core ideas:
  - Start from entry points and data flow, not random lines
  - Use logs, breakpoints, and small experiments instead of guessing
  - Reduce complexity by drawing a simple mental model first
=============================================================
"""

from __future__ import annotations

import logging
import pdb
from typing import Callable


logger = logging.getLogger(__name__)


# =============================================================
# 1. ADDING TARGETED LOGGING
# =============================================================

def debug_value_flow(fn: Callable[[int], int], value: int) -> int:
    """Example helper that logs function input and output.

    Why this works:
      - Instead of scattering print() everywhere, we wrap the call.
      - Logging shows the data passing through without changing logic.
    """
    logger.debug("Calling %s with value=%d", fn.__name__, value)
    result = fn(value)
    logger.debug("%s returned %d", fn.__name__, result)
    return result


def sample_transform(x: int) -> int:
    """Dummy function to demonstrate debug_value_flow."""
    return x * x + 1


# =============================================================
# 2. BREAKPOINTS WITH pdb
# =============================================================

def inspect_buggy_logic(x: int, y: int) -> int:
    """Demonstrate how to drop into pdb to inspect state.

    In practice, you'd call `inspect_buggy_logic` from failing code,
    then step through with `pdb`.
    """
    total = x + y
    pdb.set_trace()  # Drop into interactive debugger here.
    # From the debugger you can inspect `total`, `x`, `y` and try fixes.
    return total


# =============================================================
# 3. READING FLOW — ENTRY-POINT-ORIENTED
# =============================================================

def main_flow(username: str) -> None:
    """Toy example of an "entry point" function.

    Reading tip:
      - Start at functions like `main_flow` or route handlers.
      - Identify inputs, outputs, and side-effects (IO, DB, HTTP).
    """
    logger.info("Starting flow for user=%s", username)
    profile = load_user_profile(username)
    result = process_profile(profile)
    save_result(result)
    logger.info("Finished flow for user=%s", username)


def load_user_profile(username: str) -> dict:
    # In real code, this would call a DB or API; here we stub.
    return {"username": username, "score": 42}


def process_profile(profile: dict) -> dict:
    profile = {**profile, "status": "active"}
    return profile


def save_result(result: dict) -> None:
    # Pretend this writes somewhere; logging is enough for demonstration.
    logger.debug("Saving result: %r", result)


# =============================================================
# 4. MECHANICAL READING CHECKLIST (AS CODE COMMENTS)
# =============================================================
#
# When faced with a big, unfamiliar file:
#   1. Find the entry points: main(), CLI handlers, HTTP routes, class
#      methods referenced by tests.
#   2. Sketch data flow: what comes in, what transformations happen,
#      what goes out.
#   3. Search for logging and error-handling: where do failures surface?
#   4. Use debugger/logging around suspected faulty areas, not everywhere.
#   5. Gradually inline or simplify indirections (helper functions that
#      just call another helper) to reduce mental overhead.
#
# Interview signal:
#   - "Here is a lot of starter code" → respond by finding entry point,
#     reading signatures, and tracing a single example flow with prints
#     or logs before editing anything.
