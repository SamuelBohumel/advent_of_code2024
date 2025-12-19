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
        new_upd = update
        #check indexes 
        for i in range(len(update)-1):
            for j in range(len(update)-1):
                index1 = numbers_in_order.index(update[j])
                index2 = numbers_in_order.index(update[j+1])
                if index1 > index2:
                    #swap
                    new_upd[j], new_upd[j+1] = new_upd[j+1], new_upd[j]

        fixed_updates.append(new_upd)
    return fixed_updates


#############################################
def findInvalid(nums,i, rule):
    v = nums[i]
    if v not in rule:
        return -1
    for j in range(i):
        if nums[j] in rule[v]:
            return j
    return -1

def mySort(nums, rule, step=0):
    p=-1
    for i in range(len(nums)):
        p = findInvalid(nums, i, rule)
        if(p!=-1):
            nums = nums[:p]+[nums[i]]+nums[p:i]+nums[i+1:]
            break
    if(p==-1):
        return nums
    return mySort(nums, rule, step+1)
            
def process(nums, rule):
    read = set()
    for n in nums:
        if n in rule and len(rule[n].intersection(read))>0:
            return 0
        read.add(n)
    return nums[len(nums)//2]

def repair_updates(rules: list[str], updates: list[str]):

    rule = {}
    for rul in rules:
        a,b = rul[0], rul[1]
        if a not in rule:
            rule[a]=set()
        rule[a].add(b)
    # print(rule)

    sum = 0 
    for l in updates:    
        nums= [int(x) for x in l.strip().split(",")]
        points = process(nums, rule)
        if points != 0:
            #already valid
            continue
        nums = mySort(nums, rule)
        sum+=process(nums, rule)
    return sum

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
        # logger.debug(cor_update)
        result_task2 += cor_update[len(cor_update)//2]
    
    result_task2_ext = repair_updates(rules, updates)
    logger.info(f"Task 1 result: {result_task1}")
    logger.info(f"Task 2 result: {result_task2}")
    logger.info(f"Task 2 result_ext: {result_task2_ext}")
    


if __name__ == "__main__":
    main()