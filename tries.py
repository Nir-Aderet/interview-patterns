"""
=============================================================
  TRIES (PREFIX TREES)
=============================================================

Pattern Recognition:
  - "implement autocomplete" / "prefix search" → Trie
  - "word dictionary with wildcard '.'" → DFS on Trie nodes
  - "word search II" (find all words in grid) → Trie + DFS on grid
  - "count words with prefix" → Trie with prefix_count field

Core Structure:
  Each node has:
    children: dict[char → TrieNode]
    is_end: bool (marks end of a complete word)

Time Complexity:
  Insert / Search / StartsWith: O(L) where L = word length
  Space: O(ALPHABET_SIZE × N × L)
=============================================================
"""


# =============================================================
# 1. TRIE IMPLEMENTATION (LC 208)
# =============================================================

class TrieNode:
    def __init__(self):
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end: bool = False


class Trie:
    """
    LC 208 — Implement Trie (Prefix Tree)
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Returns True only if the FULL word is in the trie."""
        node = self._find_prefix_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        """Returns True if any word in the trie starts with prefix."""
        return self._find_prefix_node(prefix) is not None

    def _find_prefix_node(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node


# =============================================================
# 2. WORD DICTIONARY WITH WILDCARDS (LC 211)
# =============================================================

class WordDictionary:
    """
    LC 211 — Design Add and Search Words Data Structure
    '.' matches any single character → DFS through all children at that level.
    """
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return node.is_end
            ch = word[i]
            if ch == '.':
                return any(dfs(child, i + 1) for child in node.children.values())
            if ch not in node.children:
                return False
            return dfs(node.children[ch], i + 1)
        return dfs(self.root, 0)


# =============================================================
# 3. WORD SEARCH II (LC 212)
# =============================================================

class WordSearchII:
    """
    LC 212 — Word Search II
    Build a Trie from all words. DFS over the grid — follow Trie edges.
    Prune: remove completed words from Trie to avoid re-finding them.
    """
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        root = TrieNode()
        for word in words:            # build Trie
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end = word        # store word at leaf (not just True)

        rows, cols = len(board), len(board[0])
        res = []

        def dfs(node, r, c):
            ch = board[r][c]
            if ch not in node.children:
                return
            next_node = node.children[ch]
            if next_node.is_end:
                res.append(next_node.is_end)
                next_node.is_end = False   # don't find same word again

            board[r][c] = '#'   # mark visited
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                    dfs(next_node, nr, nc)
            board[r][c] = ch    # restore

            # Prune empty Trie branches
            if not next_node.children and not next_node.is_end:
                del node.children[ch]

        for r in range(rows):
            for c in range(cols):
                dfs(root, r, c)
        return res


# =============================================================
# 4. PATTERN SUMMARY
# =============================================================
#
# Use Trie when:
#   - Multiple prefix lookups on the same word set → O(L) each vs O(L*N) with list
#   - Wildcard / regex matching → DFS on Trie nodes
#   - Grid word search with many target words → Trie guides DFS pruning
#
# Alternative: use a sorted list + bisect for simple prefix lookups
#   (avoids Trie overhead when words fit in memory and patterns are simple)
