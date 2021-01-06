import ex12_utils as utils
import time
import tkinter as tk
from typing import Optional, Any, Dict, Tuple
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

    def clear_path(self):
        self.__curr_path = []

    def check_path(self) -> Optional[str]:
        return utils.is_valid_path(self.__board,
                                   self.__curr_path,
                                   self.__words_dict)


COURIER_30 = ("Courier", 30)

BUTTON_HOVER_COLOR = 'sky blue'
REGULAR_COLOR = 'azure'
BUTTON_ACTIVE_COLOR = 'dark turquoise'
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}

START_CLEAR_BUTTON_STYLE = {"font": ("Courier", 14),
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
        self._curr_word_label = tk.Label(self._left_frame,
                                         text="", **LEFT_LABEL_STYLE)
        self._progress_label = tk.Label(self._left_frame, **LEFT_LABEL_STYLE)
        self._buttons_frame = tk.Frame(self._left_frame)
        self._chars_buttons: Dict[tk.Button, str] = dict()
        self._chars_coords: Dict[Tuple[int, int], str] = dict()
        self._create_chars_grid(self._board)

    def _create_chars_grid(self, board):
        for row in range(len(board)):
            tk.Grid.columnconfigure(self._buttons_frame, row, weight=1)
            tk.Grid.rowconfigure(self._buttons_frame, row, weight=1)

        for row_index, row in enumerate(board):
            for col_index, char in enumerate(row):
                self._make_button_on_grid(char, row_index, col_index)

    def _make_button_on_grid(self, button_char: str,
                             row: int, col: int,) -> tk.Button:

        button = tk.Button(self._buttons_frame,
                           text="",
                           **BUTTON_STYLE)
        button.grid(row=row,
                    column=col,
                    sticky=tk.NSEW)

        self._chars_buttons[button] = button_char
        self._chars_coords[(row, col)] = button_char

        def _on_enter(event: Any) -> None:
            button['background'] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            button['background'] = REGULAR_COLOR

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        return button

    def _init_right_frame(self):
        self._right_frame = tk.Frame(self._main_window, bg=REGULAR_COLOR)
        self._timer_label = tk.Label(self._right_frame,
                                     **RIGHT_LABEL_STYLE, height=1)
        self._score_label = tk.Label(self._right_frame,
                                     **RIGHT_LABEL_STYLE, height=1,
                                     text="0")
        self._create_start_clear_frame()
        self._words_label = tk.Label(self._right_frame, **RIGHT_LABEL_STYLE,
                                     height=4)
        self._check_button = tk.Button(self._right_frame, text="Check!",
                                       **START_CLEAR_BUTTON_STYLE)

    def _create_start_clear_frame(self):
        self._start_clear_frame = tk.Frame(self._right_frame,
                                           bg=REGULAR_COLOR)
        self._clear_button = tk.Button(self._start_clear_frame,
                                       text="Clear",
                                       **START_CLEAR_BUTTON_STYLE)
        self._start_button = tk.Button(self._start_clear_frame,
                                       text="Start",
                                       **START_CLEAR_BUTTON_STYLE,
                                       command=self._start_game)

    def _pack(self):
        self._left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._curr_word_label.pack(side=tk.TOP, fill=tk.BOTH)
        self._progress_label.pack(side=tk.TOP, fill=tk.BOTH)
        self._buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._right_frame.pack(fill=tk.BOTH, expand=True)
        self._timer_label.pack(side=tk.TOP)
        self._score_label.pack(side=tk.TOP)
        self._start_clear_frame.pack(side=tk.TOP)
        self._clear_button.pack(side=tk.LEFT)
        self._start_button.pack(side=tk.LEFT)
        self._words_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._check_button.pack(side=tk.TOP, fill=tk.BOTH,expand=True)

    def run(self):
        self._main_window.mainloop()

    def _start_game(self):
        if self._start_button["text"] == "Start":
            self._start_button["text"] = "Stop"
            for button, button_char in self._chars_buttons.items():
                button["text"] = button_char
            self._timer.start_timer()
            self._animate_timer()
        else:
            pass

    def _animate_timer(self):
        self._timer_label["text"] = self._timer.get_time()
        if self._timer_label["text"] != "0:00":
            self._timer_animator_id = \
                self._main_window.after(100, self._animate_timer)

    def get_chars_buttons(self) -> Dict[tk.Button, str]:
        """
        TODO
        :return:
        """
        return self._chars_buttons

    def get_chars_buttons_coords(self) -> Dict[Tuple[int, int], str]:
        """
        TODO
        :return:
        """
        return self._chars_coords

    def set_button_command(self, button_char, action):
        for button, char in self._chars_buttons.items():
            if button_char == char:
                button["command"] = action

    def update_curr_word_label(self, char):
        self._curr_word_label["text"] += char


WORDS_FILE = "boggle_dict.txt"


class BoggleController:
    """
    TODO
    """
    def __init__(self):
        self.__board = randomize_board()
        self.__words_dict = utils.load_words_dict(WORDS_FILE)
        self.__gui = BoggleGui(self.__board, Timer())
        self.__logic = BoggleLogic(self.__words_dict, self.__board)

        for coord, char in self.__gui.get_chars_buttons_coords().items():
            action = self._create_button_action(coord, char)
            self.__gui.set_button_command(char, action)

    def _create_button_action(self, coord, char):
        def command():
            self.__logic.insert_coord_to_path(coord)
            self.__gui.update_curr_word_label(char)

        return command

    def run(self):
        self.__gui.run()


class Timer:
    """
    This is a class of timers.
    """
    STARTING_TIME: int = 180  # Seconds

    def __init__(self):
        self.__start_time = 0
        self.__end_time = 0
        self.__current_time = Timer.STARTING_TIME

    def start_timer(self):
        self.__start_time = int(time.time())
        self.__end_time = self.__start_time + Timer.STARTING_TIME

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

BoggleController().run()
