import os
from loguru import logger
import sys
from copy import deepcopy
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

def is_level_safe(level: list[str]) -> bool:
    """
    return if level is safe 
    So, a report only counts as safe if both of the following are true:
        The levels are either all increasing or all decreasing.
        Any two adjacent levels differ by at least one and at most three.
    """
    level = [int(num) for num in level]
    length = len(level)
    inc_dec_flag = all( [level[i] < level[i-1] for i in range(1,length)] ) or \
                   all( [level[i] > level[i-1] for i in range(1,length)] )
    diff_flag = all( [1 <= abs(level[i] - level[i-1]) <= 3 for i in range(1,length)] )
    return inc_dec_flag and diff_flag

def is_level_safe_with_dampener(level: list[str]) -> bool:
    """
    return if level is safe 
    So, a report only counts as safe if both of the following are true:
        The levels are either all increasing or all decreasing.
        Any two adjacent levels differ by at least one and at most three.v
    The Problem Dampener is a reactor-mounted module that lets the reactor
    safety systems tolerate a single bad level in what would otherwise be a safe report. 
    It's like the bad level never happened!
    """
    is_safe = is_level_safe(level)
    if not is_safe:
        flags = []
        for i in range(len(level)):
            new_list = deepcopy(level)
            new_list.pop(i)
            
            flags.append(is_level_safe(new_list))
        # logger.debug(flags)
        return any(flags)
    else:
        return True
    
    

def main():
    input_str = load_input(FILE_NAME)
    # logger.info(input_str)
    
    levels = [row.split(" ") for row in input_str]
    safe_levels, safe_levels_dampener = 0, 0
    for level in levels:
        if is_level_safe(level):
            safe_levels += 1
        if is_level_safe_with_dampener(level):
            safe_levels_dampener += 1
    
    logger.info(f"Safe levels: {safe_levels}")
    logger.info(f"Safe levels dampener: {safe_levels_dampener}")

if __name__ == "__main__":
    main()