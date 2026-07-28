"""
=============================================================
  TWO POINTERS
=============================================================

Pattern Recognition:
  - "pair with target sum" in sorted array → converging pointers
  - "remove duplicates" / "move zeros" → slow/fast pointers
  - "container with most water" → converging pointers
  - "3Sum" / "4Sum" → fix one element + two pointers
  - "partition" → left/right pointers (Dutch flag)
  - String / array palindrome check → converging pointers

Distinction from Sliding Window:
  Two Pointers: left and right move toward each other (or independently).
  Sliding Window: both pointers move in the same direction to maintain a window.
=============================================================
"""


# =============================================================
# 1. TWO SUM II (LC 167) — SORTED ARRAY
# =============================================================

class TwoSumII:
    """
    LC 167 — Two Sum II (sorted input)
    Converging pointers: sum too big → move right in; sum too small → move left out.
    """
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        l, r = 0, len(numbers) - 1
        while l < r:
            s = numbers[l] + numbers[r]
            if s == target:   return [l + 1, r + 1]  # 1-indexed
            elif s < target:  l += 1
            else:             r -= 1
        return []


# =============================================================
# 2. 3SUM (LC 15)
# =============================================================

class ThreeSum:
    """
    LC 15 — 3Sum
    Sort, fix nums[i], then two-pointer for the pair.
    Skip duplicates at both i and l/r levels.
    """
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:  # skip duplicate i
                continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == 0:
                    res.append([nums[i], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l + 1]: l += 1
                    while l < r and nums[r] == nums[r - 1]: r -= 1
                    l += 1; r -= 1
                elif s < 0: l += 1
                else:       r -= 1
        return res


# =============================================================
# 3. CONTAINER WITH MOST WATER (LC 11)
# =============================================================

class ContainerWithMostWater:
    """
    LC 11 — Container With Most Water
    Greedy two-pointer: always move the shorter side inward.
    Moving the taller side inward cannot increase area.
    """
    def maxArea(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        max_water = 0
        while l < r:
            water = (r - l) * min(height[l], height[r])
            max_water = max(max_water, water)
            if height[l] < height[r]: l += 1
            else:                      r -= 1
        return max_water


# =============================================================
# 4. TRAPPING RAIN WATER (LC 42)
# =============================================================

class TrappingRainWater:
    """
    LC 42 — Trapping Rain Water
    Water at position i = min(max_left[i], max_right[i]) - height[i].
    Two-pointer: track running max_left and max_right.
    Move the side with the smaller max inward.
    """
    def trap(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        max_l = max_r = water = 0
        while l < r:
            if height[l] <= height[r]:
                max_l = max(max_l, height[l])
                water += max_l - height[l]
                l += 1
            else:
                max_r = max(max_r, height[r])
                water += max_r - height[r]
                r -= 1
        return water


# =============================================================
# 5. REMOVE DUPLICATES FROM SORTED ARRAY (LC 26)
# =============================================================

class RemoveDuplicates:
    """
    LC 26 — Remove Duplicates from Sorted Array
    Slow pointer k tracks the insert position.
    Fast pointer i scans for the next unique value.
    """
    def removeDuplicates(self, nums: list[int]) -> int:
        k = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                nums[k] = nums[i]
                k += 1
        return k


# =============================================================
# 6. DUTCH NATIONAL FLAG (LC 75)
# =============================================================

class SortColors:
    """
    LC 75 — Sort Colors (Dutch National Flag)
    Three pointers: lo (next 0 slot), mid (current), hi (next 2 slot).
    """
    def sortColors(self, nums: list[int]) -> None:
        lo, mid, hi = 0, 0, len(nums) - 1
        while mid <= hi:
            if nums[mid] == 0:
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1; mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1   # don't increment mid: newly swapped value is unchecked


# =============================================================
# 7. VALID PALINDROME (LC 125)
# =============================================================

class ValidPalindrome:
    """LC 125 — Valid Palindrome. Converging pointers, skip non-alphanumeric."""
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum(): l += 1
            while l < r and not s[r].isalnum(): r -= 1
            if s[l].lower() != s[r].lower(): return False
            l += 1; r -= 1
        return True


# =============================================================
# 8. PATTERN SUMMARY
# =============================================================
#
# Signal                          → Two Pointer variant
# ─────────────────────────────────────────────────────────
# Pair sum in sorted array        → converging (l=0, r=end)
# 3Sum / 4Sum                     → fix outer element + converging inner pair
# Max area / container            → converging, move shorter side
# Trap water                      → converging, move smaller max side
# In-place remove / compact       → slow/fast (k = write pointer)
# Partition 3 values              → Dutch flag (lo, mid, hi)
# Palindrome check                → converging with skip
