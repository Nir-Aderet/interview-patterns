"""
=============================================================
  MATH & COMMON TRICKS
=============================================================

Pattern Recognition:
  - "reverse digits" / "palindrome number" → modulo + integer math
  - "fast power" / "x^n" → fast exponentiation (divide & conquer)
  - "count primes" → Sieve of Eratosthenes
  - "random pick / reservoir sampling" → math/probability
  - "geometry" / "points on a line" → slope as fraction (gcd normalization)
  - "modular arithmetic" → (a * b) % mod with large numbers

Key Formulas:
  Sum 1..n          = n*(n+1)//2
  Sum of squares    = n*(n+1)*(2n+1)//6
  GCD               = math.gcd(a, b)   (or Euclidean: while b: a,b = b,a%b)
  LCM               = a * b // gcd(a, b)
  Modular inverse   = pow(a, mod-2, mod)  [if mod is prime]
=============================================================
"""

import math
from collections import defaultdict


# =============================================================
# 1. PALINDROME NUMBER (LC 9)
# =============================================================

class PalindromeNumber:
    """
    LC 9 — Palindrome Number
    Reverse the second half of the number using modulo.
    No string conversion needed.
    """
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        rev = 0
        while x > rev:
            rev = rev * 10 + x % 10
            x //= 10
        return x == rev or x == rev // 10   # even / odd length


# =============================================================
# 2. FAST POWER (LC 50)
# =============================================================

class FastPower:
    """
    LC 50 — Pow(x, n)
    Divide & conquer: x^n = x^(n//2) * x^(n//2)  [* x if n is odd]
    Time: O(log n)
    """
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x, n = 1 / x, -n
        result = 1.0
        while n:
            if n & 1:            # n is odd
                result *= x
            x *= x               # square the base
            n >>= 1              # halve the exponent
        return result


# =============================================================
# 3. COUNT PRIMES — SIEVE OF ERATOSTHENES (LC 204)
# =============================================================

class CountPrimes:
    """
    LC 204 — Count Primes less than n
    Sieve: mark multiples of each prime as composite.
    Start marking from p^2 (smaller multiples already marked).
    Time: O(n log log n)  Space: O(n)
    """
    def countPrimes(self, n: int) -> int:
        if n < 2: return 0
        sieve = [True] * n
        sieve[0] = sieve[1] = False
        for p in range(2, int(n**0.5) + 1):
            if sieve[p]:
                for multiple in range(p * p, n, p):
                    sieve[multiple] = False
        return sum(sieve)


# =============================================================
# 4. MAX POINTS ON A LINE (LC 149)
# =============================================================

class MaxPointsOnLine:
    """
    LC 149 — Max Points on a Line
    For each anchor point, compute slope to every other point.
    Slope = (dy/gcd, dx/gcd) as a normalized fraction.
    Max frequency slope + 1 (the anchor itself) = max collinear points.
    """
    def maxPoints(self, points: list[list[int]]) -> int:
        if len(points) <= 2:
            return len(points)
        max_pts = 2
        for i in range(len(points)):
            slopes = defaultdict(int)
            for j in range(len(points)):
                if i == j: continue
                dy = points[j][1] - points[i][1]
                dx = points[j][0] - points[i][0]
                g  = math.gcd(abs(dy), abs(dx))
                if g != 0:
                    dy //= g
                    dx //= g
                if dx < 0:   # normalize sign
                    dy, dx = -dy, -dx
                elif dx == 0:
                    dy = abs(dy)
                slopes[(dy, dx)] += 1
            max_pts = max(max_pts, max(slopes.values()) + 1)
        return max_pts


# =============================================================
# 5. HAPPY NUMBER (LC 202)
# =============================================================

class HappyNumber:
    """
    LC 202 — Happy Number
    Replace n with sum of squares of its digits.
    Use Floyd's cycle detection or a seen-set to detect loops.
    """
    def isHappy(self, n: int) -> bool:
        def next_n(x):
            return sum(int(d)**2 for d in str(x))
        seen = set()
        while n != 1:
            if n in seen: return False
            seen.add(n)
            n = next_n(n)
        return True


# =============================================================
# 6. EXCEL COLUMN NUMBER (LC 171)
# =============================================================

class ExcelColumn:
    """
    LC 171 — Excel Sheet Column Number
    Base-26, but 'A' = 1 (not 0). Treat like a number system
    where A=1, B=2, ..., Z=26.
    """
    def titleToNumber(self, columnTitle: str) -> int:
        res = 0
        for ch in columnTitle:
            res = res * 26 + (ord(ch) - ord('A') + 1)
        return res


# =============================================================
# 7. MODULAR ARITHMETIC TEMPLATE
# =============================================================

def mod_example(a: int, b: int, mod: int) -> int:
    """
    Safely multiply large numbers under a modulus.
    (a * b) % mod  — Python handles big ints natively,
    but this pattern is expected in many contest problems.
    """
    return (a % mod) * (b % mod) % mod


def mod_pow(base: int, exp: int, mod: int) -> int:
    """Fast modular exponentiation: base^exp % mod in O(log exp)."""
    return pow(base, exp, mod)  # Python built-in handles this


# =============================================================
# 8. PATTERN SUMMARY
# =============================================================
#
# Problem signal                    → Math approach
# ──────────────────────────────────────────────────────────
# Reverse / palindrome number       → % 10 to extract digits, //10 to shrink
# x^n efficiently                   → fast power (binary exponentiation)
# Count primes up to n              → Sieve of Eratosthenes
# Collinear points                  → slope as (dy/gcd, dx/gcd) normalized fraction
# Large number % mod                → (a % mod * b % mod) % mod
# Modular inverse (mod is prime)    → pow(a, mod-2, mod)
# GCD                               → math.gcd(a, b)
# LCM                               → a * b // math.gcd(a, b)
# Sum 1..n                          → n*(n+1)//2  (O(1), avoid loops)
# Detect cycle in sequence          → Floyd's (slow/fast) or seen set
