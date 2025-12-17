import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="DEBUG")
FILE_NAME = "input.txt"

def load_input() -> list[str]:
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, FILE_NAME), "r") as f:
        task_input = f.readlines()
        task_input = [row.strip() for row in task_input]
    return task_input


def is_position_in_map(x:int, y:int, width: int, height: int) -> bool:
    return x >= 0 and x < width and y >= 0 and y < height


def check_word(crossword,  word: str, positions: list[int, int]) -> bool:
    for i in range(len(positions)):
        if not is_position_in_map(positions[i][0], positions[i][1], len(crossword), len(crossword[i])):
            return False
        if word[i] != crossword[ positions[i][0]] [ positions[i][1] ]:
            return False
    return True


def count_word(crossword: list[str], word: str) -> int:
    """
    This word search allows words to be 
    horizontal, vertical, diagonal, written backwards, or even overlapping other words. 
    It's a little unusual, though, as you don't merely need to find 
    one instance of XMAS - you need to find all of them.
    """
    word_count = 0
    for i in range(len(crossword)):
        for j in range(len(crossword[i])):
            # if frist leter match, check all directions
            if crossword[i][j] == word[0]:
                #check all directions
                directions = [
                    [ [i+k, j   ] for k in range(len(word)) ],
                    [ [i+k, j+k ] for k in range(len(word)) ],
                    [ [i+k, j-k ] for k in range(len(word)) ],
                    [ [i-k, j   ] for k in range(len(word)) ],
                    [ [i-k, j+k ] for k in range(len(word)) ],
                    [ [i-k, j-k ] for k in range(len(word)) ],
                    [ [i,   j+k ] for k in range(len(word)) ],
                    [ [i,   j-k ] for k in range(len(word)) ],
                ]
                word_count += sum([ check_word(crossword, word, direction) for direction in directions]) 
    return word_count


def count_xmas_in_x_shape(crossword: list[str]) -> int:
    word_count = 0
    height = len(crossword)
    width = len(crossword[0])
    for i in range(len(crossword)):
        for j in range(len(crossword[i])):
            if crossword[i][j] == "A":
                # check if cross is in bounds 
                if  is_position_in_map(i+1, j+1, width, height) and \
                    is_position_in_map(i+1, j-1, width, height) and \
                    is_position_in_map(i-1, j+1, width, height) and \
                    is_position_in_map(i-1, j-1, width, height):
                        #check if there is MAS on each direction
                        if (crossword[i-1][j-1] == "M" and crossword[i+1][j+1] == "S" or   
                            crossword[i-1][j-1] == "S" and crossword[i+1][j+1] == "M") and \
                            (crossword[i+1][j-1] == "M" and crossword[i-1][j+1] == "S" or 
                             crossword[i+1][j-1] == "S" and crossword[i-1][j+1] == "M"):
                                word_count += 1
    return word_count
                        
                    


def main():
    input_str = load_input()
    # logger.info(input_str)
    
    word_count = count_word(crossword=input_str, word="XMAS")
    logger.info(f"XMAS in crossword: {word_count}")
    xmas_cross_count = count_xmas_in_x_shape(input_str)
    logger.info(f"XMAS cross in crossword: {xmas_cross_count}")


if __name__ == "__main__":
    main()