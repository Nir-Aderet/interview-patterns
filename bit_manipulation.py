"""
=============================================================
  BIT MANIPULATION
=============================================================

Essential Operations:
  n & (n-1)     → clears the lowest set bit (count bits, check power of 2)
  n & (-n)      → isolates the lowest set bit
  n ^ n = 0     → XOR with itself = 0  (find single number)
  n ^ 0 = n     → XOR with 0 = identity
  n >> 1        → divide by 2
  n << 1        → multiply by 2
  ~n            → bitwise NOT (= -(n+1) in Python)
  n & 1         → check if odd
  n | (1 << k)  → set bit k
  n & ~(1<<k)   → clear bit k
  n ^ (1 << k)  → flip bit k

Python Note:
  Python integers are arbitrary precision — no fixed 32/64-bit overflow.
  For 32-bit problems, mask with: n & 0xFFFFFFFF
=============================================================
"""


# =============================================================
# 1. SINGLE NUMBER (LC 136)
# =============================================================

class SingleNumber:
    """
    LC 136 — Single Number (all others appear twice)
    XOR all numbers. Pairs cancel out (a ^ a = 0).
    What remains is the single number.
    """
    def singleNumber(self, nums: list[int]) -> int:
        res = 0
        for n in nums:
            res ^= n
        return res


# =============================================================
# 2. NUMBER OF 1 BITS (LC 191)
# =============================================================

class HammingWeight:
    """
    LC 191 — Number of 1 Bits
    n & (n-1) clears the lowest set bit.
    Count how many times until n == 0.
    """
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1   # clears lowest set bit
            count += 1
        return count


# =============================================================
# 3. COUNTING BITS (LC 338)
# =============================================================

class CountingBits:
    """
    LC 338 — Counting Bits (count 1-bits for 0..n)
    DP: dp[i] = dp[i >> 1] + (i & 1)
    Shifting right drops the last bit; (i & 1) adds it back if set.
    """
    def countBits(self, n: int) -> list[int]:
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp


# =============================================================
# 4. MISSING NUMBER (LC 268)
# =============================================================

class MissingNumber:
    """
    LC 268 — Missing Number (0..n with one missing)
    XOR all indices and all values. Pairs cancel; missing index remains.
    Alternatively: expected_sum - actual_sum.
    """
    def missingNumber(self, nums: list[int]) -> int:
        res = len(nums)
        for i, n in enumerate(nums):
            res ^= i ^ n
        return res


# =============================================================
# 5. POWER OF TWO (LC 231)
# =============================================================

class PowerOfTwo:
    """
    LC 231 — Power of Two
    A power of two has exactly one set bit.
    n & (n-1) clears that bit → result is 0.
    """
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0


# =============================================================
# 6. SUM OF TWO INTEGERS WITHOUT + (LC 371)
# =============================================================

class GetSum:
    """
    LC 371 — Sum of Two Integers (no + or -)
    XOR gives sum without carry.
    AND << 1 gives the carry.
    Repeat until no carry. Mask to 32-bit for signed handling.
    """
    def getSum(self, a: int, b: int) -> int:
        MASK = 0xFFFFFFFF
        MAX  = 0x7FFFFFFF
        while b & MASK:
            carry = (a & b) << 1
            a = (a ^ b) & MASK
            b = carry & MASK
        return a if a <= MAX else ~(a ^ MASK)


# =============================================================
# 7. REVERSE BITS (LC 190)
# =============================================================

class ReverseBits:
    """
    LC 190 — Reverse Bits
    Iterate 32 times: extract LSB, shift into result.
    """
    def reverseBits(self, n: int) -> int:
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)
            n >>= 1
        return res


# =============================================================
# 8. PATTERN SUMMARY
# =============================================================
#
# Goal                              → Bit trick
# ──────────────────────────────────────────────────────────
# Find single element (pairs exist) → XOR all elements
# Count set bits                    → n & (n-1) loop
# Is power of two?                  → n > 0 and (n & (n-1)) == 0
# Isolate lowest set bit            → n & (-n)
# Clear lowest set bit              → n & (n - 1)
# Check bit k                       → (n >> k) & 1
# Set bit k                         → n | (1 << k)
# Clear bit k                       → n & ~(1 << k)
# Flip bit k                        → n ^ (1 << k)
# Add without +                     → XOR + carry loop + 32-bit mask
# Count bits for range [0..n]       → DP: dp[i] = dp[i>>1] + (i&1)
