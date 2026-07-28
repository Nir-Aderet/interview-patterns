"""
=============================================================
  STACK & QUEUE PATTERNS
=============================================================

Pattern Recognition:
  - "valid parentheses" / "matching pairs" → stack
  - "next greater element" / "next smaller" → monotonic stack
  - "largest rectangle" / "trapped water" → monotonic stack
  - "sliding window maximum" → monotonic deque
  - "implement queue with stacks" → two stacks

Key Insight on Monotonic Stack:
  Maintain a stack that is always increasing or decreasing.
  When the invariant is violated, the popped element has found
  its "next greater" (or smaller) neighbor.
=============================================================
"""

from collections import deque


# =============================================================
# 1. VALID PARENTHESES (LC 20)
# =============================================================

class ValidParentheses:
    """
    LC 20 — Valid Parentheses
    Push open brackets; pop and match on close brackets.
    """
    def isValid(self, s: str) -> bool:
        stack = []
        match = {')': '(', '}': '{', ']': '['}
        for ch in s:
            if ch in match:
                if not stack or stack[-1] != match[ch]:
                    return False
                stack.pop()
            else:
                stack.append(ch)
        return not stack


# =============================================================
# 2. MIN STACK (LC 155)
# =============================================================

class MinStack:
    """
    LC 155 — Min Stack
    Maintain a parallel min_stack that tracks the current min
    at each level of the main stack.
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


# =============================================================
# 3. DAILY TEMPERATURES — MONOTONIC STACK (LC 739)
# =============================================================

class DailyTemperatures:
    """
    LC 739 — Daily Temperatures
    Monotonic decreasing stack (by temperature).
    When a warmer day arrives, pop and record the wait.
    Stack stores INDICES, not values.
    """
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        res = [0] * n
        stack = []  # indices of unresolved days

        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                idx = stack.pop()
                res[idx] = i - idx   # days waited
            stack.append(i)
        return res


# =============================================================
# 4. LARGEST RECTANGLE IN HISTOGRAM (LC 84)
# =============================================================

class LargestRectangle:
    """
    LC 84 — Largest Rectangle in Histogram
    Monotonic increasing stack on (height, start_index).
    When height drops, pop and compute max area for each bar.
    """
    def largestRectangleArea(self, heights: list[int]) -> int:
        max_area = 0
        stack = []   # (height, start)

        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][0] > h:
                height, start = stack.pop()
                max_area = max(max_area, height * (i - start))
            stack.append((h, start))

        # Flush remaining bars — they extend to the end
        for height, start in stack:
            max_area = max(max_area, height * (len(heights) - start))

        return max_area


# =============================================================
# 5. SLIDING WINDOW MAXIMUM — MONOTONIC DEQUE (LC 239)
# =============================================================

class SlidingWindowMaximum:
    """
    LC 239 — Sliding Window Maximum
    Monotonic decreasing deque (stores indices).
    Front of deque = index of current window max.
    Pop from front if out of window; pop from back if smaller than new element.
    Time: O(n)  —  each element pushed/popped at most once.
    """
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        dq = deque()   # indices, decreasing by value
        res = []

        for i, n in enumerate(nums):
            # Remove indices outside the current window
            if dq and dq[0] < i - k + 1:
                dq.popleft()
            # Maintain decreasing invariant
            while dq and nums[dq[-1]] < n:
                dq.pop()
            dq.append(i)
            # Window is fully formed
            if i >= k - 1:
                res.append(nums[dq[0]])
        return res


# =============================================================
# 6. IMPLEMENT QUEUE WITH STACKS (LC 232)
# =============================================================

class MyQueue:
    """
    LC 232 — Implement Queue using Stacks
    Two stacks: inbox and outbox.
    Transfer from inbox → outbox only when outbox is empty.
    Amortized O(1) per operation.
    """
    def __init__(self):
        self.inbox  = []
        self.outbox = []

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _transfer(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self) -> int:
        self._transfer()
        return self.outbox.pop()

    def peek(self) -> int:
        self._transfer()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox


# =============================================================
# 7. PATTERN SUMMARY
# =============================================================
#
# Problem type                    → Stack/Deque pattern
# ─────────────────────────────────────────────────────────────
# Matching brackets / pairs       → plain stack, push open / pop on close
# "Next greater" element          → monotonic decreasing stack
# "Next smaller" element          → monotonic increasing stack
# Largest rectangle               → monotonic increasing stack (start index)
# Sliding window max/min          → monotonic deque (indices)
# Maintain running min/max        → parallel auxiliary stack
# Queue from stacks               → inbox + outbox two-stack trick
