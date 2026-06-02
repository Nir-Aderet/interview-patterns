# Fast & Slow Pointers 
"""
When to use – signals
- Linked list problems asking for cycle detection, cycle start, or middle node.
- Problems involving sequences where you
repeatedly apply a function and need to detect repetition (e.g., “Happy Number”).

! For “find cycle start”, once they meet, reset one pointer to head and
advance both by one until they meet again.

Pitfalls: wrong pointer initialization (e.g., starting fast at head.next without reasoning),
forgetting to handle empty or one‑node lists.
"""
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt

def has_cycle(head):
    slow, fast = head, head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True

    return False
