"""
=============================================================
  TREES — Binary Trees & BST Patterns
=============================================================

Pattern Recognition:
  - "binary tree" + depth/height/diameter → DFS post-order
  - "level order" / "by level" → BFS with a deque
  - "BST" + search/insert/validate → leverage sorted property
  - "lowest common ancestor" → DFS, check subtree membership
  - "serialize/deserialize" → BFS or pre-order DFS

Key Insight: Most tree problems = recursion on subtrees.
  "What information do I need from my children to answer this node?"
=============================================================
"""

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# =============================================================
# 1. DFS TRAVERSALS (Recursive & Iterative)
# =============================================================

def inorder(root: Optional[TreeNode]) -> list[int]:
    """Left → Root → Right. For BST: yields sorted order."""
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res


def inorder_iterative(root: Optional[TreeNode]) -> list[int]:
    """Iterative inorder — avoids recursion stack."""
    res, stack, curr = [], [], root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.val)
        curr = curr.right
    return res


def preorder(root: Optional[TreeNode]) -> list[int]:
    """Root → Left → Right. Good for serialization / copying."""
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)


def postorder(root: Optional[TreeNode]) -> list[int]:
    """Left → Right → Root. Good for deletion / aggregation from leaves."""
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


# =============================================================
# 2. BFS — LEVEL ORDER (LC 102)
# =============================================================

class LevelOrder:
    """
    LC 102 — Binary Tree Level Order Traversal
    Pattern: BFS with deque; process level by level.
    """
    def levelOrder(self, root: Optional[TreeNode]) -> list[list[int]]:
        if not root:
            return []
        res, queue = [], deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):   # snapshot current level size
                node = queue.popleft()
                level.append(node.val)
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)
            res.append(level)
        return res


# =============================================================
# 3. DEPTH / HEIGHT (LC 104, 111)
# =============================================================

class MaxDepth:
    """
    LC 104 — Maximum Depth of Binary Tree
    Post-order DFS: answer at node = 1 + max(left, right)
    """
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


class MinDepth:
    """
    LC 111 — Minimum Depth
    Special case: a node with only one child is NOT a leaf.
    """
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        if not root.left:   # only right child
            return 1 + self.minDepth(root.right)
        if not root.right:  # only left child
            return 1 + self.minDepth(root.left)
        return 1 + min(self.minDepth(root.left), self.minDepth(root.right))


# =============================================================
# 4. DIAMETER (LC 543)
# =============================================================

class Diameter:
    """
    LC 543 — Diameter of Binary Tree
    Diameter through a node = left_depth + right_depth.
    Carry a global max; return depth to parent.
    """
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.max_dia = 0
        def depth(node):
            if not node:
                return 0
            l, r = depth(node.left), depth(node.right)
            self.max_dia = max(self.max_dia, l + r)
            return 1 + max(l, r)
        depth(root)
        return self.max_dia


# =============================================================
# 5. BALANCED TREE (LC 110)
# =============================================================

class IsBalanced:
    """
    LC 110 — Balanced Binary Tree
    Return -1 as a sentinel if subtree is unbalanced.
    Avoids recomputing heights.
    """
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def height(node):
            if not node:
                return 0
            l, r = height(node.left), height(node.right)
            if l == -1 or r == -1 or abs(l - r) > 1:
                return -1    # propagate failure
            return 1 + max(l, r)
        return height(root) != -1


# =============================================================
# 6. INVERT TREE (LC 226)
# =============================================================

class InvertTree:
    """LC 226 — Invert Binary Tree. Classic recursion."""
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root


# =============================================================
# 7. SAME TREE / SYMMETRIC (LC 100, 101)
# =============================================================

class SameTree:
    """LC 100 — compare two trees node by node."""
    def isSameTree(self, p, q):
        if not p and not q: return True
        if not p or not q:  return False
        return p.val == q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


