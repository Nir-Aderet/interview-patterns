"""
=============================================================
  DYNAMIC PROGRAMMING — Complete Interview Guide (Python)
=============================================================

Two mandatory conditions for DP:
  1. Optimal Substructure  — optimal solution builds from optimal sub-solutions
  2. Overlapping Subproblems — same subproblems recur, making caching worthwhile

5-Step Framework (use this in every interview):
  1. Define the state       — what does dp[i] or dp[i][j] represent?
  2. Write the recurrence   — how does current state depend on previous?
  3. Identify base cases    — what are the smallest known values?
  4. Choose top-down / bottom-up
  5. Answer the question    — which cell in dp is the final answer?
=============================================================
"""

import functools
import sys
sys.setrecursionlimit(10_000)  # raise Python's default limit of 1000 for large inputs


# =============================================================
# 1. MEMOIZATION (TOP-DOWN)
# =============================================================
# When to use:
#   - You think recursively about the problem naturally
#   - Not all subproblems need to be solved (sparse state space)
#   - State is complex (tuples, strings as keys)

# --- Option A: @lru_cache (fastest to write in interviews) ---

class ClimbStairs_TopDown:
    """LC 70 — Climbing Stairs"""
    def climbStairs(self, n: int) -> int:
        @functools.lru_cache(maxsize=None)  # maxsize=None = unlimited cache
        def dp(i):
            if i <= 1:
                return 1          # base cases: 1 way to reach step 0 or 1
            return dp(i - 1) + dp(i - 2)
        return dp(n)


# --- Option B: Manual memo dict (shows deeper understanding) ---

class ClimbStairs_ManualMemo:
    """LC 70 — Climbing Stairs (manual memoization)"""
    def climbStairs(self, n: int) -> int:
        memo = {}
        def dp(i):
            if i in memo:
                return memo[i]
            if i <= 1:
                return 1
            memo[i] = dp(i - 1) + dp(i - 2)
            return memo[i]
        return dp(n)


# =============================================================
# 2. TABULATION (BOTTOM-UP)
# =============================================================
# When to use:
#   - All subproblems must be solved anyway (dense state space)
#   - You want space optimization (harder with recursion)
#   - Interviewer explicitly wants iterative solution

# --- 1D DP: Coin Change (LC 322) ---

class CoinChange:
    """
    LC 322 — Coin Change
    State:  dp[a] = minimum coins to make amount a
    Recurrence: dp[a] = min(dp[a - coin] + 1) for each coin
    Base case: dp[0] = 0
    """
    def coinChange(self, coins: list[int], amount: int) -> int:
        INF = float('inf')
        dp = [INF] * (amount + 1)
        dp[0] = 0

        for a in range(1, amount + 1):
            for coin in coins:
                if a - coin >= 0:
                    dp[a] = min(dp[a], dp[a - coin] + 1)

        return dp[amount] if dp[amount] != INF else -1


# --- 2D DP: Longest Common Subsequence (LC 1143) ---

class LongestCommonSubsequence:
    """
    LC 1143 — Longest Common Subsequence
    State:  dp[i][j] = LCS length of text1[:i] and text2[:j]
    Recurrence:
        if text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
        else:                         dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    Base case: dp[0][j] = dp[i][0] = 0 (empty string)
    """
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]


# =============================================================
# 3. SPACE OPTIMIZATION
# =============================================================
# Many 2D tables only look back one row — compress to O(n) space.

class LCS_SpaceOptimized:
    """LC 1143 — LCS with O(n) space instead of O(m*n)"""
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        n = len(text2)
        prev = [0] * (n + 1)

        for ch1 in text1:
            curr = [0] * (n + 1)
            for j, ch2 in enumerate(text2, 1):
                if ch1 == ch2:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            prev = curr

        return prev[n]


# --- 0/1 Knapsack with O(W) space ---
# KEY: iterate weight dimension IN REVERSE to avoid using same item twice

def knapsack_01(weights: list[int], values: list[int], W: int) -> int:
    """
    0/1 Knapsack — each item used at most once
    State:  dp[cap] = max value with capacity cap
    Recurrence: dp[cap] = max(dp[cap], dp[cap - w] + v)
    Reverse iteration prevents reusing the same item in one pass.
    """
    dp = [0] * (W + 1)
    for w, v in zip(weights, values):
        for cap in range(W, w - 1, -1):  # REVERSE
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]


def knapsack_unbounded(weights: list[int], values: list[int], W: int) -> int:
    """
    Unbounded Knapsack — each item can be used unlimited times
    Forward iteration allows reusing items in the same pass.
    """
    dp = [0] * (W + 1)
    for w, v in zip(weights, values):
        for cap in range(w, W + 1):  # FORWARD
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]


# =============================================================
# 4. DP ON STRINGS
# =============================================================

class WordBreak_II:
    """
    LC 140 — Word Break II
    State:  dp[i] = all valid sentences formed from s[i:]
    Top-down with memo — returns list of sentences
    """
    def wordBreak(self, s: str, wordDict: list[str]) -> list[str]:
        word_set = set(wordDict)
        memo = {}

        def dp(start):
            if start in memo:
                return memo[start]
            if start == len(s):
                return [""]  # base case: one empty suffix
            res = []
            for end in range(start + 1, len(s) + 1):
                word = s[start:end]
                if word in word_set:
                    for sentence in dp(end):
                        res.append(word + (" " + sentence if sentence else ""))
            memo[start] = res
            return res

        return dp(0)


