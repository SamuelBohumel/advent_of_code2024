import os
import sys
import itertools
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO")

FILE_NAME = "input.txt"

class Problem:
    def __init__(self, result: int, numbers: list[int]):
        self.result = int(result)
        self.numbers = numbers


    def get_result(self, numbers: list[int], operators) -> int | None:
        result = numbers[0]

        for i, operator in enumerate(operators):
            n = numbers[i + 1]

            if operator == "||":
                result = int(str(result) + str(n))
            elif operator == "+":
                result += n
            else:  # "*"
                result *= n

            # Early pruning (assumes positive inputs)
            if result > self.result:
                return None

        return result

    def solve(self, operator_set) -> int:
        n = len(self.numbers)

        if n == 1:
            return self.result if self.numbers[0] == self.result else 0

        for ops in itertools.product(operator_set, repeat=n - 1):
            res = self.get_result(self.numbers, ops)
            if res is not None and res == self.result:
                return self.result

        return 0

    def is_equation_possible(self) -> int:
        return self.solve(("+", "*"))

    def is_equation_possible_concat(self) -> int:
        return self.solve(("+", "*", "||"))


def load_input(filename: str) -> list[str]:
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, FILE_NAME), "r") as f:
        task_input = f.readlines()
        task_input = [row.strip() for row in task_input]
    return task_input

def main():
    input_str = load_input(FILE_NAME)


    problems = []
    for line in input_str:
        result, numbers = line.split(":")
        nums = list(map(int, numbers.strip().split()))
        problems.append(Problem(result=result, numbers=nums))

    correct_equations1 = 0
    correct_equations2 = 0

    for prob in problems:
        correct_equations1 += prob.is_equation_possible()
        correct_equations2 += prob.is_equation_possible_concat()

    logger.info(f"Possible equations1: {correct_equations1}")
    logger.info(f"Possible equations2: {correct_equations2}")


if __name__ == "__main__":
    main()
