# bfs
"""
Explore a graph or tree level by level using a queue,
ideal for shortest path in **unweighted** graphs or grids and level‑order traversals.
Level order traversal
"""

from collections import deque

def bfs(start, neighbors_fn):
    """
    Generic BFS.
    - start: starting node/state.
    - neighbors_fn(node) -> iterable of neighbors.
    """
    visited = {start}
    queue = deque([(start, 0)])  # (node, distance)

    while queue:
        node, dist = queue.popleft()
        # TODO: process node (e.g., check goal, collect result)

        for nei in neighbors_fn(node):
            if nei not in visited:
                visited.add(nei)
                queue.append((nei, dist + 1))



  # dfs
"""
“All paths” problems, backtracking, or problems that naturally
decompose recursively on trees/graphs.
Tree problems asking to compute sums, depths, or collect root‑to‑leaf paths.
"""
  def dfs_paths(root):
    """
    Collect all root-to-leaf paths in a ***binary tree***.
    """
    res = []

    def dfs(node, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right:
            res.append(list(path))
        else:
            dfs(node.left, path)
            dfs(node.right, path)
        path.pop()  # backtrack

    dfs(root, [])
    return res
  
def DFS(graph: dict[int,list[int]], start_vertex: int) -> :
  	visited = set(start_vertex)
  	stack = [start_vertex]
  	
  	while stack:
  		current_vertex = stack.pop()
  		visited.add(current_vertex)
  		for vertex in graph[current_vertex]:
  			if vertex not in visited:
  				stack.append(vertex)
  	return visited

  
# Binary tree traversals
"""
inorder: left - current node action - right
preorder: current node action - left - right
postorder: left - right - current node action
"""
def inorder(root):
    if not root:
        return
    inorder(root.left)
    # visit root.val
    inorder(root.right)

def preorder(root):
    if not root:
        return
    # visit root.val
    preorder(root.left)
    preorder(root.right)

def postorder(root):
    if not root:
        return
    postorder(root.left)
    postorder(root.right)
    # visit root.val
