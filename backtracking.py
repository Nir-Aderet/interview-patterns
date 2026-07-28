"""
=============================================================
  BACKTRACKING
=============================================================

Pattern Recognition:
  - "all permutations" / "all subsets" / "all combinations" → backtracking
  - "place N queens" / "solve sudoku" → backtracking + constraint check
  - "word search" in grid → DFS + visited set (backtrack)
  - "palindrome partitioning" → backtrack on split points

Template:
  def backtrack(state, choices):
      if is_goal(state):
          result.append(copy(state))
          return
      for choice in choices:
          if is_valid(state, choice):
              make(state, choice)
              backtrack(state, next_choices)
              undo(state, choice)          ← THE KEY STEP

The undo step is what makes it backtracking (not just DFS).
=============================================================
"""


# =============================================================
# 1. SUBSETS (LC 78)
# =============================================================

class Subsets:
    """
    LC 78 — Subsets (all 2^n subsets, no duplicates in input)
    At each index, choose: include or exclude.
    start_idx prevents re-using earlier elements.
    """
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        def backtrack(start, path):
            res.append(path[:])            # snapshot current subset
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()                 # undo
        backtrack(0, [])
        return res


# =============================================================
# 2. SUBSETS II (LC 90) — WITH DUPLICATES
# =============================================================

class SubsetsII:
    """
    LC 90 — Subsets II (array may have duplicates)
    Sort first. Skip duplicate values at the same recursion level.
    """
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        def backtrack(start, path):
            res.append(path[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:  # skip duplicate
                    continue
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()
        backtrack(0, [])
        return res


# =============================================================
# 3. PERMUTATIONS (LC 46)
# =============================================================

class Permutations:
    """
    LC 46 — Permutations (all elements distinct)
    Use a 'used' set to track which elements are in the current path.
    """
    def permute(self, nums: list[int]) -> list[list[int]]:
        res = []
        def backtrack(path, used):
            if len(path) == len(nums):
                res.append(path[:])
                return
            for n in nums:
                if n not in used:
                    path.append(n)
                    used.add(n)
                    backtrack(path, used)
                    path.pop()
                    used.remove(n)
        backtrack([], set())
        return res


# =============================================================
# 4. COMBINATION SUM (LC 39)
# =============================================================

class CombinationSum:
    """
    LC 39 — Combination Sum (elements can be reused)
    Pass same index i (not i+1) to allow reuse.
    Prune: if remaining < 0, stop.
    """
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        res = []
        def backtrack(start, path, remaining):
            if remaining == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break                    # sort candidates first to enable pruning
                path.append(candidates[i])
                backtrack(i, path, remaining - candidates[i])  # i, not i+1
                path.pop()
        candidates.sort()
        backtrack(0, [], target)
        return res


# =============================================================
# 5. PALINDROME PARTITIONING (LC 131)
# =============================================================

class PalindromePartitioning:
    """
    LC 131 — Palindrome Partitioning
    At each split point, check if the prefix is a palindrome.
    Only recurse if it is.
    """
    def partition(self, s: str) -> list[list[str]]:
        res = []
        def is_palindrome(sub): return sub == sub[::-1]
        def backtrack(start, path):
            if start == len(s):
                res.append(path[:])
                return
            for end in range(start + 1, len(s) + 1):
                substr = s[start:end]
                if is_palindrome(substr):
                    path.append(substr)
                    backtrack(end, path)
                    path.pop()
        backtrack(0, [])
        return res


# =============================================================
# 6. WORD SEARCH (LC 79)
# =============================================================

class WordSearch:
    """
    LC 79 — Word Search in Grid
    DFS with in-place visited marking (restore on backtrack).
    Temporarily set cell to '#' to mark visited, restore after.
    """
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r, c, idx):
            if idx == len(word):
                return True
            if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[idx]:
                return False
            tmp, board[r][c] = board[r][c], '#'   # mark visited
            found = any(dfs(r + dr, c + dc, idx + 1)
                        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)])
            board[r][c] = tmp                      # restore
            return found

        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


# =============================================================
# 7. N-QUEENS (LC 51)
# =============================================================

class NQueens:
    """
    LC 51 — N-Queens
    Place one queen per row. Track which columns and diagonals are occupied.
    Diagonals: (r - c) for '\\', (r + c) for '/'
    """
    def solveNQueens(self, n: int) -> list[list[str]]:
        res = []
        cols, diag1, diag2 = set(), set(), set()

        def backtrack(row, board):
            if row == n:
                res.append([''.join(r) for r in board])
                return
            for col in range(n):
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue
                cols.add(col); diag1.add(row - col); diag2.add(row + col)
                board[row][col] = 'Q'
                backtrack(row + 1, board)
                board[row][col] = '.'
                cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

        backtrack(0, [['.' for _ in range(n)] for _ in range(n)])
        return res


# =============================================================
# 8. PATTERN SUMMARY
# =============================================================
#
# Trigger                         → Backtracking variant
# ─────────────────────────────────────────────────────────
# All subsets                     → include/exclude each element
# All permutations                → used set, try every unused element
# Combinations with reuse         → pass same index i
# No reuse                        → pass i + 1
# Has duplicates                  → sort + skip if nums[i] == nums[i-1] at same level
# Grid path search                → in-place mark + restore (# trick)
# Constraint placement (queens)   → track cols + both diagonals
# Pruning: sort + break when over target → huge speedup for combination sum
