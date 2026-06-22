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

int main() {
    auto groups = group_anagrams({"eat", "tea", "tan", "ate", "nat", "bat"});
    for (const auto& g : groups) {
        for (const auto& w : g) std::cout << w << " ";
        std::cout << "\n";
    }
    return 0;
}
