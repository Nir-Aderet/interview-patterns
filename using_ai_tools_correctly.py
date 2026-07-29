"""
=============================================================
  USING AI TOOLS CORRECTLY AS A DEVELOPER
=============================================================

Goal:
  Turn AI tools (Perplexity, Claude, etc.) into reliable collaborators,
  not crutches, and integrate them into your interview prep and daily
  coding work.

This file is influenced by your attached AI guides and prompt-engineering
course notes, adapted into concrete coding patterns.[cite:7][cite:9]
=============================================================
"""

from __future__ import annotations

# NOTE: This file is mostly guidance plus tiny code examples.
#       Treat it as a "living manual" you can extend.


# =============================================================
# 1. PATTERN: SPECIFIC, STRUCTURED PROMPTS
# =============================================================

example_prompt = """\
Role: You are a senior Python engineer.

Context: I have this function that is O(n^2). It runs on lists of length
up to 10^5. I want to make it O(n log n) or better.

Input code:
```python
# original code here
```

Task:
1. Identify the bottleneck with Big-O notation.
2. Propose 2 alternative algorithms, with pros/cons.
3. Rewrite the function using the best approach.
4. Provide test cases that cover edge cases.
"""

# Why this works:
#   - Role + Context + Input + Task is a reusable prompt pattern.
#   - Enumerated tasks help the model structure its answer.
#   - You can copy/paste this pattern into Perplexity / Claude and
#     swap in the details for each coding question.


# =============================================================
# 2. PATTERN: PROMPT → VERIFY → INTEGRATE
# =============================================================

def ai_refactor_and_verify(original_fn, tests):
    """Conceptual pattern for using AI-generated code safely.

    Steps (what you actually do in your workflow):
      1. Ask AI for a refactor (using a structured prompt like above).
      2. Paste its suggestion into a scratch file, not production.
      3. Run your own tests (and add more) locally.
      4. Only integrate once tests pass and the logic is clear to you.

    Why this matters:
      - Your mental model + tests are the real guarantees, not AI.
      - In interviews, you must still be able to explain the code.
    """
    # This function is illustrative; you implement the steps manually.
    pass


# =============================================================
# 3. PATTERN: FEW-SHOT EXAMPLES FOR FORMAT & STYLE
# =============================================================

few_shot_example = """\
System: You are a code review assistant. You care most about:
- correctness
- performance
- readability

User:
Here is an example of the kind of review I want:

Bad code:
```python
for i in range(len(nums)):
    for j in range(len(nums)):
        if i != j and nums[i] + nums[j] == target:
            return i, j
```

Good review:
1. Complexity: This is O(n^2); can be reduced to O(n) with a hash map.
2. Correctness: It works but may return duplicate indices.
3. Suggestion: Use a dictionary to store seen values.
4. Example fix: (show code).

Now review this new function in the SAME style:
```python
# your code here
```\
"""

# Why this works:
#   - You show the AI what "good output" looks like (few-shot prompting).
#   - You anchor the style and structure so reviews are consistent.


# =============================================================
# 4. PATTERN: USING AI FOR BIG CODE READING
# =============================================================

big_code_prompt = """\
I have a large codebase. Please:
1. Identify the main entry points (CLI, HTTP routes, main functions).
2. Summarize the data flow between those components.
3. List 3-5 places where bugs are most likely (based on patterns).
4. Suggest a debugging plan using logging and breakpoints.
"""

# Combine this with your debugging_and_code_reading.py patterns:
#   - Ask AI for an overview, then you yourself run experiments and
#     step through with the debugger.


# =============================================================
# 5. PATTERN SUMMARY
# =============================================================
#
# Signal                             → AI usage pattern
# ─────────────────────────────────────────────────────────────
# "need help improving code"         → Role+Context+Input+Task prompt
# "need specific output format"      → Few-shot examples showing format
# "huge codebase"                    → Big-code prompt + your own probing
# "can't trust model fully"          → Prompt → Verify → Integrate workflow
# "interview prep with AI"           → Use AI to explain patterns, then
#                                      implement them yourself in this repo.
