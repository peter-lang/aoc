import math

numbers = sorted(map(int, open("7.txt", "r").read().strip().split(",")))

# part 1
median = numbers[(len(numbers) - 1) // 2]
# if there are two medians, both would produce the same result, it's ok to take the lower
print(sum(abs(n - median) for n in numbers))


def dist(a, b):
    diff = abs(a - b)
    return (diff + 1) * diff // 2


def cost(med):
    return sum(dist(n, med) for n in numbers)


# Function: SUM abs(a - i)**2_ / 2 (2_ means falling power of 2)
# Discrete derivative: SUM abs(a - i)**2_ / 2 = -SUM (a - i) for i<a + SUM (i-a) for i>=a = SUM (i-a)
# Maximum, where discrete derivative is 0 => i = sum(a) / len(a)
# Note: this is an approximation, as chain-rule is different in discrete calculus
# we need to add an error term to the second derivative each time a sign change happens
# in the abs function. This means a total of len(a) error in the first derivative, so
# (sum(a)-len(a)) / len(a) <= i <= (sum(a)+len(a)) / len(a)

squared_median = sum(numbers) / len(numbers)
print(
    min(
        cost(math.ceil(squared_median) - 1),
        cost(math.ceil(squared_median)),
        cost(math.floor(squared_median)),
        cost(math.floor(squared_median) + 1),
    )
)
