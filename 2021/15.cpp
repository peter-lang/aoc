#include <iostream>
#include <fstream>
#include <map>
#include "../lib/vec.hpp"
#include "../lib/heapdict.hpp"

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

int heuristic(vec2i n, vec2i end) {
    return (n-end).abs().sum();
}

int a_star(MX& risk_map) {
    vec2i start = {0, 0};
    vec2i end = vec2i(risk_map.shape) - vec2i({1, 1});
    heapdict<vec2i, int> open_set;
    open_set.push_item(start, heuristic(start, end));

    map<vec2i, int> g_score;
    g_score[start] = 0;

    static const vec2i neighbours[] = {{-1, 0}, {0, -1}, {0, 1}, {1, 0}};

    while (open_set.size() > 0) {
        vec2i current = open_set.pop_item().first;
        if (current == end) {
            return g_score[current];
        }
        for (auto&& n_offset : neighbours) {
            vec2i child = current + n_offset;
            if (child.x < 0 || child.x >= risk_map.shape.x || child.y < 0 || child.y >= risk_map.shape.y) {
                continue;
            }
            int tentative_g_score = g_score[current] + risk_map[child];
            auto it = g_score.find(child);
            if (it == g_score.end()) {
                g_score[child] = tentative_g_score;
                open_set.push_item(child, tentative_g_score + heuristic(child, end));
            } else if (tentative_g_score < it->second) {
                it->second = tentative_g_score;
                open_set.push_item(child, tentative_g_score + heuristic(child, end));
            }
        }
    }
    return -1;
}


int main(int argc, char **argv) {
    auto stream = fstream("15.txt");
    auto mx = read_input(stream);
//    auto mx = read_input(argc, argv);

    auto start = chrono::steady_clock::now();

    auto mx_extended = mx.repeat(5, 5);
    for (size_t x = 0; x < 5; x++)
        for (size_t y = 0; y < 5; y++)
            mx_extended.slice(mx.shape, {x * mx.shape.x, y * mx.shape.y}) += x+y;
    mx_extended -= 1;
    mx_extended %= 9;
    mx_extended += 1;

    auto p1 = a_star(mx);
    auto p2 = a_star(mx_extended);

    auto end = chrono::steady_clock::now();
    cout << "part 1: " << p1 << endl;
    cout << "part 2: " << p2 << endl;

    cout << "Runtime: " << chrono::duration_cast<chrono::microseconds>(end-start).count() << " us" << endl;

    return 0;
}
