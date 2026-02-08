import os
from loguru import logger
import sys
from itertools import product

logger.remove()
logger.add(sys.stdout, level="INFO")

FILE_NAME = "input.txt"
EMPTY = '.'


class Point:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

    def __str__(self):
        return f"Point: {self.value}: row: {self.row} | col: {self.col}"


def load_input(filename: str) -> list[str]:
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, FILE_NAME), "r") as f:
        return [row.strip() for row in f.readlines()]


def count_antidodes(points: dict, bound_rows: int, bound_cols: int) -> int:
    total_count = 0
    positions = set()

    for key, point_arr in points.items():
        for a, b in product(point_arr, repeat=2):
            if a is b:
                continue

            logger.debug(f"{a}, {b}")

            offset_x = b.row - a.row
            offest_y = b.col - a.col

            candidates = [
                (a.row - offset_x, a.col - offest_y),
                (b.row + offset_x, b.col + offset_x),
            ]

            for row, col in candidates:
                if 0 <= row < bound_rows and 0 <= col < bound_cols:
                    if (row, col) not in positions:
                        logger.info(f"Adding point: ({row}, {col})")
                        positions.add((row, col))
                        total_count += 1

    return total_count


def main():
    input_str = load_input(FILE_NAME)
    logger.info(input_str)

    points = {}

    # load input to dictionary
    for i, row in enumerate(input_str):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                continue
            point = Point(i, j, cell)
            points.setdefault(cell, []).append(point)

    # correct bounds = grid size
    bound_rows = len(input_str)
    bound_cols = len(input_str[0])

    for key, value in points.items():
        logger.debug(key)
        for p in value:
            logger.debug(p)

    antid_count = count_antidodes(points, bound_rows, bound_cols)
    logger.info(f"Antidodes: {antid_count}")


if __name__ == "__main__":
    main()