class IsSymmetric:
    """LC 101 — Symmetric Tree. Mirror DFS: left.left vs right.right."""
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def mirror(l, r):
            if not l and not r: return True
            if not l or not r:  return False
            return l.val == r.val and mirror(l.left, r.right) and mirror(l.right, r.left)
        return mirror(root.left, root.right)


# =============================================================
# 8. PATH SUM (LC 112, 113, 124)
# =============================================================

class PathSum:
    """LC 112 — Does any root-to-leaf path sum equal target?"""
    def hasPathSum(self, root, targetSum):
        if not root:
            return False
        if not root.left and not root.right:
            return root.val == targetSum   # leaf check
        return self.hasPathSum(root.left,  targetSum - root.val) or \
               self.hasPathSum(root.right, targetSum - root.val)


class MaxPathSum:
    """
    LC 124 — Binary Tree Maximum Path Sum
    Path can start and end anywhere. At each node:
      gain  = node.val + max(left_gain, 0) + max(right_gain, 0)
      return = node.val + max(left_gain, right_gain, 0)  ← only ONE branch up
    """
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float('-inf')
        def gain(node):
            if not node: return 0
            l = max(gain(node.left),  0)
            r = max(gain(node.right), 0)
            self.max_sum = max(self.max_sum, node.val + l + r)
            return node.val + max(l, r)   # only one arm goes upward
        gain(root)
        return self.max_sum


# =============================================================
# 9. LOWEST COMMON ANCESTOR (LC 236, 235)
# =============================================================

class LCA:
    """
    LC 236 — LCA of Binary Tree (not necessarily BST)
    If current node equals p or q, it's an ancestor.
    If both children return a node, current is the LCA.
    """
    def lowestCommonAncestor(self, root, p, q):
        if not root or root == p or root == q:
            return root
        left  = self.lowestCommonAncestor(root.left,  p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root    # p and q are in different subtrees
        return left or right


class LCA_BST:
    """
    LC 235 — LCA of BST
    BST property: if both p, q < node → go left. If both > node → go right.
    First split point is the LCA.
    """
    def lowestCommonAncestor(self, root, p, q):
        while root:
            if p.val < root.val and q.val < root.val:
                root = root.left
            elif p.val > root.val and q.val > root.val:
                root = root.right
            else:
                return root


# =============================================================
# 10. VALIDATE BST (LC 98)
# =============================================================

class ValidateBST:
    """
    LC 98 — Validate Binary Search Tree
    Pass down valid range [lo, hi] for each node.
    Avoids the classic mistake of only checking immediate children.
    """
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node, lo=float('-inf'), hi=float('inf')):
            if not node:
                return True
            if not (lo < node.val < hi):
                return False
            return validate(node.left, lo, node.val) and \
                   validate(node.right, node.val, hi)
        return validate(root)


# =============================================================
# 11. SERIALIZE / DESERIALIZE (LC 297)
# =============================================================

class Codec:
    """
    LC 297 — Serialize and Deserialize Binary Tree
    Pre-order DFS with 'N' as null marker.
    """
    def serialize(self, root) -> str:
        res = []
        def dfs(node):
            if not node:
                res.append('N')
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ','.join(res)

    def deserialize(self, data: str):
        vals = iter(data.split(','))
        def dfs():
            v = next(vals)
            if v == 'N':
                return None
            node = TreeNode(int(v))
            node.left  = dfs()
            node.right = dfs()
            return node
        return dfs()


# =============================================================
# 12. PATTERN SUMMARY
# =============================================================
#
# Signal                          → Approach
# ──────────────────────────────────────────────────────────
# Compute per-node value          → Post-order DFS (children first)
# Level-by-level output           → BFS with deque
# Root-to-leaf path               → DFS, carry running sum/path
# BST property                    → Leverage sorted order (no full search)
# Global max crossing root        → Track self.max in DFS, return single arm
# Two nodes' relationship         → LCA pattern
# Serialize / reconstruct         → Pre-order DFS with null markers