class EditDistance:
    """
    LC 72 — Edit Distance
    State:  dp[i][j] = min edits to convert word1[:i] to word2[:j]
    Recurrence:
        if chars match:  dp[i][j] = dp[i-1][j-1]
        else:            dp[i][j] = 1 + min(dp[i-1][j],   # delete
                                            dp[i][j-1],   # insert
                                            dp[i-1][j-1]) # replace
    """
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i   # delete all chars of word1
        for j in range(n + 1):
            dp[0][j] = j   # insert all chars of word2

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[m][n]


# =============================================================
# 5. INTERVAL DP
# =============================================================
# State is a range [l, r]. Fill by increasing length.

class PalindromicSubstrings:
    """
    LC 647 — Palindromic Substrings
    State:  dp[l][r] = True if s[l..r] is a palindrome
    Fill by substring length (len 1 first, then len 2, etc.)
    """
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        count = 0

        for length in range(1, n + 1):        # substring length
            for l in range(n - length + 1):
                r = l + length - 1
                if length == 1:
                    dp[l][r] = True
                elif length == 2:
                    dp[l][r] = (s[l] == s[r])
                else:
                    dp[l][r] = (s[l] == s[r]) and dp[l + 1][r - 1]
                if dp[l][r]:
                    count += 1

        return count


# =============================================================
# 6. DP ON TREES
# =============================================================
# "Bottom-up DP" on trees = post-order DFS: compute children first.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class HouseRobberIII:
    """
    LC 337 — House Robber III
    State per node: (max_without_node, max_with_node)
    Post-order: resolve children before parent.
    """
    def rob(self, root: TreeNode) -> int:
        def dp(node):
            if not node:
                return 0, 0   # (skip, take)
            left_skip,  left_take  = dp(node.left)
            right_skip, right_take = dp(node.right)

            take = node.val + left_skip + right_skip
            skip = max(left_skip, left_take) + max(right_skip, right_take)
            return skip, take

        skip, take = dp(root)
        return max(skip, take)


# =============================================================
# 7. STATE MACHINE DP
# =============================================================
# Model discrete states (e.g., holding/not holding stock, cooldown).

class BestTimeToBuyAndSellStockWithCooldown:
    """
    LC 309 — Best Time to Buy and Sell Stock with Cooldown
    States: hold (own stock), sold (just sold, in cooldown), rest (idle)
    Transition:
        hold[i] = max(hold[i-1], rest[i-1] - price)   # buy or keep holding
        sold[i] = hold[i-1] + price                    # sell today
        rest[i] = max(rest[i-1], sold[i-1])            # idle or come off cooldown
    """
    def maxProfit(self, prices: list[int]) -> int:
        hold = float('-inf')
        sold = 0
        rest = 0

        for price in prices:
            prev_sold = sold
            sold = hold + price
            hold = max(hold, rest - price)
            rest = max(rest, prev_sold)

        return max(sold, rest)


# =============================================================
# 8. DP PATTERNS QUICK REFERENCE
# =============================================================
#
# Pattern          | Key signal                      | State      | Example LCs
# -----------------|---------------------------------|------------|------------------
# Linear 1D        | array, max subarray, sequence   | dp[i]      | 53, 152, 300, 322
# Knapsack         | pick items, subset sum          | dp[i][cap] | 416, 494, 518
# String DP        | two strings, edit, LCS          | dp[i][j]   | 72, 1143, 115
# Interval DP      | palindrome, any partition       | dp[l][r]   | 5, 516, 312
# Tree DP          | binary tree subproblem          | recursion  | 124, 337, 968
# State Machine    | at most k, cooldown             | dp[i][s]   | 121-123, 309
# Digit DP         | count nums with property        | dp[pos]    | 233, 357


# =============================================================
# 9. BEST PRACTICES SUMMARY
# =============================================================
#
# 1. Always verbalize your recurrence BEFORE coding.
#    "dp[i] = max profit ending at day i" shows your thought process.
#
# 2. Use @lru_cache on inner functions — idiomatic Python, saves lines.
#
# 3. Name dp tables semantically: dp_ways, dp_profit, dp_len — not just dp.
#
# 4. Handle base cases explicitly and first — most off-by-one bugs live here.
#
# 5. Verify with a tiny example by hand before coding (n=3, s="ab").
#
# 6. Correctness first, space optimization second (only optimize if asked).
#
# 7. For 0/1 knapsack space optimization: iterate weights in REVERSE.
#    For unbounded knapsack: iterate weights FORWARD.
#
# 8. Python recursion limit is 1000 — use sys.setrecursionlimit() or
#    switch to bottom-up if n > 500.
#
# 9. @lru_cache requires hashable arguments — use tuples, not lists, as keys.
#
# 10. When in doubt: top-down is faster to write; bottom-up is safer for
#     large inputs and space optimization.
