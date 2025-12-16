import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="DEBUG")
FILE_NAME = "input.txt"

def load_input(filename: str) -> list[str]:
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, FILE_NAME), "r") as f:
        task_input = f.readlines()
        task_input = [row.strip() for row in task_input]
    return task_input

def similarity_score(col1: list[str], col2: list[str]):
    """
    Calculate a total similarity score by adding up each number in the left list 
    after multiplying it by the number of times that number appears in the right list.
    """
    similarity_score = 0
    for number in col1:
        appears_in_col2_count = col2.count(number)
        similarity_score += (int(number) * appears_in_col2_count)
    return similarity_score

def main():
    input_str = load_input(FILE_NAME)
    # logger.info(input_str)
    col1, col2 = [], []
    for line in input_str:
        splitted = line.split(" ")
        col1.append(splitted[0])
        col2.append(splitted[-1])
    col1.sort()
    col2.sort()
    assert len(col1) == len(col2)
    #sum the differences
    differences = 0
    for i in range(len(col1)):
        differences += abs(int(col1[i]) - int(col2[i]))

    logger.info(f"Accumulated difference: {differences}")
    logger.info(f"Similarity score: {similarity_score(col1, col2)}")

if __name__ == "__main__":
    main()