import ex12_utils as utils
from typing import Optional

STARTING_SCORE = 0


class BoggleLogic:
    def __init__(self, words_dict, board):
        self.__words_dict = words_dict
        self.__board = board
        self.__curr_path = []
        self.__found_words = set()
        self.__score = STARTING_SCORE

    def update_score(self, n):
        self.__score += n**2

    def get_score(self):
        return self.__score

    def insert_coord_to_path(self, coord):
        self.__curr_path.append(coord)

    def pop_coord_from_path(self):
        self.__curr_path.pop()

    def check_path(self) -> Optional[str]:
        return utils.is_valid_path(self.__curr_path)


class BoggleGui:
    pass


class BoggleController:
    pass


