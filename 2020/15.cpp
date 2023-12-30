#include <iostream>
#include <vector>

using namespace std;

const uint32_t nums[] = {0, 3, 1, 6, 7, 5};
const size_t nums_size = sizeof(nums) / sizeof(uint32_t);


uint32_t spoken_number(size_t N) {
    vector<uint32_t> mem(N, 0);
    for (size_t i = 0; i < nums_size-1; ++i) {
        mem[nums[i]] = i + 1;
    }

    uint32_t prev = nums[nums_size-1];
    for (size_t turn = nums_size; turn < N; ++turn) {
        uint32_t next = 0;
        if (mem[prev] != 0) {
            next = turn - mem[prev];
        }
        mem[prev] = turn;
        prev = next;
    }
    return prev;
}

int main(int argc, char **argv) {
    auto start = chrono::steady_clock::now();
    auto p1 = spoken_number(2020);
    auto p2 = spoken_number(30000000);
    auto end = chrono::steady_clock::now();

    cout << "part 1: " << p1 << endl;
    cout << "part 2: " << p2 << endl;

    cout << "Runtime: " << chrono::duration_cast<chrono::microseconds>(end-start).count() << " us" << endl;
}
