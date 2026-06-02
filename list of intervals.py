# Merge / Overlapping Intervals
"""
Sort intervals by their start, then sweep left‑to‑right,
merging overlapping intervals into combined ranges;

When to use – signals
- Input is a list of intervals [start, end].
- Questions about merging overlapping meetings, counting rooms, or inserting a new interval.
- Words like “overlapping time intervals”, “meeting rooms”, or “calendar slots.”

"""
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            # Overlap: extend the last interval
            merged[-1][1] = max(last_end, end)
        else:
            # Disjoint: push new interval
            merged.append([start, end])

    return merged
