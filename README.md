# 🧠 Interview Patterns — Python

A self-study reference for mastering coding interview patterns. Each file covers one pattern: when to recognize it, how to approach it, and annotated code examples mapped to LeetCode problems.

## Files

| File | Pattern | Key LeetCode Problems |
|------|---------|----------------------|
| `array.py` | Prefix sums, Kadane's, hashing | 53, 560, 238 |
| `continuous subarray-substring.py` | Sliding window | 3, 76, 424 |
| `sorted input.py` | Two pointers on sorted input | 167, 15, 42 |
| `two_pointers.py` | Two pointers (general) | 11, 125, 977 |
| `binary_search.py` | Binary search patterns | 704, 33, 153, 410 |
| `Linked list.py` | Linked list manipulation | 206, 21, 141 |
| `find cycles, repetitions, midpoint.py` | Floyd's cycle / slow-fast pointers | 142, 287 |
| `list of intervals.py` | Interval merging & overlap | 56, 57, 435 |
| `graphs-grids.py` | BFS / DFS on graphs & grids | 200, 207, 994 |
| `trees.py` | Binary trees & BST patterns | 104, 226, 98, 235 |
| `heaps_priority_queues.py` | Heap / priority queue patterns | 215, 295, 23, 355 |
| `stack_queue.py` | Stack & monotonic stack | 20, 84, 739, 232 |
| `backtracking.py` | Backtracking & constraint search | 46, 78, 131, 51 |
| `tries.py` | Trie (prefix tree) | 208, 211, 212 |
| `dynamic_programming.py` | All DP patterns | 70, 322, 1143, 140 |
| `bit_manipulation.py` | Bit tricks | 136, 191, 268, 338 |
| `math_and_tricks.py` | Math, modular arithmetic, geometry | 9, 50, 204, 149 |

## Pattern Recognition Cheat Sheet

```
Input signal                          → Pattern to reach for
─────────────────────────────────────────────────────────────
Sorted array / sorted 2 arrays        → Binary search / two pointers
Subarray / substring (contiguous)     → Sliding window
All permutations / combinations       → Backtracking
Shortest path / levels in graph       → BFS
Explore all paths / connected regions → DFS
Top-K / running median                → Heap
Overlapping subproblems               → Dynamic programming
Prefix / balance tracking             → HashMap + prefix
Valid parentheses / next greater      → Stack (monotonic)
Word prefix / autocomplete            → Trie
XOR / bit counting                    → Bit manipulation
Linked list cycle / midpoint          → Slow & fast pointers
```
