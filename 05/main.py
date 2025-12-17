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


def filter_correct_updates(rules: list[str], updates: list[str]) -> list[str]:
    correct_updates = []
    wrong_updates = []
    for update in updates:
        update_pages = [int(num) for num in update.split(',')]
        rules_applied = []
        for i in range(1, len(update_pages)):
            is_in_rules = any( [update_pages[i] == rule[1] and update_pages[i-1] == rule[0] for rule in rules] )
            rules_applied.append(is_in_rules)
        # if every number had a rule
        if all(rules_applied):
            correct_updates.append(update_pages)
        else:
            wrong_updates.append(update_pages)
    return correct_updates, wrong_updates


def fix_updates(rules: list[str], wrong_updates: list[str]) -> list[str]:
    fixed_updates = []
    for update in wrong_updates:
        rules_applied = []
        new_upd = update
        for i in range(1, len(new_upd)):
            is_in_rules = any( [new_upd[i] == rule[1] and new_upd[i-1] == rule[0] for rule in rules] )
            

        
    return fix_updates


def main():
    input_str = load_input(FILE_NAME)
    # logger.info(input_str)
    #Load rules and updates
    rules, updates = [], []
    rules_flag = True
    for row in input_str:
        if row == '':
            rules_flag = False
            continue
        if rules_flag:
            rules.append(row)
        else:
            updates.append(row)
    
    rules = [[int(num) for num in rule.split('|')] for rule in rules]         

         
    correct_updates, wrong_updates = filter_correct_updates(rules, updates)    
    wrong_updates = fix_updates(rules, wrong_updates)    
    # logger.info(f"filtered: {filtered}")
    #sum numbers in the middle of update 
    result_task1 = 0
    for update in correct_updates:
        result_task1 += update[len(update)//2]
        
    logger.info(f"Task 1 result: {result_task1}")


if __name__ == "__main__":
    main()