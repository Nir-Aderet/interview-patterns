/*
Hexadecimal Literal: Prefix the value with 0x or 0X.
Binary Literal: Prefix the value with 0b or 0B
std::int32_t  s32 = -1'000'000;      // digit separator ' for readability

*/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

/*
| Old / Dangerous              | Modern / Safe                             |
| ---------------------------- | ----------------------------------------- |
| char buf[N] + strcpy/strncpy | std::string                               |
| Raw arrays int arr[N]        | std::array<int, N> or std::vector<int>    |
| new / delete                 | std::make_unique, std::make_shared        |
| int for sizes/indices        | std::size_t or static_cast<int>(v.size()) |
| NULL                         | nullptr                                   |
| C-style cast (int)x          | static_cast<int>(x)                       |
| Raw loop over container      | Range-based for                           |
| volatile int for concurrency | std::atomic<int>                          |
| #define MAX 100              | constexpr int MAX = 100;                  |
*/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

/*    USING
using creates a type alias — a new name for an existing type. It makes complex types readable and easier to change later.
using Graph = std::vector<std::vector<int>>;
using AdjList = std::unordered_map<int, std::vector<int>>;
This means: "wherever I write Graph, the compiler reads std::vector<std::vector<int>>." They are 100% identical — it is purely a readability tool.

If you later change the graph representation (e.g., to a map), you update one line instead of every function signature.
In C they used: typedef std::vector<std::vector<int>> Graph;  // old C style — avoid
*/

 /*    AUTO
Let the Compiler Deduce the Type, The type is still fully static and fixed at compile time
for (auto x : v)            std::cout << x << " ";   // x is int (copy)
for (auto& x : v)           x *= 2;                   // x is int& (modifies v)
for (const auto& x : v)     std::cout << x << " ";   // x is const int& (read-only, no copy)
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
// BAD - Signed/Unsigned Mismatch
std::vector<int> v = {1, 2, 3};
for (int i = 0; i <= v.size() - 1; ++i) {  // DANGER: if v is empty, v.size()-1 wraps to HUGE_NUMBER
    // Integer underflow on size_t (unsigned) when vector is empty causes loop to run 2^64 times.
}
// GOOD — cast size to signed, or use range-based for
for (int i = 0; i < static_cast<int>(v.size()); ++i) { /* safe */ }
for (const int x : v) { /* safest */ }

// BAD - Integer Overflow and Two's Complement
int8_t x = 127;
x += 1;       // overflow — undefined behavior for signed, wraps to -128 for int8_t

// GOOD
int16_t x = 127;
x += 1;       // 128 — fits

// Or use explicit check
if (x < std::numeric_limits<int8_t>::max()) x += 1;

// For embedded: always use fixed-width types and document value ranges
std::uint8_t voltage_8bit = 255;  // max voltage representation; don't add more
// Bug class: Two's complement wrap-around for signed types is undefined behavior in C++. For unsigned types, it wraps deterministically but is often a logic bug.

// BAD — silent truncation -> DATA LOSS !!!
uint32_t big = 0x1234'5678;
uint8_t  small = big;   // silently becomes 0x78 — data lost!

// GOOD — explicit cast + assertion/documentation
uint8_t small_safe = static_cast<uint8_t>(big & 0xFF);  // deliberate extraction
// In modern C++17, use if-constexpr or std::in_range (C++20)

// BAD
int* p = new int(42);
delete p;
std::cout << *p;   // USE AFTER FREE — undefined behavior

// BAD — double delete
delete p;   // double free — heap corruption

// GOOD — smart pointers make this impossible
auto p = std::make_unique<int>(42);
// p automatically freed when it goes out of scope
// Second access would require explicitly moving ownership

// BAD
const std::string& bad_ref() {
    std::string s = "hello";
    return s;   // s is destroyed when function returns — dangling reference!
}

// GOOD — return by value
std::string good() {
    return "hello";   // NRVO/move ensures this is efficient
}

