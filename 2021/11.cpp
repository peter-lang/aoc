#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <queue>

using namespace std;

typedef vector<uint8_t> ROW;
typedef vector<vector<uint8_t>> MX;

template <class T>
struct vec2 {
    T x, y;

    vec2() :x(0), y(0) {}
    vec2(T x, T y) : x(x), y(y) {}
    vec2(const vec2& v) : x(v.x), y(v.y) {}
    
    vec2& operator=(const vec2& v) {
        x = v.x;
        y = v.y;
        return *this;
    }
    
    vec2 operator+(const vec2& v) const {
        return vec2(x + v.x, y + v.y);
    }

    vec2 operator-(const vec2& v) const {
        return vec2(x - v.x, y - v.y);
    }
    
    vec2& operator+=(const vec2& v) {
        x += v.x;
        y += v.y;
        return *this;
    }

    vec2& operator-=(const vec2& v) {
        x -= v.x;
        y -= v.y;
        return *this;
    }
    
    vec2 operator+(T s) const {
        return vec2(x + s, y + s);
    }

    vec2 operator-(T s) const {
        return vec2(x - s, y - s);
    }

    vec2 operator*(T s) const {
        return vec2(x * s, y * s);
    }

    vec2 operator/(T s) const {
        return vec2(x / s, y / s);
    }
    
    
    vec2& operator+=(T s) {
        x += s;
        y += s;
        return *this;
    }

    vec2& operator-=(T s) {
        x -= s;
        y -= s;
        return *this;
    }

    vec2& operator*=(T s) {
        x *= s;
        y *= s;
        return *this;
    }

    vec2& operator/=(T s) {
        x /= s;
        y /= s;
        return *this;
    }

};

typedef vec2<int> vec2i;

MX read_input(string filename) {
    ifstream file(filename);
    string str;
    MX result;
    while (getline(file, str)) {
        ROW r;
        for(char& c : str) {
            r.push_back(c - '0');
        }
        result.push_back(r);
    }
    return result;
}

int iterate(MX& mx) {
    queue<vec2i> q;
    int flashes = 0;
    for (int r = 0; r < mx.size(); r++) {
        for (int c = 0; c < mx[r].size(); c++) {
            mx[r][c]++;
            if (mx[r][c] == 10) {
                mx[r][c] = 0;
                q.push({r, c});
            }
        }
    }
    vec2i neighbours[] = {
        {-1, -1}, {-1, 0}, {-1, 1},
        {0, -1}, {0, 1},
        {1, -1}, {1, 0}, {1, 1}
    };
    size_t max_x = mx.size();
    size_t max_y = mx[0].size();
    while (!q.empty()) {
        auto co = q.front();
        flashes++;
        for (auto&& nr : neighbours) {
            auto n = co + nr;
            if (n.x < 0 || n.x >= max_x || n.y < 0 || n.y >= max_y)
                continue;
            if (mx[n.x][n.y] == 0)
                continue;
            mx[n.x][n.y]++;
            if (mx[n.x][n.y] == 10) {
                mx[n.x][n.y] = 0;
                q.push(n);
            }
        }
        q.pop();
    }
    return flashes;
}


ostream& operator<<(ostream& stream, const MX& mx) {
    for (auto&& r : mx) {
        for (auto&& v : r) {
            stream << int(v);
        }
        stream << endl;
    }
    return stream;
}


int main() {
    auto mx_1 = read_input("11.txt");
    auto mx_2 = read_input("11.txt");
    int mx_size = mx_1.size() * mx_1[0].size();
    auto start = chrono::steady_clock::now();

    int total = 0;
    for (int i = 0; i < 100; i++) {
        total += iterate(mx_1);
    }
    int idx = 1;
    while (iterate(mx_2) != mx_size) {
        idx++;
    }

    auto end = chrono::steady_clock::now();
    cout << "part 1: " << total << endl;
    cout << "part 2: " << idx << endl;

    cout << "Runtime: " << chrono::duration_cast<chrono::microseconds>(end-start).count() << " us" << endl;
}
