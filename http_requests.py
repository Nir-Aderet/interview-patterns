"""
=============================================================
  HTTP REQUESTS — Practical Patterns in Python
=============================================================

Goal:
  Build a solid mental model for making HTTP requests with Python,
  handling timeouts, retries, status codes, and common interview-style
  tasks (REST APIs, pagination, etc.).

Core ideas:
  - HTTP is just request → response over the network
  - You control METHOD (GET/POST/PUT/DELETE), URL, headers, body
  - You MUST handle errors: timeouts, non-2xx status, malformed data
  - You should separate "transport" (requests) from "business logic"
=============================================================
"""

from __future__ import annotations

import requests
from typing import Any, Dict, Optional


# =============================================================
# 1. BASIC REQUESTS — GET and POST
# =============================================================

class BasicHTTPClient:
    """Minimal wrapper around requests for simple APIs.

    Pattern recognition:
      - You see "call this REST API" → think: GET/POST + params + JSON.
      - You see "parse JSON" → combine with json_parsing patterns.
    """

    def get_json(self, url: str, timeout: float = 5.0) -> Dict[str, Any]:
        """Perform a GET request and return JSON.

        Why this works:
          - timeout guards against hanging connections (never omit it).
          - response.raise_for_status() converts HTTP error codes into
            Python exceptions that you can handle in error-handling patterns.
          - response.json() parses JSON directly, raising if invalid.
        """
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()          # fail fast on non-2xx
        return resp.json()

    def post_json(self, url: str, payload: Dict[str, Any], timeout: float = 5.0) -> Dict[str, Any]:
        """Perform a POST request with JSON payload.

        Why this works:
          - json=payload tells requests to serialize and set headers.
          - Same error-handling pattern as GET.
        """
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()


# =============================================================
# 2. ROBUST CLIENT — TIMEOUTS, RETRIES, HEADERS
# =============================================================

class RobustHTTPClient:
    """HTTP client with retries and default headers.

    This models the interview pattern: "build a resilient client".
    """

    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip("/")  # avoid double slashes
        self.session = requests.Session()      # reuse TCP connection
        self.session.headers.update(default_headers or {})

    def _request_with_retries(
        self,
        method: str,
        path: str,
        *,
        retries: int = 3,
        timeout: float = 5.0,
        **kwargs: Any,
    ) -> requests.Response:
        """Core transport function with simple retry loop.

        Why this works:
          - We centralize retry logic so all endpoints inherit behavior.
          - Only retry on *transient* errors (here: exceptions / 5xx).
          - We do NOT retry on 4xx (client errors) — usually a bug.
        """
        url = f"{self.base_url}/{path.lstrip('/') }"

        last_exc: Optional[Exception] = None
        for attempt in range(1, retries + 1):
            try:
                resp = self.session.request(method, url, timeout=timeout, **kwargs)
                # If server error (5xx), we may retry; otherwise return.
                if 500 <= resp.status_code < 600 and attempt < retries:
                    continue
                return resp
            except requests.RequestException as exc:
                # Transport-level issue: DNS, connection, timeout, etc.
                last_exc = exc
                if attempt == retries:
                    raise
        # Defensive fallback; normally unreachable because of raise above.
        raise last_exc if last_exc else RuntimeError("Request failed without exception")

    def get_json(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        resp = self._request_with_retries("GET", path, **kwargs)
        resp.raise_for_status()
        return resp.json()


# =============================================================
# 3. PAGINATION PATTERN
# =============================================================

class PaginatedClient(RobustHTTPClient):
    """Pattern for iterating over paginated HTTP APIs.

    Many APIs expose results page by page, e.g. `?page=1&page_size=50`.
    Recognizing this pattern lets you write an iterator once and reuse it.
    """

    def iter_pages(self, path: str, *, page_size: int = 50):
        """Yield pages of JSON results.

        Why this works:
          - We use a generator so callers can process items lazily.
          - We stop when the API returns fewer than page_size results.
        """
        page = 1
        while True:
            params = {"page": page, "page_size": page_size}
            resp = self._request_with_retries("GET", path, params=params)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("results") or data
            if not items:
                break
            yield items
            if len(items) < page_size:
                break
            page += 1


# =============================================================
# 4. INTERVIEW-STYLE EXERCISE
# =============================================================

def fetch_all_users(client: PaginatedClient) -> list[Dict[str, Any]]:
    """Example function for an interview task.

    Task: "Given a paginated /users endpoint, return all users as a list".

    Why this works:
      - We keep business logic (users) separate from HTTP details.
      - We rely on the pagination iterator to hide API mechanics.
    """
    users: list[Dict[str, Any]] = []
    for page in client.iter_pages("users"):
        users.extend(page)
    return users


# =============================================================
# 5. PATTERN SUMMARY
# =============================================================
#
# Signal in problem statement       → HTTP pattern to reach for
# ─────────────────────────────────────────────────────────────
# "Call REST API"                   → Basic HTTP client + JSON parsing
# "Handle timeouts / retries"      → Wrapper with Session + retry loop
# "Paginated endpoint"             → Generator that yields pages/items
# "Different environments"         → base_url + environment-specific config
# "Test without network"           → dependency-inject client, mock methods
