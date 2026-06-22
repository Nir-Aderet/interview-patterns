// Hash-Based Patterns
//  Recognize it when: you need O(1) lookup, counting frequencies, or grouping.


// Example: Two Sum (sorted input)
// Find two numbers in a sorted array that sum to target
#include <vector>
#include <iostream>

std::pair<int,int> two_sum_sorted(const std::vector<int>& nums, int target) {
    int left = 0, right = static_cast<int>(nums.size()) - 1;
    while (left < right) {
        int sum = nums[left] + nums[right];
        if (sum == target)  return {left, right};
        else if (sum < target) ++left;
        else                   --right;
    }
    return {-1, -1};  // not found
}

int main1() {
    std::vector<int> v = {1, 3, 5, 8, 11};
    auto [l, r] = two_sum_sorted(v, 9);        // structured bindings (C++17)
    std::cout << "Indices: " << l << ", " << r << "\n";  // 1, 3  (3+8=11? No: 1+8=9)
    return 0;
}

// Example: Longest substring without repeating characters
#include <string>
#include <unordered_map>
#include <iostream>

int length_of_longest_unique(const std::string& s) {
    std::unordered_map<char, int> last_seen;  // char -> last index
    int max_len = 0;
    int left = 0;

    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
        char c = s[right];
        if (last_seen.count(c) && last_seen[c] >= left) {
            left = last_seen[c] + 1;  // shrink window past duplicate
        }
        last_seen[c] = right;
        max_len = std::max(max_len, right - left + 1);
    }
    return max_len;
}

int main2() {
    std::cout << length_of_longest_unique("abcabcbb") << "\n";  // 3 ("abc")
    std::cout << length_of_longest_unique("pwwkew")   << "\n";  // 3 ("wke")
    return 0;
}


// Example: Group anagrams
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <iostream>

std::vector<std::vector<std::string>> group_anagrams(
    const std::vector<std::string>& words)
{
    std::unordered_map<std::string, std::vector<std::string>> groups;

    for (const std::string& w : words) {
        std::string key = w;
        std::sort(key.begin(), key.end());  // sorted word as key
        groups[key].push_back(w);
    }

    std::vector<std::vector<std::string>> result;
    for (auto& [key, group] : groups) {
        result.push_back(std::move(group));
    }
    return result;
}

int main3() {
    auto groups = group_anagrams({"eat", "tea", "tan", "ate", "nat", "bat"});
    for (const auto& g : groups) {
        for (const auto& w : g) std::cout << w << " ";
        std::cout << "\n";
    }
    return 0;
}

// DP
// Classic: Fibonacci with memoization
#include <vector>
#include <iostream>

int fib(int n) {
    if (n <= 1) return n;
    std::vector<int> dp(n + 1);
    dp[0] = 0; dp[1] = 1;
    for (int i = 2; i <= n; ++i)
        dp[i] = dp[i-1] + dp[i-2];
    return dp[n];
}

// Coin change — minimum coins for amount
int coin_change(const std::vector<int>& coins, int amount) {
    std::vector<int> dp(amount + 1, amount + 1);  // "infinity"
    dp[0] = 0;
    for (int i = 1; i <= amount; ++i) {
        for (int coin : coins) {
            if (coin <= i) dp[i] = std::min(dp[i], dp[i - coin] + 1);
        }
    }
    return (dp[amount] > amount) ? -1 : dp[amount];
}

int main4() {
    std::cout << fib(10) << "\n";                           // 55
    std::cout << coin_change({1, 5, 6, 9}, 11) << "\n";    // 2 (5+6)
    return 0;
}

// In real code, you bundle the cache and the function together so the caller never has to manage the cache manually.
// This is the OOP approach.

#include <unordered_map>
#include <iostream>

class FibSolver {
public:
    int compute(int n) {
        if (n <= 1) return n;

        auto it = cache_.find(n);
        if (it != cache_.end()) {
            return it->second;          // cache hit
        }

        int result = compute(n - 1) + compute(n - 2);
        cache_[n] = result;             // store
        return result;
    }

    void clear_cache() { cache_.clear(); }
    std::size_t cache_size() const { return cache_.size(); }

private:
    std::unordered_map<int, int> cache_;   // hidden from caller
};

int main5() {
    FibSolver solver;                       // cache lives inside the object

    std::cout << solver.compute(5)  << "\n";   // 5
    std::cout << solver.compute(10) << "\n";   // 55
    std::cout << solver.compute(5)  << "\n";   // instant — still cached

    std::cout << "Cache size: " << solver.cache_size() << "\n";  // 9 entries (2..10)
}
