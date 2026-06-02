# sliding window
def sliding_window_template(nums, condition_fn):
    """
    Generic sliding window template.
    - nums: list or string-like (treat with indexing).
    - condition_fn(state) -> bool: returns True when window is 'valid'.
    """
    n = len(nums)
    left = 0
    best = None  # e.g., best length, best sum, etc.
    # Example of state: counts, current sum, etc.
    # Initialize whatever state you need.
    state = {}

    for right in range(n):
        # 1) Expand window to include nums[right]
        x = nums[right]
        # TODO: update state to include x

        # 2) Shrink from the left while the window violates constraints
        while left <= right and not condition_fn(state):
            y = nums[left]
            # TODO: update state to remove y
            left += 1

        # 3) Update best answer if window is valid
        if condition_fn(state):
            # Example: track max length
            window_len = right - left + 1
            # TODO: update best as needed
            # best = max(best, window_len) or similar

    return best
    
