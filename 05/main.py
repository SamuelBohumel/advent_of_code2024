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

def order_by_rules(rules: list[str]) -> str:
    #extract all nums
    array = []
    for rule in rules:
        if rule[0] not in array:
            array.append(rule[0])
        if rule[1] not in array:
            array.append(rule[1])
    for i in range(1, len(array)):
        for j in range(1, len(array)):
            for rule in rules:
                if rule[0] == array[j] and rule[1] == array[j-1]:
                    #swap numbers
                    array[j], array[j-1] = array[j-1], array[j]
    return array        

def fix_updates(rules: list[str], wrong_updates: list[str]) -> list[str]:
    fixed_updates = []
    numbers_in_order = order_by_rules(rules)
    logger.debug(numbers_in_order)
    for update in wrong_updates:
        new_upd = []
        #check indexes 
        


        fixed_updates.append(new_upd)
    return fixed_updates


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
    corrected_updates = fix_updates(rules, wrong_updates)    
    # logger.info(f"filtered: {filtered}")
    #sum numbers in the middle of update 
    result_task1 = 0
    result_task2 = 0
    for update in correct_updates:
        result_task1 += update[len(update)//2]
    for cor_update in corrected_updates:
        logger.debug(cor_update)
        result_task2 += cor_update[len(cor_update)//2]
        
    logger.info(f"Task 1 result: {result_task1}")
    logger.info(f"Task 2 result: {result_task2}")


if __name__ == "__main__":
    main()