"""
=============================================================
  HEAPS & PRIORITY QUEUES
=============================================================

Python: heapq is a MIN-heap by default.
  Max-heap trick: push/pop NEGATIVE values.

Pattern Recognition:
  - "Kth largest / smallest" → heap of size K
  - "top K frequent" → heap on frequencies
  - "running median" → two heaps (max-heap + min-heap)
  - "merge K sorted lists" → heap on (val, list_index)
  - "task scheduling" → greedy + heap
=============================================================
"""

import heapq
from collections import Counter
from typing import Optional


# =============================================================
# 1. KTH LARGEST ELEMENT (LC 215)
# =============================================================

class KthLargest:
    """
    LC 215 — Kth Largest Element in an Array
    Maintain a min-heap of size K.
    Root of heap = Kth largest (all K-1 larger elements are also in the heap above it).
    Time: O(n log k)  Space: O(k)
    """
    def findKthLargest(self, nums: list[int], k: int) -> int:
        heap = []
        for n in nums:
            heapq.heappush(heap, n)
            if len(heap) > k:
                heapq.heappop(heap)  # evict smallest → keeps top-K
        return heap[0]               # root = Kth largest


# =============================================================
# 2. TOP K FREQUENT ELEMENTS (LC 347)
# =============================================================

class TopKFrequent:
    """
    LC 347 — Top K Frequent Elements
    Count frequencies, then use a min-heap of size K on (freq, element).
    Alternative: bucket sort by frequency → O(n)
    """
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        freq = Counter(nums)
        # nlargest internally uses a heap → O(n log k)
        return [item for item, _ in heapq.nlargest(k, freq.items(), key=lambda x: x[1])]


# =============================================================
# 3. FIND MEDIAN FROM DATA STREAM (LC 295)
# =============================================================

class MedianFinder:
    """
    LC 295 — Find Median from Data Stream
    Two heaps:
      lo = max-heap (stores lower half)  → negate for Python
      hi = min-heap (stores upper half)
    Invariant: len(lo) == len(hi) or len(lo) == len(hi) + 1
    """
    def __init__(self):
        self.lo = []  # max-heap (negated)
        self.hi = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)          # push to max-heap
        # balance: lo's max must be <= hi's min
        if self.lo and self.hi and (-self.lo[0]) > self.hi[0]:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # size balance: lo can have at most 1 extra
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0


# =============================================================
# 4. MERGE K SORTED LISTS (LC 23)
# =============================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class MergeKSortedLists:
    """
    LC 23 — Merge K Sorted Lists
    Push (node.val, index, node) into heap.
    Index breaks ties without comparing ListNode objects.
    Time: O(n log k) where n = total nodes
    """
    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))

        dummy = ListNode(0)
        curr = dummy
        while heap:
            val, i, node = heapq.heappop(heap)
            curr.next = node
            curr = curr.next
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next


# =============================================================
# 5. TASK SCHEDULER (LC 621)
# =============================================================

class TaskScheduler:
    """
    LC 621 — Task Scheduler
    Greedy: always pick the most frequent remaining task.
    Use a max-heap on (-count, task).
    Use a cooldown queue of (available_time, count, task).
    """
    def leastInterval(self, tasks: list[str], n: int) -> int:
        freq = Counter(tasks)
        max_heap = [(-cnt, task) for task, cnt in freq.items()]
        heapq.heapify(max_heap)

        time = 0
        cooldown = []  # (available_at, -remaining_count, task)

        while max_heap or cooldown:
            time += 1
            if max_heap:
                cnt, task = heapq.heappop(max_heap)
                cnt += 1                  # decrement count (negated)
                if cnt < 0:
                    cooldown.append((time + n, cnt, task))
            # Release tasks whose cooldown has expired
            if cooldown and cooldown[0][0] == time:
                _, cnt, task = heapq.heappop(cooldown)
                heapq.heappush(max_heap, (cnt, task))
        return time


# =============================================================
# 6. PATTERN SUMMARY
# =============================================================
#
# Signal                        → Heap pattern
# ─────────────────────────────────────────────────────────
# Kth largest                   → min-heap size K
# Kth smallest                  → max-heap size K (negate)
# Top-K frequent                → heap on (freq, element)
# Running median                → two heaps (lo max + hi min)
# Merge K sorted                → heap of (val, list_idx, node)
# Greedy scheduling             → max-heap + cooldown queue
# Sliding window max            → use monotonic deque instead
#
# Python heapq cheatsheet:
#   heapq.heappush(h, x)         push x
#   heapq.heappop(h)             pop smallest
#   heapq.heappushpop(h, x)      push then pop (faster than separate calls)
#   heapq.nlargest(k, iterable)  top-K largest
#   heapq.nsmallest(k, iterable) top-K smallest
#   Max-heap: push -x, pop and negate result
