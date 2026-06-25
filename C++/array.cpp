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
// STRING
// a vector<char> with extra string-specific methods
// strings ≤15 chars are stored in the object itself (no heap allocation)

std::string s = "Hello, SolarEdge!";

std::cout << s.size()         << "\n";   // 17
std::cout << s.substr(7, 9)   << "\n";   // "SolarEdge"
std::cout << s.find("Solar")  << "\n";   // 7 (index)
// SEARCH — returns index or std::string::npos if not found
std::size_t pos = s.find("Solar");
if (pos != std::string::npos) {
    std::cout << "Found at " << pos << "\n";  // 7
}
// SUBSTRING — substr(start_index, length)
std::cout << s.substr(7, 9) << "\n";  // "SolarEdge"
std::cout << s.substr(7)    << "\n";  // "SolarEdge!" — to end

// CONCATENATION
s += " :)";                           // append in-place — most efficient
s.append(" more");                    // same as +=
std::string s2 = s + " extra";        // creates a NEW string — allocation

// REPLACE — replace(start, length, new_string)
s.replace(0, 5, "Hi");               // "Hi, SolarEdge! :) more"

// COMPARE
std::string a = "abc", b = "abc";
std::cout << (a == b) << "\n";        // 1 (true) — use == for equality
std::cout << a.compare(b) << "\n";    // 0 = equal, <0 = less, >0 = greater

// CONVERT
std::string num_str = std::to_string(42);     // int → string
int num = std::stoi("42");                     // string → int (throws if invalid)
double d = std::stod("3.14");                  // string → double

// Convert to C string (needed for legacy APIs)
const char* cstr = s.c_str();

// ARRAY !!!!
// Use when: Size is fixed at compile time, stack allocation is required (embedded, performance-critical)
std::array<int, 5> arr = {5, 3, 1, 4, 2};

std::cout << arr.size()  << "\n";   // 5 — compile-time known
std::cout << arr[0]      << "\n";   // 5 — unchecked, O(1)
std::cout << arr.at(0)   << "\n";   // 5 — bounds-checked, throws std::out_of_range
std::cout << arr.front() << "\n";   // 5 — first element
std::cout << arr.back()  << "\n";   // 2 — last element

std::sort(arr.begin(), arr.end());  // sort in-place: {1,2,3,4,5}
std::fill(arr.begin(), arr.end(), 0);  // fill all with 0

// PAIR & TUPEL
#include <utility>   // std::pair
#include <tuple>     // std::tuple
#include <iostream>

// PAIR — two values of potentially different types
std::pair<std::string, int> device = {"inverter_A", 5000};
std::cout << device.first  << "\n";  // "inverter_A"
std::cout << device.second << "\n";  // 5000

auto d2 = std::make_pair("inverter_B", 3000);  // type deduced

// Structured binding (C++17) — unpack pair into named variables
auto [name, watts] = device;
std::cout << name << " " << watts << "\n";

// TUPLE — N values of potentially different types
auto record = std::make_tuple(1, "SE5000", 5000.0f);
auto [id, model, power] = record;    // structured binding
std::cout << id << " " << model << " " << power << "\n";

// Old way (C++14 and before)
std::cout << std::get<0>(record) << "\n";  // 1
std::cout << std::get<1>(record) << "\n";  // "SE5000"

// std::unordered_map and std::unordered_set — Hash Tables
/* Under the hood: An array of buckets. 
Each key is hashed → mapped to a bucket index → stored in that bucket (as a linked list for collision handling).
Average O(1) for insert/find/erase. 
Worst case O(n) when many keys hash to the same bucket (rare with good hash functions).
*/
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <iostream>

std::unordered_map<std::string, int> watts;

// INSERT — three equivalent ways
watts["inverter_A"] = 5000;                      // operator[] — inserts if missing!
watts.insert({"inverter_B", 3000});              // insert pair
watts.emplace("inverter_C", 2000);               // construct in-place (most efficient)

// FIND — ALWAYS prefer find() over [] for lookups
auto it = watts.find("inverter_A");
if (it != watts.end()) {
    std::cout << it->first << ": " << it->second << "\n";  // key: value
}

// COUNT — returns 0 or 1 (map has unique keys)
if (watts.count("inverter_D") == 0) {
    std::cout << "Not found\n";
}

// ERASE
watts.erase("inverter_C");

// ITERATE — order is NOT guaranteed (hash table = unordered)
for (const auto& [key, val] : watts) {
    std::cout << key << " = " << val << "\n";
}

// UNORDERED_SET — same hash table, but stores only keys (no values)
std::unordered_set<int> seen;
seen.insert(1); seen.insert(2); seen.insert(1);  // duplicates ignored
std::cout << seen.size() << "\n";                 // 2

// MAP & SET
/* Under the hood: Self-balancing binary search tree (red-black tree). Keys are always sorted. Every operation traverses O(log n) tree levels.

Operation	                Time
insert / erase / find	    O(log n)
Iteration (sorted order)	O(n)
lower_bound / upper_bound	O(log n)

Use map/set over unordered_map/unordered_set when:
- You need sorted iteration
- You need lower_bound / upper_bound (range queries)
- Key type has no hash function
*/
#include <map>
#include <set>
#include <iostream>

std::map<int, std::string> id_to_name;
id_to_name[3] = "C";
id_to_name[1] = "A";
id_to_name[2] = "B";

// Iterates in SORTED key order: 1, 2, 3
for (const auto& [id, name] : id_to_name) {
    std::cout << id << ": " << name << "\n";
}

// lower_bound: first key >= 2
auto it = id_to_name.lower_bound(2);
std::cout << it->first << "\n";  // 2

std::set<int> s = {5, 1, 3, 1, 4};  // duplicates removed, sorted
for (int x : s) std::cout << x << " ";  // 1 3 4 5
