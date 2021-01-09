##############################################################################
# FILE: boggle_logic.py
# WRITERS:
#         Nimrod Bar Giora , nimrodnm , 207090622
#         Or Franco, or.franco, 209498666
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A class that run the logic of a Boggle game.
##############################################################################
import ex12_utils as utils
from typing import Optional, Set, List, Tuple, Dict
import time

# Constants:
STARTING_SCORE = 0


class BoggleLogic:
    """
    This is a class that creates and runs the logic part of Boggle games.
    """
    def __init__(self, words_dict: Dict[str, bool], board: List[List[str]]):
        """
        The constructor of the Boggle Logic class.
        :param words_dict: a dictionary contains all the legal words.
        :param board: the board that will be played on the first game.
        """
        self.__words_dict = words_dict
        self.__board = board
        self.__curr_path: List[Tuple[int, int]] = []
        self._found_words: Set = set()
        self.__score: int = STARTING_SCORE
        # an indicator if the game as started:
        self._game_started: bool = False

    def update_score(self, n: int):
        """
        this function updates the score of the user according to the length
        of the word.
        :param n: the length of the word that was found.
        """
        self.__score += n ** 2

    def get_score(self) -> int:
        """
        this function returns the current score of the user.
        """
        return self.__score

    def insert_coord_to_path(self, coord: Tuple[int, int]):
        """
        this function inserts the coord given to the current path attribute.
        :param coord: a Tuple of ints representing a row and column on the
                        board.
        """
        self.__curr_path.append(coord)

    def pop_coord_from_path(self):
        """
        this function removes the last coord that was inserted to the current
        path.
        """
        self.__curr_path.pop()

    def clear_path(self):
        """
        this function clears the current path attribute.
        """
        self.__curr_path = []

    def submit_word(self) -> Optional[str]:
        """
        this function checks if the current path represents a valid word.
        if True, it updates the score of the user, and adds the found word
        to the found words list.
        :return: the legal word that was found or None.
        """
        word = utils.is_valid_path(self.__board,
                                   self.__curr_path,
                                   self.__words_dict)
        self.clear_path()

        if word and word not in self._found_words:
            self.update_score(len(word))
            self._found_words.add(word)
            return word

        return

    def get_path(self):
        """
        this function returns the current path.
        """
        return self.__curr_path

    def start_game(self, new_board: List[List[str]]):
        """
        This function starts and stops the game according to the game_started
        attribute.
        :param new_board: the board of the new game.

        """
        # Restart all attributes:
        if self._game_started:
            self.__curr_path = []
            self._found_words = set()
            self.__score = STARTING_SCORE
            self.__board = new_board
            self._game_started = False
        else:
            self._game_started = True


class Timer:
    """
    This is a class of timers.
    """

    def __init__(self, duration: int):
        """
        the constructor of the timer class.
        :param duration: number of seconds the timer should count from.
        """
        self.__start_time = 0
        self.__end_time = 0
        self.__duration = duration

    def start_timer(self):
        """
        this function starts the timer.
        """
        self.__start_time = int(time.time())
        self.__end_time = self.__start_time + self.__duration

    def _calculate_time(self) -> int:
        """
        This method calculates the remaining time of the timer in 'self'.
        :return: The remaining time in seconds, or None if time is over.
        """
        current_time = int(time.time())
        if current_time <= self.__end_time:
            return self.__end_time - current_time
        return 0

    def get_time(self):
        """
        :return: The current time of the timer in 'self', as a string,
                in this format: m:ss .
        """
        current_time = self._calculate_time()

        return convert_to_minutes_format(current_time)


def convert_to_minutes_format(time_in_secs: int) -> str:
    """
    This functions takes seconds as input,
    and returns the time in minutes (as a string).
    :param time_in_secs: The time in seconds (integer).
    :return: A string representing the time in this format: m:ss
    """
    minutes = time_in_secs // 60
    seconds = time_in_secs - (minutes * 60)

    if seconds < 10:
        seconds = f"0{seconds}"

    return f"{minutes}:{seconds}"
