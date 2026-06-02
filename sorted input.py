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

# binary search
"""
Use binary search not only on arrays, but also on answer space or on specially
structured arrays (e.g., rotated arrays, first/last occurrence, duplicates) by
adjusting the condition under which you move left or right pointers.
"""
def first_occurrence(arr, target):
    left, right = 0, len(arr) - 1
    ans = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            ans = mid
            right = mid - 1  # keep searching left side
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return ans
def binary_search_answer(low, high, feasible):
    """
    Find minimum x in [low, high] such that feasible(x) is True,
    assuming feasibility is monotonic.
    """
    ans = None
    while low <= high:
        mid = (low + high) // 2
        if feasible(mid):
            ans = mid
            high = mid - 1  # try to find smaller feasible
        else:
            low = mid + 1
    return ans
