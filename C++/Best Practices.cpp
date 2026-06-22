/*    USING
using creates a type alias — a new name for an existing type. It makes complex types readable and easier to change later.
using Graph = std::vector<std::vector<int>>;
This means: "wherever I write Graph, the compiler reads std::vector<std::vector<int>>." They are 100% identical — it is purely a readability tool.

If you later change the graph representation (e.g., to a map), you update one line instead of every function signature.
In C they used: typedef std::vector<std::vector<int>> Graph;  // old C style — avoid
*/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/*    QUEUE
 std::queue<int> q;
| Method    | Does                   | Returns                    |
| --------- | ---------------------- | -------------------------- |
| q.front() | Peeks at front element | The element (by reference) |
| q.back()  | Peeks at last element  | The element (by reference) |
| q.pop()   | Removes front element  | void — nothing             |
| q.push(x) | Adds element to back   | void                       |
| q.empty() | Checks if empty        | bool                       |
| q.size()  | Number of elements     | std::size_t                |
*/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/*    STATIC
If you want the function to cache results across calls, declare dp as static.
A static local variable is initialized once and persists for the entire program lifetime.

!!!! NOT THREAD-SAFE !!!!

int fib(int n) {
    static std::vector<int> cache = {0, 1};  // initialized ONCE, persists forever

    // Extend cache only if needed
    while (static_cast<int>(cache.size()) <= n) {
        int sz = cache.size();
        cache.push_back(cache[sz-1] + cache[sz-2]);
    }
    return cache[n];
}
External cache passed in
The external cache pattern is the cleanest for real code:
int fib(int n, std::vector<int>& cache) {
    if (n < static_cast<int>(cache.size())) return cache[n];
    // ... compute and store
}
*/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <memory>
#include <algorithm>

// Reserve to avoid reallocations (important for performance)
std::vector<int> big;
big.reserve(1000);   // allocates memory upfront

struct Motor {
    Motor(int id) : id_(id) { std::cout << "Motor " << id_ << " ON\n"; }
    ~Motor()               { std::cout << "Motor " << id_ << " OFF\n"; }
    int id_;
};

int main1() {
    auto m = std::make_unique<Motor>(42);  // heap allocation, RAII
    std::cout << m->id_ << "\n";
    // ~Motor() called automatically here — no delete needed
    return 0;
}
auto a = std::make_shared<Motor>(1);
auto b = a;          // both own the Motor; ref count = 2
a.reset();           // ref count = 1; Motor still alive
b.reset();           // ref count = 0; Motor destroyed

template <typename T>
T clamp(T val, T lo, T hi)  // clamp return type T, and recieves 3 parameters of type T
// this way one signeture can handle multiple types that support it's inner logic
{
    if (val < lo) return lo;
    if (val > hi) return hi;
    return val;
}

int main2() {
    std::cout << clamp(5, 0, 10)       << "\n";   // 5
    std::cout << clamp(15, 0, 10)      << "\n";   // 10
    std::cout << clamp(3.5, 0.0, 5.0)  << "\n";   // 3.5
}

// Pass by value (copy) — use for small/cheap types
int square(int n) { return n * n; }

// Pass by const reference — use for large objects (no copy, no modify)
void print_vec(const std::vector<int>& v) {
    for (int x : v) std::cout << x << " ";
    std::cout << "\n";
}

// Pass by reference — use to modify caller's variable
void double_all(std::vector<int>& v) {
    for (int& x : v) x *= 2;
}

// Return by value — modern C++ uses NRVO, no performance penalty
std::vector<int> make_vec(int n) {
    std::vector<int> result;
    for (int i = 0; i < n; ++i) result.push_back(i);
    return result;  // move semantics handle this efficiently
}

int x = 10;
int& ref = x;   // ref IS x
ref = 20;       // x is now 20

// Prefer references in function signatures to avoid null checks:
void increment(int& val) { ++val; }  // modifies caller's variable

int x = 10;
int* ptr = &x;  // ptr holds the address of x
*ptr = 20;      // dereference: change x through ptr
ptr = nullptr;  // safe null

// Pointer arithmetic (common in embedded)
int arr[3] = {1, 2, 3};
int* p = arr;
std::cout << *(p + 1);  // prints 2

// Value semantics (default)
std::vector<int> a = {1, 2, 3};
std::vector<int> b = a;  // b is a COPY of a
b.push_back(4);
// a still has 3 elements; b has 4

// Reference semantics (opt-in)
std::vector<int>& c = a;  // c is an alias for a
c.push_back(99);
// a now also has 99 — same object!

void example() {
    int x = 5;              // STACK — automatic, fast
    int* p = new int(5);    // HEAP — manual
    delete p;               // must free or it leaks
    p = nullptr;            // best practice: null after delete
}

// STRING

std::string s = "Hello, SolarEdge!";

std::cout << s.size()         << "\n";   // 17
std::cout << s.substr(7, 9)   << "\n";   // "SolarEdge"
std::cout << s.find("Solar")  << "\n";   // 7 (index)

s += " :)";                               // concatenate
s.replace(0, 5, "Hi");                   // replace "Hello" → "Hi"

// Convert to C string (needed for legacy APIs)
const char* cstr = s.c_str();

// Check if contains
if (s.find("Solar") != std::string::npos) {
    std::cout << "Found!\n";
}


// unordered_map

// Interview note: [] operator on unordered_map inserts a default value if the key doesn't exist.
// Always use .count() or .find() first to check.
