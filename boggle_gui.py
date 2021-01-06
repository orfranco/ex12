import tkinter as tk
from typing import Optional, Any, Dict, Tuple


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
        self._chars_buttons: Dict[tk.Button, Tuple[str, Tuple[int, int]]] = dict()
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

        self._chars_buttons[button] = (button_char, (row, col))

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
        self._create_scrollbar_frame()
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

    def _create_scrollbar_frame(self):
        self._scrollbar_frame = tk.Frame(self._right_frame, bg=REGULAR_COLOR)
        self._words_scrollbar = tk.Scrollbar(self._scrollbar_frame)
        self._found_words_list = \
            tk.Listbox(self._scrollbar_frame,
                       yscrollcommand=self._words_scrollbar.set, width=26)
        self._found_words_list.insert(tk.END, "a word")

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
        self._scrollbar_frame.pack(side=tk.TOP, fill=tk.Y)
        self._words_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self._found_words_list.pack(side=tk.LEFT)
        self._check_button.pack(side=tk.TOP, fill=tk.BOTH,expand=True)

    def run(self):
        self._main_window.mainloop()

    def _start_game(self):
        if self._start_button["text"] == "Start":
            self._start_button["text"] = "Stop"
            for button, button_data in self._chars_buttons.items():
                button["text"] = button_data[0]
            self._timer.start_timer()
            self._animate_timer()
        else:
            pass

    def _animate_timer(self):
        self._timer_label["text"] = self._timer.get_time()
        if self._timer_label["text"] != "0:00":
            self._timer_animator_id = \
                self._main_window.after(100, self._animate_timer)

    def get_chars_buttons(self) -> Dict[tk.Button, Tuple[str, Tuple[int, int]]]:
        """
        TODO
        :return:
        """
        return self._chars_buttons

    def set_grid_button_command(self, button, action):
        button["command"] = action

    def set_clear_command(self, action):
        self._clear_button["command"] = action

    def set_check_command(self, action):
        self._check_button["command"] = action

    def update_curr_word_label(self, char, is_clear=False):
        if not is_clear:
            self._curr_word_label["text"] += char
        else:
            self._curr_word_label["text"] = ""

    def good_choice(self, score, word):
        self._score_label["text"] = score
        self._found_words_list.insert(word)