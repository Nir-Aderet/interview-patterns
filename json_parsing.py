"""
=============================================================
  JSON PARSING — Turning Text into Structured Data
=============================================================

Goal:
  Comfortably read, transform, and validate JSON responses in Python,
  and recognize when to use schemas vs ad-hoc dict handling.

Core ideas:
  - JSON ≈ nested dict/list/str/int/bool/None in Python
  - You should treat JSON as untrusted input → validate shape & types
  - Small scripts: ad-hoc dict access; bigger systems: schemas / models
=============================================================
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List


# =============================================================
# 1. BASIC LOADING AND DUMPING
# =============================================================

def load_json_string(text: str) -> Dict[str, Any]:
    """Parse JSON string into Python dict.

    Why this works:
      - json.loads() turns text into native Python objects.
      - We type-hint Dict[str, Any] to signal "dynamic JSON".
    """
    return json.loads(text)


def dump_json_pretty(data: Dict[str, Any]) -> str:
    """Serialize Python dict to pretty-printed JSON string.

    Why this works:
      - json.dumps(..., indent=2, sort_keys=True) improves readability.
      - sort_keys helps with stable diffs/logging.
    """
    return json.dumps(data, indent=2, sort_keys=True)


# =============================================================
# 2. DEFENSIVE ACCESS — AVOID KEYERRORS
# =============================================================

def get_user_name(user_json: Dict[str, Any]) -> str:
    """Safely get a user's name from JSON.

    Interview-style pattern: "Access nested JSON without crashing".
    """
    # .get() returns None by default instead of raising KeyError.
    name = user_json.get("name")
    if not isinstance(name, str):
        raise ValueError("Invalid user JSON: 'name' must be a string")
    return name


# =============================================================
# 3. SCHEMA VIA DATACLASS
# =============================================================

@dataclass
class User:
    """Example schema for user JSON.

    Why this works:
      - dataclass gives you a lightweight "model" without frameworks.
      - Converting JSON → Dataclass clarifies required/optional fields.
    """
    id: int
    name: str
    email: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "User":
        """Validate and construct a User from JSON dict.

        We explicitly pull fields so missing keys raise KeyError,
        which error-handling patterns can catch.
        """
        return cls(id=int(data["id"]), name=str(data["name"]), email=str(data["email"]))


# =============================================================
# 4. TRANSFORMING JSON LISTS
# =============================================================

def emails_from_users(users_json: List[Dict[str, Any]]) -> List[str]:
    """Extract valid email strings from a list of user JSON objects."""
    emails: List[str] = []
    for data in users_json:
        try:
            user = User.from_json(data)
        except (KeyError, ValueError, TypeError):
            # In a real system, log and continue; here we skip invalid entries.
            continue
        emails.append(user.email)
    return emails


# =============================================================
# 5. JSON + HTTP — TYPICAL PIPELINE
# =============================================================

def parse_users_response(response_text: str) -> List[User]:
    """Example of end-to-end JSON handling.

    Pattern: HTTP client → response.text → json.loads → schema.
    """
    raw = load_json_string(response_text)
    items = raw.get("results") or raw
    if not isinstance(items, list):
        raise ValueError("Expected a list of users in 'results'")
    return [User.from_json(item) for item in items]


# =============================================================
# 6. PATTERN SUMMARY
# =============================================================
#
# Signal in problem statement       → JSON pattern
# ────────────────────────────────────────────────────────────
# "parse API response"              → json.loads + defensive .get()
# "map JSON to objects"            → dataclasses or Pydantic models
# "extract specific fields"        → list comprehension + validation
# "nested JSON shape"              → recursive parsing or typed models
# "invalid / missing fields"       → raise + handle in error-handling.py
