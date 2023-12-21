#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <queue>

#include "../lib/vec.hpp"

using namespace std;

typedef uint8_t MX_T;
typedef mx2<MX_T> MX;

MX read_input(istream& stream) {
    string str;

    vector<vector<MX_T>> result;
    while (getline(stream, str)) {
        vector<MX_T> row;
        for(char& c : str) {
            row.push_back(c - '0');
        }
        result.push_back(row);
    }
    return mx2(result);
}

MX read_input(int argc, char **argv) {
    if (argc > 1) {
        auto stream = fstream(argv[1]);
        return read_input(stream);
    } else {
        return read_input(cin);
    }
}

int iterate(MX& mx) {
    queue<vec2i> q;
    int flashes = 0;
    for (int x = 0; x < mx.shape.x; x++) {
        for (int y = 0; y < mx.shape.y; y++) {
            mx.at(x, y)++;
            if (mx.at(x, y) == 10) {
                mx.at(x, y) = 0;
                q.push({x, y});
            }
        }
    }
    static const vec2i neighbours[] = {
        {-1, -1}, {-1, 0}, {-1, 1},
        {0, -1}, {0, 1},
        {1, -1}, {1, 0}, {1, 1}
    };
    while (!q.empty()) {
        auto co = q.front();
        flashes++;
        for (auto&& nr : neighbours) {
            auto n = co + nr;
            if (n.x < 0 || n.x >= mx.shape.x || n.y < 0 || n.y >= mx.shape.y)
                continue;
            if (mx.at(n) == 0)
                continue;
            mx.at(n)++;
            if (mx.at(n) == 10) {
                mx.at(n) = 0;
                q.push(n);
            }
        }
        q.pop();
    }
    return flashes;
}

template <class T>
std::ostream& operator<<(std::ostream& stream, const mx2<T>& mx) {
    for (size_t x = 0; x < mx.shape.x; x++) {
        for (size_t y = 0; y < mx.shape.y; y++) {
            stream << int(mx.at(x, y));
        }
        stream << std::endl;
    }
    return stream;
}

int main(int argc, char **argv) {
    auto stream = fstream("11.txt");
    auto mx = read_input(stream);
    // auto mx = read_input(argc, argv);

    auto mx2 = mx;
    int mx_size = mx.size();
    auto start = chrono::steady_clock::now();


    int total = 0;
    for (int i = 0; i < 100; i++) {
        total += iterate(mx);
    }
    int idx = 1;
    while (iterate(mx2) != mx_size) {
        idx++;
    }

    auto end = chrono::steady_clock::now();
    cout << "part 1: " << total << endl;
    cout << "part 2: " << idx << endl;

    cout << "Runtime: " << chrono::duration_cast<chrono::microseconds>(end-start).count() << " us" << endl;
}
