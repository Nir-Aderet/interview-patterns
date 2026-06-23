#include <string>
#include <iostream>

class Sensor {
public:
    // --- DEFAULT constructor (no arguments)
    Sensor() : id_(0), name_("unknown"), value_(0.0f) {
        std::cout << "Default Sensor created\n";
    }

    // --- PARAMETERIZED constructor with MEMBER INITIALIZER LIST
    //     Syntax: : member1_(arg1), member2_(arg2)
    //     This initializes members DIRECTLY — no default construction first.
    //     Without the list, name_ would be default-constructed to "" THEN assigned "new name"
    //     — that's two operations (double-initialization). The list does it in ONE step.
    Sensor(int id, std::string name, float val)
        : id_(id)                    // direct-initialize id_ with id
        , name_(std::move(name))     // move name into name_ — no copy
        , value_(val)                // direct-initialize value_ with val
    {
        std::cout << "Sensor " << name_ << " created\n";
    }

    // --- COPY constructor — called when: Sensor b = a;
    Sensor(const Sensor& other)
        : id_(other.id_)
        , name_(other.name_)         // copies the string
        , value_(other.value_)
    {
        std::cout << "Sensor copied\n";
    }

    // --- MOVE constructor — called when: Sensor b = std::move(a);
    //     Steals other's resources instead of copying them
    Sensor(Sensor&& other) noexcept
        : id_(other.id_)
        , name_(std::move(other.name_))  // steal the string buffer
        , value_(other.value_)
    {
        other.id_    = 0;
        other.value_ = 0.0f;
        std::cout << "Sensor moved\n";
    }

    // --- DESTRUCTOR — runs automatically when object goes out of scope
    //     In this class, std::string cleans itself up, so nothing manual is needed
    ~Sensor() {
        std::cout << "Sensor " << name_ << " destroyed\n";
    }

    float value() const { return value_; }

private:
    int         id_;
    std::string name_;
    float       value_;
};

// Initializer List Is Required for const and Reference Members
class Config {
public:
    // const and reference members MUST be initialized in the initializer list
    // They cannot be assigned in the constructor body — they have no "before state"
    Config(int max, int& counter)
        : MAX_VAL(max)          // const int — must initialize here
        , counter_ref_(counter) // int& — must initialize here; cannot be re-seated
    {}

    // This would NOT compile:
    /* Config(int max, int& counter) {
         MAX_VAL = max;        // ERROR: assignment to const
         counter_ref_ = counter; // ERROR: assigns the referenced int, doesn't bind
    } */

private:
    const int MAX_VAL;
    int&      counter_ref_;
};
// struct is the same syntax
struct Point {
    float x, y;
    // Constructor with initializer list
    Point(float x, float y) : x(x), y(y) {}  // parameter name same as member — fine here
    // Destructor (trivial here but shown for completeness)
    ~Point() = default;   // = default tells compiler to generate the default version
};

// MOVE

std::string original = "Hello, SolarEdge!";
// original owns a heap buffer containing "Hello, SolarEdge!"

// WITHOUT move — deep copy: new buffer allocated, content copied
std::string copy = original;
std::cout << original << "\n";  // original still valid: "Hello, SolarEdge!"

// WITH move — ownership transfer: no new buffer, original loses its buffer
std::string stolen = std::move(original);
std::cout << stolen   << "\n";  // "Hello, SolarEdge!"
std::cout << original << "\n";  // "" — valid but unspecified (usually empty)
// RULE: never read a moved-from variable without re-assigning it first

// Common pattern: move into a container (avoids copying large objects)
std::vector<std::string> vec;
std::string big = "large string data";
vec.push_back(std::move(big));  // big's buffer is stolen into the vector
// big is now in moved-from state — re-assign before use

// Re-assign before use — now safe again
big = "new value";
std::cout << big << "\n";  // "new value"
