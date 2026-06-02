# two pointers
"""
When to use – signals
- Input is sorted or can be sorted without violating constraints.
- Problem talks about pairs/triples, sum to target,
removing duplicates, checking palindrome, or partitioning around a pivot.
- You’d otherwise use a double loop O(n^2) to find pair relationships.
"""
def two_pointers_sorted(arr, target):
    """
    Classic two-pointer template for sorted arrays.
    Returns True if there exists a pair with sum == target.
    """
    left, right = 0, len(arr) - 1

    while left < right:
        curr = arr[left] + arr[right]
        if curr == target:
            return True
        elif curr < target:
            left += 1  # need a bigger sum
        else:
            right -= 1  # need a smaller sum

    return False
