import sys

from itertools import product
from operator import add, mul, concat


def calc(operation, a, b):
    if operation == concat:
        return int(concat(str(a), str(b)))
    return operation(a, b)


def solve(test_value, include_concat=False, *nums):
    operations = (
        product([add, mul], repeat=len(nums) - 1)
        if not include_concat
        else product([add, mul, concat], repeat=len(nums) - 1)
    )
    for operation in operations:
        calculated_value = 0
        for num in range(len(nums) - 1):
            a, b = nums[num] if num == 0 else calculated_value, nums[num + 1]
            calculated_value = calc(operation[num], a, b)
            if calculated_value > test_value:
                break
        if calculated_value == test_value:
            return True
    return False


data = open(sys.argv[1]).read().strip()

p1 = p2 = 0
for line in data.split("\n"):
    test_value = int(line.split(": ")[0])
    nums = list(map(int, line.split(": ")[1].split(" ")))
    p1 += test_value if solve(test_value, False, *nums) else 0
    p2 += test_value if solve(test_value, True, *nums) else 0
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")