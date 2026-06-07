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
# Top K Elements (Heaps)
"""
“Top K largest/smallest/frequent elements”, “Kth largest”, or similar ranking tasks.
O(n*log k): n times repositioning k elements while maintaining heap trait
largest -> min-heap, head is the smallest of the k largest numbers
smallest -> max-heap, head is the largest of the k smallest numbers

~ If the problem cares about uniqueness (e.g., “top K distinct elements”),
you may need a set or to deduplicate before/after the heap.
~ If it cares about original order, you might need to store (priority, index)
and sort or handle ties carefully after popping from the heap.
~ For “top K elements”, remember that the heap contents are in arbitrary order; if you need
them sorted, you must sort after extraction (or use nlargest/nsmallest which do this for you).
"""
import heapq

data = [5, 1, 3, 9, 2]
# Best Practice: In-place transformation in O(N)
heapq.heapify(data) 

"""
Safeguard Tuple Comparisons (Priority Queues)
Insert a unique, incrementing counter as a tie-breaker inside the tuple: (priority, count, task)
"""
# Counter acts as a tie-breaker and preserves insertion order
counter = 0
pq = []
# Push items: (priority, tie_breaker, data)
heapq.heappush(pq, (2, counter, Task("Low Priority")))
counter += 1
heapq.heappush(pq, (2, counter, Task("Same Priority, but Second")))
counter += 1

# Max heap - The value-negation method
max_heap = []
heapq.heappush(max_heap, -10)  # Pushing 10
heapq.heappush(max_heap, -30)  # Pushing 30

largest = -heapq.heappop(max_heap)  # Returns 30

heapq.heapreplace(heap, item)   # Pops the smallest element first, then pushes the new item.
heapq.heappushpop(heap, item)   # Pushes the new item first, then pops the smallest.

def top_k_largest(nums, k):
    """
    Returns the k largest elements in nums.
    """
    if k <= 0:
        return []
    # for k-th largest num
    """
    # Returns the k-th largest element in nums.
    if k <= 0 or k > len(nums):
        raise ValueError("k out of range")
    """

    
    # Min-heap of size k
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        else:
            if x > heap[0]:
                heapq.heapreplace(heap, x)
    # heap contains k largest, in arbitrary order
    return heap

    # return heap[0] # FOR The smallest in the heap is the k-th largest overall

def top_k_smallest(nums, k):
    """
    Returns the k smallest elements using a max-heap simulated with negatives.
    """
    if k <= 0:
        return []

    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, -x)  # store negative
        else:
            if x < -heap[0]:          # x is smaller than current largest of the small set
                heapq.heapreplace(heap, -x)

    # Convert back to positive values
    return [-v for v in heap]