// BAD — iterator invalidation in VECTOR !!!
std::vector<int> v = {1, 2, 3};
auto it = v.begin();
v.push_back(4);     // may reallocate! it is now dangling
std::cout << *it;   // undefined behavior

// GOOD — re-obtain iterator after modification, or use indices
v.push_back(4);
for (std::size_t i = 0; i < v.size(); ++i) { /* index stays valid */ }


#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <memory>
#include <algorithm>

/*
| Use Case                               | Reference T& | Pointer T*         | Reason                                            |
| -------------------------------------- | ------------ | ------------------ | ------------------------------------------------- |
| Read a large object without copying    | const T&     | —                  | Reference cannot be null; cleaner syntax          |
| Modify caller's variable               | T&           | T*                 | Both work; reference is cleaner if never null     |
| Optional parameter (might not exist)   | —            | T* (nullable)      | Reference cannot represent "nothing"              |
| Return multiple values from a function | T& out       | T* out             | Reference preferred if always valid               |
| Pointing into a dynamic data structure | —            | T*                 | Pointers can be re-seated; references cannot      |
| C API interop                          | —            | T*                 | C has no references                               |
| Array/buffer passed in                 | —            | T* buf, size_t len | Pointer + length is the C++ idiom for raw buffers |
| Re-pointing to a different object      | —            | T*                 | References cannot be re-seated after binding      |
*/
#include <iostream>
#include <string>
#include <vector>

class Inverter {
public:
    // --- 1. Pass by VALUE — small/trivial types, or when you need a local copy
    //        Cost: one copy of the argument is made, caller unchanged
    void set_id(int id) {
        id_ = id;   // int is cheap to copy — by-value is fine
    }
    // --- 2. Pass by CONST REFERENCE — large objects, read-only
    //        Cost: no copy; caller's object cannot be modified
    void log_name(const std::string& name) const {
        std::cout << name << "\n";   // reads name, never copies it
    }
    // --- 3. Pass by NON-CONST REFERENCE — large objects, modify caller's variable
    //        Cost: no copy; caller's object WILL be modified
    void append_log(std::string& log) {
        log += "[Inverter] ";        // modifies the caller's string directly
    }
    // --- 4. Pass by POINTER — optional parameters, arrays, C API interop
    //        Cost: no copy; can be nullptr
    void set_logger(std::ostream* out) {
        logger_ = out;               // store pointer; caller may pass nullptr
    }
    // --- 5. Pass by RVALUE REFERENCE (T&&) — take ownership of a temporary
    //        Cost: no copy; moves the resource (e.g., string buffer ownership)
    void set_name(std::string&& name) {
        name_ = std::move(name);     // steal name's internal buffer — no copy
    }
    // --- 6. CONST member function — guarantees this function does NOT modify the object
    //        Required when called on a const object
    int  get_id()   const { return id_; }
    bool is_active() const { return active_; }
    // --- 7. STATIC member function — belongs to the class, not an instance
    //        Has no 'this' pointer; accessed as Inverter::make_default()
    static Inverter make_default() {
        return Inverter();
    }
    // --- 8. [[nodiscard]] — compiler warns if return value is ignored
    //        Use for error codes and important return values
    [[nodiscard]] bool connect() {
        active_ = true;
        return true;   // warning if caller writes: inv.connect(); without using result
    }
private:
    int          id_     = 0;
    bool         active_ = false;
    std::string  name_;
    std::ostream* logger_ = nullptr;
};

int main6() {
    Inverter inv;
    inv.set_id(42);                     // by value
    inv.log_name("SE5000");             // const ref — no copy of string literal
    std::string log;
    inv.append_log(log);                // non-const ref — log is modified
    inv.set_logger(&std::cout);         // pointer — optional
    inv.set_name(std::string("Alpha")); // rvalue ref — string moved, not copied
    bool ok = inv.connect();            // [[nodiscard]] — result must be used
    auto inv2 = Inverter::make_default(); // static
}

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
