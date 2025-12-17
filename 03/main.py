import os
from loguru import logger
import sys
import re
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

def extract_pattern(input_str: list[str], pattern: str) -> list[str]:
    
    results = []
    for row in input_str:
        matches = re.findall(pattern, row)
        results.extend(matches)
        # logger.debug(results)
    return results


def main():
    input_str = load_input(FILE_NAME)
    # logger.info(input_str)
    reg_muls = r'mul\([0-9]{1,3},[0-9]{1,3}\)'
    reg_plus_instructions = r'mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don\'t\(\)'
    #Task 1: extract only mul statements 
    mul_statements = extract_pattern(input_str, reg_plus_instructions)
    result_mul = 0
    result_mul_plut_instr = 0
    instruction = True
    for statement in mul_statements:
        if statement == "do()":
            instruction = True
            continue
        if statement == "don't()":
            instruction = False
            continue
        
        numbers = statement.replace("mul(", "").replace(")", "").split(",")
        assert len(numbers) == 2
        #always add to res_mul
        result_mul += (int(numbers[0]) * int(numbers[1]))
        #add to result_mul_plut_instr only if flag is true
        if instruction:
            result_mul_plut_instr += (int(numbers[0]) * int(numbers[1]))
    
    logger.info(f"Result task1: {result_mul}")
    logger.info(f"Result task1: {result_mul_plut_instr}")
    
    

if __name__ == "__main__":
    main()