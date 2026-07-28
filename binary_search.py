"""
=============================================================
  BINARY SEARCH PATTERNS
=============================================================

Pattern Recognition:
  - "sorted array" + O(log n) hint → binary search
  - "rotated sorted array" → modified binary search
  - "find minimum" / "find peak" → binary search on answer
  - "search in 2D matrix" → treat as 1D array
  - "minimum max" / "maximum min" → binary search on the answer space

Template — left-inclusive, right-exclusive [lo, hi):
  lo, hi = 0, len(nums)
  while lo < hi:
      mid = lo + (hi - lo) // 2    ← avoids integer overflow
      if condition(mid):
          hi = mid
      else:
          lo = mid + 1
  return lo
=============================================================
"""


# =============================================================
# 1. CLASSIC BINARY SEARCH (LC 704)
# =============================================================

class BinarySearch:
    """LC 704 — Binary Search. Returns index or -1."""
    def search(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1


# =============================================================
# 2. FIND FIRST / LAST POSITION (LC 34)
# =============================================================

class FindFirstLast:
    """
    LC 34 — Find First and Last Position of Element
    Two binary searches: leftmost and rightmost occurrence.
    """
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        def find_left():
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = lo + (hi - lo) // 2
                if nums[mid] < target: lo = mid + 1
                else: hi = mid
            return lo

        def find_right():
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = lo + (hi - lo) // 2
                if nums[mid] <= target: lo = mid + 1
                else: hi = mid
            return lo - 1

        left = find_left()
        if left == len(nums) or nums[left] != target:
            return [-1, -1]
        return [left, find_right()]


# =============================================================
# 3. SEARCH IN ROTATED SORTED ARRAY (LC 33)
# =============================================================

class SearchRotated:
    """
    LC 33 — Search in Rotated Sorted Array
    Key insight: at least one half is always sorted.
    Check which half is sorted, then decide which half to search.
    """
    def search(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:            # left half is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                                # right half is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1


# =============================================================
# 4. FIND MINIMUM IN ROTATED SORTED ARRAY (LC 153)
# =============================================================

class FindMin:
    """
    LC 153 — Find Minimum in Rotated Sorted Array
    The minimum is always in the unsorted half.
    If nums[mid] > nums[hi] → min is in right half.
    """
    def findMin(self, nums: list[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1    # min is right of mid
            else:
                hi = mid        # mid could be the min
        return nums[lo]


# =============================================================
# 5. SEARCH A 2D MATRIX (LC 74)
# =============================================================

class SearchMatrix:
    """
    LC 74 — Search a 2D Matrix (rows and columns sorted)
    Map 1D index → 2D: row = idx // cols, col = idx % cols
    """
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])
        lo, hi = 0, rows * cols - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            val = matrix[mid // cols][mid % cols]
            if val == target:   return True
            elif val < target:  lo = mid + 1
            else:               hi = mid - 1
        return False


# =============================================================
# 6. BINARY SEARCH ON ANSWER (LC 875, 410)
# =============================================================

class KokoEatingBananas:
    """
    LC 875 — Koko Eating Bananas
    Binary search on the answer space [1, max(piles)].
    Ask: "Can Koko finish all piles at speed k within h hours?"
    """
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        import math
        lo, hi = 1, max(piles)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            hours_needed = sum(math.ceil(p / mid) for p in piles)
            if hours_needed <= h:
                hi = mid         # mid is feasible, try lower
            else:
                lo = mid + 1     # too slow
        return lo


class SplitArrayLargestSum:
    """
    LC 410 — Split Array Largest Sum
    Binary search on answer [max(nums), sum(nums)].
    Check: can we split into at most m subarrays with max sum <= mid?
    """
    def splitArray(self, nums: list[int], m: int) -> int:
        def feasible(max_sum):
            parts, curr = 1, 0
            for n in nums:
                if curr + n > max_sum:
                    parts += 1
                    curr = 0
                curr += n
            return parts <= m

        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


# =============================================================
# 7. PATTERN SUMMARY
# =============================================================
#
# Signal                              → Binary Search variant
# ──────────────────────────────────────────────────────────────
# Exact target in sorted array        → classic lo <= hi, return mid
# Leftmost / rightmost position       → separate left / right searches
# Rotated sorted array                → check which half is sorted
# Minimum in rotated array            → compare mid vs hi
# 2D sorted matrix                    → map to 1D index
# "Minimum max" / "Maximum min"        → binary search on answer space
# Condition: "is X feasible?"         → feasibility function as predicate
#
# Boundary conditions:
#   [lo, hi]  → while lo <= hi  / return lo or -1   (inclusive on both ends)
#   [lo, hi)  → while lo < hi   / return lo          (left-inclusive)
