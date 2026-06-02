# In-Place linked list reversal
"""node = None
temp -> head.next -> node -> head-|
^--------------------------------/
"""
def reverse_linked_list(head):
    prev, curr = None, head

    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev  # new head

def reverse_between(head, m, n):
    if not head or m == n:
        return head

    dummy = ListNode(0, head)
    prev = dummy

    # 1) Move prev to node before position m
    for _ in range(m - 1):
        prev = prev.next

    # 2) Reverse sub-list of length (n - m + 1)
    sublist_tail = prev.next
    curr = sublist_tail
    prev_node = None
    for _ in range(n - m + 1):
        nxt = curr.next
        curr.next = prev_node
        prev_node = curr
        curr = nxt

    # 3) Reconnect
    prev.next = prev_node          # new head of sub-list
    sublist_tail.next = curr       # tail points to node after n

    return dummy.next

def reverse_k_group(head, k):
    if k <= 1 or not head:
        return head

    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # 1) Find kth node from group_prev
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next  # not enough nodes

        group_next = kth.next

        # 2) Reverse [group_prev.next, kth]
        prev, curr = group_next, group_prev.next
        for _ in range(k):
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # 3) Reconnect
        tmp = group_prev.next      # this becomes the tail of the reversed group
        group_prev.next = prev     # prev is new head of this group
        group_prev = tmp
