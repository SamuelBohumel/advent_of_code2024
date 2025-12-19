import os
from loguru import logger
from copy import deepcopy
import sys
logger.remove()
logger.add(sys.stdout, level="DEBUG")
FILE_NAME = "input.txt"

GUARD = "^"
OBSTACLE = "#"
VISITED = "X"
MY_OBSTACLE = "O"

class Position:
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def is_in_bounds(self) -> bool:
        return self.x >= 0 and \
               self.x < self.width and \
               self.y >= 0 and \
               self.y < self.height 

    def equals(self, position) -> bool:
        return self.x == position.x and self.y == position.y

    def __str__(self):
        return f"Position: {self.x}, {self.y}"
        
        

def load_input(filename: str) -> list[str]:
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, FILE_NAME), "r") as f:
        task_input = f.readlines()
        task_input = [row.strip() for row in task_input]
    return task_input


def find_start_position(pole_map: list[str]) -> Position:
    for i in range(len(pole_map)):
        for j in range(len(pole_map[i])):
            if pole_map[i][j] == GUARD:
                return Position(x=j, y=i, width=len(pole_map[i]), height=len(pole_map))
    raise Exception("Guard not found")

def count_visited(pole_map: list[str]) -> int:
    count = 0
    for row in pole_map:
        count += row.count(VISITED)
    return count

def test_loop(pole_map: list[str], pos: Position, x_movement: int, y_movement: int) -> bool:
    """
    returns True if there is a loop after placing a new obstacle in the map:
    """
    init_position = deepcopy(pos)
    visited = []
    while pos.is_in_bounds():
        next_position = deepcopy(pos)
        next_position.x += x_movement
        next_position.y += y_movement
        if next_position.is_in_bounds() and pole_map[next_position.y][next_position.x] == OBSTACLE:
            #change direcion 90 degrees
            if x_movement == 0 and y_movement == -1:    #UP 
                # we change to RIGHT
                x_movement = 1
                y_movement = 0
            elif x_movement == 0 and y_movement == 1:   #DOWN
                # we change to LEFT
                x_movement = -1
                y_movement = 0
            elif x_movement == -1 and y_movement == 0:   #LEFT
                # we change to UP
                x_movement = 0
                y_movement = -1
            elif x_movement == 1 and y_movement == 0:   #RIGHT
                # we change to DOWN            
                x_movement = 0
                y_movement = 1
        unique_str = str(pos.x) + str(pos.y) + str(x_movement) + str(y_movement)
        if unique_str in visited:
            break
        else:
            visited.append(unique_str)
        # add X to visited position
        pole_map[pos.y] = pole_map[pos.y][:pos.x] + VISITED + pole_map[pos.y][pos.x + 1:]
        # update position
        pos.x += x_movement
        pos.y += y_movement
        if pos.equals(init_position):
            return True
        # logger.debug(pos)
    return False


def predict_guard_position(pole_map: list[str]) -> int:
    dist_positions = 0
    obstacle_count = 0
    obstacles = []
    x_movement = 0
    y_movement = -1 # first we go UP
    position = find_start_position(pole_map) 
    pos_string = str(position.x) + str(position.y)
    while position.is_in_bounds():
        next_position = deepcopy(position)
        next_position.x += x_movement
        next_position.y += y_movement
        if next_position.is_in_bounds() and pole_map[next_position.y][next_position.x] == OBSTACLE:
            #change direcion 90 degrees
            if x_movement == 0 and y_movement == -1:    #UP 
                # we change to RIGHT
                x_movement = 1
                y_movement = 0
            elif x_movement == 0 and y_movement == 1:   #DOWN
                # we change to LEFT
                x_movement = -1
                y_movement = 0
            elif x_movement == -1 and y_movement == 0:   #LEFT
                # we change to UP
                x_movement = 0
                y_movement = -1
            elif x_movement == 1 and y_movement == 0:   #RIGHT
                # we change to DOWN            
                x_movement = 0
                y_movement = 1
        # if postiion is already visited and we can place obstacle on the next one - we can create a loop               
        possible_position = deepcopy(position)
        possible_position.x += x_movement
        possible_position.y += y_movement       
        if possible_position.is_in_bounds():    # if we can set the obstacle
            new_map = deepcopy(pole_map)
            new_map[possible_position.y] = new_map[possible_position.y][:possible_position.x] + OBSTACLE + new_map[possible_position.y][possible_position.x + 1:]
            if test_loop(pole_map=new_map, 
                         pos=deepcopy(position), 
                         x_movement=x_movement, 
                         y_movement=y_movement):
                logger.info(f"testloop is True, obstacle: {possible_position.x}, {possible_position.y}")
                obstacle_count += 1                
        # add X to visited position
        pole_map[position.y] = pole_map[position.y][:position.x] + VISITED + pole_map[position.y][position.x + 1:]
        # update position
        position.x += x_movement
        position.y += y_movement
    x_count = count_visited(pole_map)
    logger.debug(f"xcount: {x_count} | dist_positions: {dist_positions}")
    # assert x_count == dist_positions
    return x_count, obstacle_count


def main():
    input_str = load_input(FILE_NAME)
    # logger.info(input_str)
    
    dis_positions, obstacle_count = predict_guard_position(pole_map=deepcopy(input_str))
    
    logger.info(f"Distinct visited positions: {dis_positions}")
    logger.info(f"Obstacle_count: {obstacle_count}")


if __name__ == "__main__":
    main()