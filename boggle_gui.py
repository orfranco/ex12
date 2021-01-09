import tkinter as tk
from typing import Optional, Any, Dict, Tuple


COURIER_30 = ("Courier", 30)
CALIBRI_11 = ("Calibri", "11",)

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
                    "width": 15, "height": 2, "relief": "ridge"}

RIGHT_LABEL_STYLE = {"font": COURIER_30, "bg": REGULAR_COLOR,
                     "width": 7, "relief": "ridge"}
CHAR_INDEX = 0
COORD_INDEX = 1


class BoggleGui:
    def __init__(self, board, timer):
        self._board = board
        self._timer = timer
        self._end_timer_action = None
        self._main_window = tk.Tk()
        # self._main_window.eval("tk::PlaceWindow . center")
        self._main_window.title("Boggle")
        self._main_window.resizable(False, False)
        self._init_left_frame()
        self._init_right_frame()
        self._pack()
        self._center_main_window()

    def _center_main_window(self):
        """
        TODO
        :return:
        """
        self._main_window.update_idletasks()
        # Get main window and screen dimensions:
        root_w = self._main_window.winfo_width()
        root_h = self._main_window.winfo_height()
        screen_w = self._main_window.winfo_screenwidth()
        screen_h = self._main_window.winfo_screenheight()

        # Calculate the coordinates for the main window:
        x = (screen_w / 2) - (root_w / 2)
        y = (screen_h / 2) - (root_h / 2)

        # Set the dimensions and the placement of the main window:
        self._main_window.geometry('%dx%d+%d+%d' % (root_w, root_h, x, y))

    def _init_left_frame(self):
        """
        TODO
        :return:
        """
        self._left_frame = tk.Frame(self._main_window,
                                    bg=REGULAR_COLOR)
        self._curr_word_label = tk.Label(self._left_frame,
                                         text="", **LEFT_LABEL_STYLE)
        self._buttons_frame = tk.Frame(self._left_frame)

        # Dictionaries with data on the grid of characters:
        self._grid_buttons_to_data = dict()
        self._coords_to_buttons = dict()

        self._init_chars_grid()

    def _init_chars_grid(self):
        """
        TODO
        :return:
        """
        # Create a grid:
        for row in range(len(self._board)):
            tk.Grid.columnconfigure(self._buttons_frame, row, weight=1)
            tk.Grid.rowconfigure(self._buttons_frame, row, weight=1)

        # Fill the grid with buttons:
        for row_index, row in enumerate(self._board):
            for col_index, char in enumerate(row):
                self._make_button_on_grid(char, row_index, col_index)

    def _make_button_on_grid(self, button_char: str,
                             row: int, col: int,) -> tk.Button:
        """
        TODO
        :param button_char:
        :param row:
        :param col:
        :return:
        """
        button = tk.Button(self._buttons_frame, text="", **BUTTON_STYLE)
        button.grid(row=row, column=col, sticky=tk.NSEW)

        self._grid_buttons_to_data[button] = (button_char, (row, col))
        self._coords_to_buttons[(row, col)] = button

        def _on_enter(event: Any) -> None:
            button['background'] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            button['background'] = REGULAR_COLOR

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

        return button

    def _init_right_frame(self):
        """
        TODO
        :return:
        """
        self._right_frame = tk.Frame(self._main_window,
                                     bg=REGULAR_COLOR)
        self._timer_label = tk.Label(self._right_frame,
                                     **RIGHT_LABEL_STYLE,
                                     height=1)
        self._score_label = tk.Label(self._right_frame,
                                     **RIGHT_LABEL_STYLE,
                                     height=1, text="0")

        self._create_start_clear_frame()
        self._create_scrollbar_frame()
        self._check_button = tk.Button(self._right_frame, text="Check!",
                                       **START_CLEAR_BUTTON_STYLE)

    def _create_start_clear_frame(self):
        """
        TODO
        :return:
        """
        self._start_clear_frame = tk.Frame(self._right_frame,
                                           bg=REGULAR_COLOR)
        self._clear_button = tk.Button(self._start_clear_frame,
                                       text="Clear",
                                       **START_CLEAR_BUTTON_STYLE)
        self._start_button = tk.Button(self._start_clear_frame,
                                       text="Start",
                                       **START_CLEAR_BUTTON_STYLE)

    def _create_scrollbar_frame(self):
        # TODO: leyafyef.
        """
        TODO
        :return:
        """
        self._scrollbar_frame = tk.Frame(self._right_frame, bg=REGULAR_COLOR)
        self._words_scrollbar = tk.Scrollbar(self._scrollbar_frame)
        self._found_words_list = tk.Listbox(self._scrollbar_frame,
                                            yscrollcommand=
                                            self._words_scrollbar.set,
                                            width=26, height=11)

    def _pack(self):
        """
        TODO
        :return:
        """
        # Pack left frame:
        self._left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._curr_word_label.pack(side=tk.TOP)
        self._buttons_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Pack right frame:
        self._right_frame.pack(fill=tk.BOTH, expand=True)
        self._timer_label.pack(side=tk.TOP)
        self._score_label.pack(side=tk.TOP)
        self._start_clear_frame.pack(side=tk.TOP)
        self._clear_button.pack(side=tk.LEFT)
        self._start_button.pack(side=tk.LEFT)
        self._scrollbar_frame.pack(side=tk.TOP, fill=tk.Y)
        self._words_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self._found_words_list.pack(side=tk.LEFT)
        self._check_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run(self):
        self._main_window.mainloop()

    def start_stop_game(self, new_board):
        """
        TODO
        :param new_board:
        :return:
        """
        # Start the game:
        if self._start_button["text"] == "Start":
            print("start_gui")
            self._start_button["text"] = "Stop"
            self._found_words_list.delete(0, tk.END)
            self._score_label["text"] = "0"

            for button, button_data in self._grid_buttons_to_data.items():
                button["text"] = button_data[CHAR_INDEX]
            self._timer.start_timer()
            self._animate_timer()

        else:
            self._stop_game(new_board)

    def _stop_game(self, new_board):
        """
        TODO
        :param new_board:
        :return:
        """
        self._start_button["text"] = "Start"
        self._board = new_board

        # Clear labels:
        self._curr_word_label["text"] = ""
        self._timer_label["text"] = ""

        # Stop the timer animation:
        self._main_window.after_cancel(self._timer_animator_id)

        # Reload characters to the grid:
        for row in range(len(new_board)):
            for col in range(len(new_board)):
                button = self._coords_to_buttons[(row, col)]
                coord = (row, col)
                new_char = new_board[row][col]
                self._grid_buttons_to_data[button] = (new_char, coord)
                self._coords_to_buttons[coord]["text"] = ""
        self._popup(new_board)

    def _animate_timer(self):
        """
        TODO
        :return:
        """
        self._timer_label["text"] = self._timer.get_time()

        if self._timer_label["text"] != "0:00":
            self._timer_animator_id = \
                self._main_window.after(100, self._animate_timer)
        else:
            self._end_timer_action()

    def get_timer_label(self):
        return self._timer_label

    def get_chars_buttons(self) -> Dict[tk.Button, Tuple[str, Tuple[int, int]]]:
        """
        TODO
        :return:
        """
        return self._grid_buttons_to_data

    def set_grid_button_command(self, button, action):
        button["command"] = action

    def set_clear_command(self, action):
        self._clear_button["command"] = action

    def set_check_command(self, action):
        self._check_button["command"] = action

    def set_start_stop_command(self, action):
        self._start_button["command"] = action

    def set_end_timer_action_command(self, action):
        self._end_timer_action = action

    def update_curr_word_label(self, char, is_clear=False):
        if not is_clear:
            self._curr_word_label["text"] += char
        else:
            self._curr_word_label["text"] = ""

    def good_choice(self, score, word):
        """
        TODO
        :param score:
        :param word:
        :return:
        """
        self._score_label["text"] = score
        self._found_words_list.insert(tk.END, word)

    def _popup(self, new_board):
        popup = tk.Toplevel(self._main_window)
        # Make sure its impossible to click on the main window:
        popup.transient(self._main_window)
        popup.grab_set()

        # Center the popup on the screen:
        self._main_window.eval(f"tk::PlaceWindow {str(popup)} center")

        def play_again():
            self._end_timer_action()
            popup.destroy()

        def quit_cmd():
            popup.destroy()
            self._main_window.destroy()

        popup.wm_title("Game Stopped")
        # text_frame = tk.Frame(popup, relief=tk.RAISED, borderwidth=1)
        score_label = tk.Label(popup,
                               text=
                               f"Your Score: {self._score_label['text']}",
                               font=CALIBRI_11,
                               width=24)
        question_label = tk.Label(popup,
                                  text="Do you want to play again?",
                                  font=CALIBRI_11)
        score_label.pack(side='top', fill='x', pady=10)
        question_label.pack(side='top', fill='x', pady=10)
        buttons_frame = tk.Frame(popup)
        play_again_button = tk.Button(popup,
                                      text="Yes",
                                      font=CALIBRI_11,
                                      width=4,
                                      command=play_again)
        quit_button = tk.Button(popup,
                                text="No",
                                font=CALIBRI_11,
                                width=4,
                                command=quit_cmd)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        play_again_button.pack(side=tk.LEFT, padx=(40, 0), pady=5)
        quit_button.pack(side=tk.RIGHT, padx=(0, 40))
        popup.mainloop()

# TODO:
#  1) Fix popup:
#     - center. done
#     - yifyuf
#  2) yifyuf main window
#  3) Add tests!
#  4) Document!.
