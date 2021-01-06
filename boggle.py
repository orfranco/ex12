import ex12_utils as utils
import time
import tkinter as tk
from typing import Optional, Any
from boggle_board_randomizer import *

STARTING_SCORE = 0


class BoggleLogic:
    def __init__(self, words_dict, board):
        self.__words_dict = words_dict
        self.__board = board
        self.__curr_path = []
        self.__found_words = set()
        self.__score = STARTING_SCORE

    def update_score(self, n):
        self.__score += n ** 2

    def get_score(self):
        return self.__score

    def insert_coord_to_path(self, coord):
        self.__curr_path.append(coord)

    def pop_coord_from_path(self):
        self.__curr_path.pop()

    def check_path(self) -> Optional[str]:
        return utils.is_valid_path(self.__board,
                                   self.__curr_path,
                                   self.__words_dict)


COURIER_30 = ("Courier", 30)

BUTTON_HOVER_COLOR = 'tomato'
REGULAR_COLOR = 'steel blue'
BUTTON_ACTIVE_COLOR = 'gold'
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}
START_RESTART_BUTTON_STYLE = {"font": ("Courier", 14),
                              "borderwidth": 1,
                              "relief": tk.RAISED,
                              "bg": REGULAR_COLOR,
                              "width": 7,
                              "activebackground": BUTTON_ACTIVE_COLOR}
LEFT_LABEL_STYLE = {"font": COURIER_30, "bg": REGULAR_COLOR,
                    "width": 15, "height": 1, "relief": "ridge"}

RIGHT_LABEL_STYLE = {"font": COURIER_30, "bg": REGULAR_COLOR,
                     "width": 7, "relief": "ridge"}

class BoggleGui:
    def __init__(self, board, timer):
        self._board = board
        self._timer = timer
        self._main_window = tk.Tk()
        self._main_window.title("Boggle")
        self._main_window.resizable(False, False)
        self._init_left_frame()
        self._init_right_frame()
        self._pack()

    def _init_left_frame(self):
        self._left_frame = tk.Frame(self._main_window, bg=REGULAR_COLOR)
        self._curr_word_label = tk.Label(self._left_frame, **LEFT_LABEL_STYLE)
        self._progress_label = tk.Label(self._left_frame, **LEFT_LABEL_STYLE)
        self._buttons_frame = tk.Frame(self._left_frame)
        self._grid_buttons = dict()
        self._create_chars_grid(self._board)

    def _init_right_frame(self):
        self._right_frame = tk.Frame(self._main_window, bg=REGULAR_COLOR)
        self._timer_label = tk.Label(self._right_frame,
                                     **RIGHT_LABEL_STYLE, height=1
                                     , text="03:00")
        self._score_label = tk.Label(self._right_frame,
                                     **RIGHT_LABEL_STYLE, height=1,
                                     text="0")
        self._create_start_restart_frame()
        self._words_label = tk.Label(self._right_frame, **RIGHT_LABEL_STYLE,
                                     height=6)

    def _create_chars_grid(self, board):
        for row in range(len(board)):
            tk.Grid.columnconfigure(self._buttons_frame, row, weight=1)
            tk.Grid.rowconfigure(self._buttons_frame, row, weight=1)

        for row_index, row in enumerate(board):
            for col_index, char in enumerate(row):
                self._make_button_on_grid(char, row_index, col_index)

    def _make_button_on_grid(self, button_char: str, row: int, col: int,
                             rowspan: int = 1,
                             columnspan: int = 1) -> tk.Button:

        button = tk.Button(self._buttons_frame,
                           text=button_char,
                           **BUTTON_STYLE)
        button.grid(row=row,
                    column=col,
                    rowspan=rowspan,
                    columnspan=columnspan,
                    sticky=tk.NSEW)

        self._grid_buttons[button_char] = button

        def _on_enter(event: Any) -> None:
            button['background'] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            button['background'] = REGULAR_COLOR

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        return button

    def _create_start_restart_frame(self):
        self._start_restart_frame = tk.Frame(self._right_frame,
                                             bg=REGULAR_COLOR)
        self._start_button = tk.Button(self._start_restart_frame,
                                       text="Start",
                                       **START_RESTART_BUTTON_STYLE)
        self._restart_button = tk.Button(self._start_restart_frame,
                                         text="Restart",
                                         **START_RESTART_BUTTON_STYLE)

    def _pack(self):
        self._left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._curr_word_label.pack(side=tk.TOP, fill=tk.BOTH)
        self._progress_label.pack(side=tk.TOP, fill=tk.BOTH)
        self._buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._right_frame.pack(fill=tk.BOTH, expand=True)
        self._timer_label.pack(side=tk.TOP)
        self._score_label.pack(side=tk.TOP)
        self._start_restart_frame.pack(side=tk.TOP)
        self._start_button.pack(side=tk.LEFT)
        self._restart_button.pack(side=tk.LEFT)
        self._words_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run(self):
        self._main_window.mainloop()


class BoggleController:
    """
    TODO
    """
    def __init__(self):
        pass


class Timer:
    """
    This is a class of timers.
    """
    STARTING_TIME: int = 180  # Seconds

    def __init__(self):
        self.__start_time = int(time.time())
        self.__end_time = self.__start_time + 180
        self.__current_time = Timer.STARTING_TIME

    def _calculate_time(self) -> Optional[int]:
        """
        This method calculates the remaining time of the timer in 'self'.
        :return: The remaining time in seconds, or None if time is over.
        """
        current_time = int(time.time())
        if current_time <= self.__end_time:
            return self.__end_time - current_time
        return

    def get_time(self):
        """
        :return: The current time of the timer in 'self', as a string,
                in this format: m:ss .
        """
        current_time = self._calculate_time()

        if current_time is not None:
            return convert_to_minutes_format(current_time)

        return


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



boggle = BoggleGui(randomize_board(),Timer())
boggle.run()
