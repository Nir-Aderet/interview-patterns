// Binary tree DFS and BFS
#include <queue>
#include <vector>
#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left  = nullptr;
    TreeNode* right = nullptr;
    TreeNode(int v) : val(v) {}
};

// DFS — recursive inorder traversal
void inorder(TreeNode* root, std::vector<int>& result) {
    if (!root) return;
    inorder(root->left, result);
    result.push_back(root->val);
    inorder(root->right, result);
}

// BFS — level-order using a queue
std::vector<std::vector<int>> level_order(TreeNode* root) {
    std::vector<std::vector<int>> levels;
    if (!root) return levels;

    std::queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {
        int sz = q.size();
        std::vector<int> level;
        for (int i = 0; i < sz; ++i) {
            TreeNode* node = q.front(); q.pop();
            level.push_back(node->val);
            if (node->left)  q.push(node->left);
            if (node->right) q.push(node->right);
        }
        levels.push_back(level);
    }
    return levels;
}

int main() {
    //       1
    //      / \
    //     2   3
    TreeNode* root = new TreeNode(1);
    root->left  = new TreeNode(2);
    root->right = new TreeNode(3);

    std::vector<int> inorder_result;
    inorder(root, inorder_result);
    for (int x : inorder_result) std::cout << x << " ";  // 2 1 3
    std::cout << "\n";

    // Memory: in a real program use unique_ptr for tree nodes
    delete root->left; delete root->right; delete root;
    return 0;
}
