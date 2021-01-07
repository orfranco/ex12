import ex12_utils as utils
from typing import Optional
import time

STARTING_SCORE = 0


class BoggleLogic:
    def __init__(self, words_dict, board):
        self.__words_dict = words_dict
        self.__board = board
        self.__curr_path = []
        self._found_word = set()
        self.__score = STARTING_SCORE
        self._game_started = False

    def update_score(self, n):
        """
        TODO
        :param n:
        :return:
        """
        self.__score += n ** 2

    def get_score(self):
        """
        TODO
        :return:
        """
        return self.__score

    def insert_coord_to_path(self, coord):
        """
        TODO
        :param coord:
        :return:
        """
        self.__curr_path.append(coord)

    def pop_coord_from_path(self, coord):
        """
        TODO
        :param coord:
        :return:
        """
        self.__curr_path.pop()

    def clear_path(self):
        """
        TODO
        :return:
        """
        self.__curr_path = []

    def submit_word(self) -> Optional[str]:
        """
        TODO
        :return:
        """
        word = utils.is_valid_path(self.__board,
                                   self.__curr_path,
                                   self.__words_dict)
        self.clear_path()

        if word and word not in self._found_word:
            self.update_score(len(word))
            self._found_word.add(word)
            return word

        return

    def get_path(self):
        """
        TODO
        :return:
        """
        return self.__curr_path

    def start_game(self, new_board):
        """
        TODO
        :param new_board:
        :return:
        """
        if self._game_started:
            self.__curr_path = []
            self._found_word = set()
            self.__score = STARTING_SCORE
            self.__board = new_board
            self._game_started = False
        else:
            self._game_started = True


class Timer:
    """
    This is a class of timers.
    """

    def __init__(self, duration):
        self.__start_time = 0
        self.__end_time = 0
        self.__duration = duration

    def start_timer(self):
        """
        TODO
        :return:
        """
        self.__start_time = int(time.time())
        self.__end_time = self.__start_time + self.__duration

    def _calculate_time(self) -> Optional[int]:
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
    This functions converts takes seconds as input,
    and returns the time in minutes (as a string).
    :param time_in_secs: The time in seconds (integer).
    :return: A string representing the time in this format: m:ss
    """
    minutes = time_in_secs // 60
    seconds = time_in_secs - (minutes * 60)

    if seconds < 10:
        seconds = f"0{seconds}"

    return f"{minutes}:{seconds}"
