import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="DEBUG")
FILE_NAME = "ex_input.txt"

def load_input(filename: str) -> list[str]:
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, FILE_NAME), "r") as f:
        task_input = f.readlines()
        task_input = [row.strip() for row in task_input]
    return task_input

def main():
    input_str = load_input(FILE_NAME)
    logger.info(input_str)


if __name__ == "__main__":
    main()