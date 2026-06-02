# prefix sum
"""
For subarray sum equals K, use a dict from prefix_sum to count occurrences.
you can use 2 prefix, one form the start and another fom the end -> claculate the sum without
using / of the whole array excluding item i.
"""
def prefix_sum(arr):
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, left, right):
    # sum of arr[left:right+1]
    return prefix[right + 1] - prefix[left]

# Monotonic Stack
def next_greater_elements(nums):
    """
    Returns an array where ans[i] is the next greater element to the right of nums[i],
    or -1 if none.
    when you see a bigger value x, you can immediately resolve the next greater element for
    all smaller values on top of the stack (because you scan left → right, and x is the
    first such bigger value they see).
    Ask: “Do I want the next (or previous) greater or smaller value?”
    Greater ⇒ keep stack decreasing so a bigger value knocks out smaller ones.
    Smaller ⇒ keep stack increasing so a smaller value knocks out bigger ones.
    """
    n = len(nums)
    ans = [-1] * n
    stack = []  # stack of indices, monotonic decreasing by value

    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
          """
          As long as the current value x is greater than the value at the
          index on top of the stack, this x is the “next greater to the right” for that index.
          Pop that index idx and set ans[idx] = x.
          """
            idx = stack.pop()
            ans[idx] = x
        stack.append(i)

    return ans
