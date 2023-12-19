import bisect
from typing import Sequence

numbers = sorted(map(int, open("7.txt", "r").read().strip().split(",")))

# part 1
median = numbers[(len(numbers) - 1) // 2]
print(sum(abs(n - median) for n in numbers))


def dist(a, b):
    diff = abs(a - b)
    return (diff + 1) * diff // 2


# Function = SUM (abs(n-i)+1)*abs(n-i) / 2 = SUM (n-i)**2/2 + abs(n-i)/2
# Derivative = SUM -n + SUM i + (len(greater items) - len(less items)) / 2
# Decrease is at most len(items) for (len(greater items) - len(less items)) / 2
# Increase is always len(items) for SUM i
# Derivative is monotone increasing, we can use binary search to find value close to 0
class Derivative(Sequence):
    def __init__(self, nums):
        self.nums = nums
        self.total = sum(nums)

    def __len__(self) -> int:
        return self.nums[-1] - self.nums[0] + 1

    def __getitem__(self, item):
        i = item + self.nums[0]
        less_items = bisect.bisect_left(self.nums, i)
        greater_items = len(self.nums) - bisect.bisect_right(self.nums, i)
        return -self.total + len(self.nums) * i + (greater_items - less_items) / 2


derivative = Derivative(numbers)
mid = bisect.bisect_left(derivative, 0)
assert derivative[mid - 1] < 0 <= derivative[mid]
mid = mid + numbers[0]

cost_1 = sum(dist(n, mid) for n in numbers)
cost_2 = sum(dist(n, mid - 1) for n in numbers)
print(min(cost_1, cost_2))
