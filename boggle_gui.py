##############################################################################
# FILE: boggle_gui.py
# WRITERS:
#         Nimrod Bar Giora , nimrodnm , 207090622
#         Or Franco, or.franco, 209498666
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A GUI class for a Boggle game.
##############################################################################
import tkinter as tk
from typing import Any, Dict, Tuple, Callable, List
import time
import os
import sys
with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f
    # tries to open pygame,
    try:
        import pygame
        pygame_imported = True
    except:
        pygame_imported = False
    # enable stdout
    sys.stdout = oldstdout


# Fonts
COURIER_27 = ("Courier", 27)
COURIER_24 = ("Courier", 24)
COURIER_30 = ("Courier", 30)
COURIER_14 = ("Courier", 14)
CALIBRI_11 = ("Calibri", 11)

# Styles:
BUTTON_HOVER_COLOR = 'sky blue'
REGULAR_COLOR = 'LightSteelBlue3'
BUTTON_ACTIVE_COLOR = 'dark turquoise'
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": "groove",
                "bg": REGULAR_COLOR,
                "width": 1,
                "height": 1,
                "activebackground": BUTTON_ACTIVE_COLOR}
START_CLEAR_BUTTON_STYLE = {"font": COURIER_14,
                            "borderwidth": 1,
                            "relief": "raised",
                            "bg": "DeepSkyBlue4",
                            "padx": 3,
                            "width": 7,
                            "activebackground": BUTTON_ACTIVE_COLOR}
CHECK_BUTTON_STYLE = {"font": COURIER_14,
                      "borderwidth": 1,
                      "relief": "raised",
                      "bg": "DeepSkyBlue4",
                      "width": 15, "height": 2,
                      "activebackground": BUTTON_ACTIVE_COLOR}

LEFT_LABEL_STYLE = {"font": COURIER_27, "bg": REGULAR_COLOR,
                    "width": 16, "height": 2, "relief": "groove"}

RIGHT_LABEL_STYLE = {"font": COURIER_24, "bg": REGULAR_COLOR,
                     "width": 7, "relief": "flat"}
LISTBOX_STYLE = {'bg': 'azure',
                 'selectbackground': 'azure',
                 'selectforeground': 'Black',
                 'activestyle': 'none',
                 'relief': 'flat',
                 'width': 26, 'height': 11}
# Popup style:
SCORE_TEXT = "Your Score: {}"
QUESTION_TEXT = "Do you want to play again?"
PLAY_AGAIN_BUTTON_STYLE = {'text': 'Yes', 'font': CALIBRI_11, 'width': 4}
QUIT_BUTTON_STYLE = {'text': 'No', 'font': CALIBRI_11, 'width': 4}

# Constants:
LOGO_IMAGE_FILE = "Files/boggle_img.png"
MAIN_WINDOW_TITLE = "Boggle !!!"
CHECK_BUTTON_TEXT = "Check!"
CLEAR_BUTTON_TEXT = "Clear"
CHAR_INDEX = 0
COORD_INDEX = 1
END_TIME = "0:00"
START_NBA_TIME = "0:11"

# Button sound effects:
REGULAR_BUTTON_SOUND = "Files/basic-click-wooden_16.wav"
EXIT_GAME_SOUND = "Files/Close Door.wav"
NBA_SOUND = "Files/nba-games-tone.wav"
DEFAULT_CHANNEL = 0
NBA_CHANNEL = 1
DEFAULT_VOLUME = 0.3
NBA_VOLUME = 0.1


class BoggleGui:
    """
    This is a class that creates and runs a GUI for Boggle games.
    """
    def __init__(self, board: List[List[str]], timer: Any):
        """
        The constructor of the Boggle Gui.
        :param board: the board that will be played on the first game.
        :param timer: the timer object.
        """
        if pygame_imported:
            pygame.init()
        self._board = board
        self._timer = timer
        self._end_timer_action = None
        self._main_window = tk.Tk()
        self._main_window.geometry("570x450")
        self._main_window.title(MAIN_WINDOW_TITLE)
        self._main_window.resizable(False, False)
        self._init_logo()
        self._init_left_frame()
        self._init_right_frame()
        self._pack()
        self._center_main_window()

    def _center_main_window(self):
        """
        This function centres the main window on the screen.
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

    def _init_logo(self):
        """
        This method initializes the logo of the game at the top of the main
        window.
        """
        headline_img = tk.PhotoImage(file=LOGO_IMAGE_FILE)
        headline_img = headline_img.zoom(4, 4)
        headline_img = headline_img.subsample(4, 10)
        self._headline_label = tk.Label(self._main_window,
                                        image=headline_img, bg="azure")
        self._headline_label.image = headline_img

    def _init_left_frame(self):
        """
        this function inits the left frame and the widgets it contains.
        """
        self._left_frame = tk.Frame(self._main_window, bg=REGULAR_COLOR)
        self._curr_word_label = tk.Label(self._left_frame, **LEFT_LABEL_STYLE)
        self._buttons_frame = tk.Frame(self._left_frame)

        # Dictionaries with data on the grid of characters:
        self._grid_buttons_to_data = dict()
        self._coords_to_buttons = dict()

        self._init_chars_grid()

    def _init_chars_grid(self):
        """
        this function inits the grid of buttons containing the chars.
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
        this function creates a button and places it on the grid. and inserts
        the button and its data to the buttons dictionaries.
        :param button_char: the char that the button will contain.
        :param row: the row on the grid the button needed to be placed in.
        :param col: the col on the grid the button needed to be placed in.
        :return: a button widget that is placed on the grid, and contains the
                char that was given.
        """
        # Creates the button widget and places it on the grid:
        button = tk.Button(self._buttons_frame, text="", **BUTTON_STYLE)
        button.grid(row=row, column=col, sticky=tk.NSEW)

        # Adds the button and its data to the buttons dictionaries:
        self._grid_buttons_to_data[button] = (button_char, (row, col))
        self._coords_to_buttons[(row, col)] = button

        def _on_enter(event: Any) -> None:
            button['background'] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            button['background'] = REGULAR_COLOR

        # binding the events to the functions:
        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

        return button

    def _init_right_frame(self):
        """
        this function inits the right frame and the widgets it contains.
        """
        self._right_frame = tk.Frame(self._main_window, bg=REGULAR_COLOR,
                                     borderwidth=1, relief=tk.GROOVE)
        self._timer_label = tk.Label(self._right_frame,
                                     **RIGHT_LABEL_STYLE,
                                     height=1)
        self._score_label = tk.Label(self._right_frame,
                                     **RIGHT_LABEL_STYLE,
                                     height=1, text="")

        self._create_start_clear_frame()

        self._create_words_list_frame()

        self._check_button = tk.Button(self._right_frame,
                                       text=CHECK_BUTTON_TEXT,
                                       **CHECK_BUTTON_STYLE)

    def _create_start_clear_frame(self):
        """
        this function creates the frame that contains the start and clear
        buttons.
        """
        self._start_clear_frame = tk.Frame(self._right_frame, bg=REGULAR_COLOR)
        self._clear_button = tk.Button(self._start_clear_frame,
                                       text=CLEAR_BUTTON_TEXT,
                                       **START_CLEAR_BUTTON_STYLE)
        self._start_button = tk.Button(self._start_clear_frame,
                                       text="Start",
                                       **START_CLEAR_BUTTON_STYLE)

    def _create_words_list_frame(self):
        """
        This function creates a frame that will contain the correct words the
        user will find, with a scrollbar.
        """
        # init the frame:
        self._scrollbar_frame = tk.Frame(self._right_frame, bg=REGULAR_COLOR)
        # init the scrollbar:
        self._words_scrollbar = tk.Scrollbar(self._scrollbar_frame)
        # init the list that the scrollbar will contain:
        self._found_words_list = tk.Listbox(self._scrollbar_frame,
                                            yscrollcommand=
                                            self._words_scrollbar.set,
                                            **LISTBOX_STYLE)

    def _pack(self):
        """
        This function packs all the widgets in the main window
        in the correct order.
        """
        # Pack left frame and the widgets it contains:
        self._headline_label.pack(fill=tk.BOTH)
        self._left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._curr_word_label.pack(side=tk.TOP, fill=tk.BOTH)
        self._buttons_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Pack right frame and the widgets it contains:
        self._right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._timer_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._score_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._start_clear_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._clear_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._start_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._scrollbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._words_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._found_words_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._check_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True,ipady=8)

    def run(self):
        """
        This function starts the mainloop of the main window.
        """
        self._main_window.mainloop()

    def start_stop_game(self, new_board: List[List[str]]):
        """
        This function starts and stops the game according to the start_button
        label text.
        :param new_board: The board of the new game.
        """
        # Start the game:
        if self._start_button["text"] == "Start":
            # Initializing the text on the labels of the games:
            self._start_button["text"] = "Stop"
            self._found_words_list.delete(0, tk.END)
            self._score_label["text"] = "0"
            # Reveal the characters on the grid:
            for button, button_data in self._grid_buttons_to_data.items():
                button["text"] = button_data[CHAR_INDEX]
            # Start the timer and its animation:
            self._timer.start_timer()
            self._animate_timer()

        else:
            self._stop_game(new_board)

    def _stop_game(self, new_board: List[List[str]]):
        """
        This method stops the game and prepares the GUI for a new game.
        :param new_board: A new board for the next game.
        """
        self._start_button["text"] = "Start"
        self._board = new_board

        # Clear labels:
        self._curr_word_label["text"] = ""

        # Stop the timer animation:
        self._main_window.after_cancel(self._timer_animator_id)

        # Reload characters to the grid:
        for row in range(len(new_board)):
            for col in range(len(new_board)):
                button: tk.Button = self._coords_to_buttons[(row, col)]
                coord = (row, col)
                new_char = new_board[row][col]
                self._grid_buttons_to_data[button] = (new_char, coord)
                self._coords_to_buttons[coord]["text"] = ""

        # Open the popup window to show to score and offer another game:
        self._game_end_popup()

    def _animate_timer(self):
        """
        This method updates the timer label on the main window.
        """
        self._timer_label["text"] = self._timer.get_time()

        # If the timer hasn't reached 0 - keep animating:
        if self._timer_label["text"] != END_TIME:
            self._timer_animator_id = \
                self._main_window.after(100, self._animate_timer)
            if self._timer_label["text"] == START_NBA_TIME:
                self.play_button_sound(NBA_SOUND, NBA_CHANNEL, NBA_VOLUME)
        else:  # The timer has reached 0:
            self._end_timer_action()

    def get_chars_buttons(self) -> Dict[tk.Button, Tuple[str, Tuple[int,int]]]:
        """
        This method returns a dictionary with all of the character-buttons on
        the main window. Each key is a button on the characters grid, and its
        value is a tuple containing:
        1) The character it holds. 2) Its coordinates on the grid.
        """
        return self._grid_buttons_to_data

    def set_grid_button_command(self, button: tk.Button, action: Callable):
        """
        This method binds the given action to the given button on the
        characters grid.
        :param button: A character button on the characters grid.
        :param action: The function that will run when the user presses on
                       this character button.
        """
        button["command"] = action

    def set_clear_command(self, action: Callable):
        """
        this method binds the given action (a function) to the clear button.
        :param action: The function that will run when the player presses the
                       clear button.
        """
        self._clear_button["command"] = action

    def set_check_command(self, button_action: Callable,
                          keyboard_action: Callable):
        """
        This method binds the given actions (functions) to the check button,
        and to the Enter and Space keys of the keyboard.
        :param button_action: The function that will run when the player clicks
                            the check button.
        :param keyboard_action: The function that will run when the player
                                presses Enter or Space on the keyboard.
        """
        self._check_button["command"] = button_action
        self._main_window.bind("<Key>", keyboard_action)

    def set_start_stop_command(self, action: Callable):
        """
        This method binds the given action (a function) to the start/stop
        button.
        :param action: The function that will run when the player presses the
                       start/stop button.
        """
        self._start_button["command"] = action

    def set_end_timer_action_command(self, action: Callable):
        """
        This method binds the given action (a function) to an attribute which
        will be used when the timer has reached 0 (the game has ended).
        :param action: The function that will run when the timer reaches 0.
        """
        self._end_timer_action = action

    def update_curr_word_label(self, char: str, is_clear=False):
        """
        This method updates the label that shows the word that the player is
        currently constructing.
        Will add each character after the player chose it (if is_clear=False),
        and will clear the label if the player pushed the "clear"
        button (is_clear=True).
        :param char: The character to be added to the label.
        :param is_clear: if False - add the given char to the label.
                         If True - clear the label.
        """
        if not is_clear:
            self._curr_word_label["text"] += char
        else:
            self._curr_word_label["text"] = ""

    def good_choice(self, score: int, word: str):
        """
        This method is called when a correct word was chosen by the player.
        It updates the score label on the main window, and adds the chosen
        word to the words list on the main window.
        :param score: The updated score (integer).
        :param word: The word that the player chose (string).
        """
        self._score_label["text"] = score
        self._found_words_list.insert(tk.END, word)

    def _game_end_popup(self):
        """
        This method creates a popup window that shows the score the user has
        earned, and asks him if he wants to play again.
        """
        popup = tk.Toplevel(self._main_window, bg=REGULAR_COLOR)
        popup.resizable(False, False)
        popup.wm_title("Game Ended")

        # Make sure its impossible to click on the main window:
        popup.transient(self._main_window)
        popup.grab_set()

        # Center the popup on the screen:
        self._main_window.eval(f"tk::PlaceWindow {str(popup)} center")

        def play_again():
            """Restarts the game and destroys the popup window."""
            self.play_button_sound(REGULAR_BUTTON_SOUND, clear_mixer=True)
            self._end_timer_action()
            popup.destroy()

        def quit_cmd():
            """Closes the game."""
            self.play_button_sound(EXIT_GAME_SOUND)
            time.sleep(0.3)
            popup.destroy()
            self._main_window.destroy()

        score_label = tk.Label(popup,
                               text=SCORE_TEXT.format(self._score_label['text']),
                               font=CALIBRI_11, bg=REGULAR_COLOR,
                               width=24)
        question_label = tk.Label(popup, text=QUESTION_TEXT,
                                  font=CALIBRI_11,
                                  bg=REGULAR_COLOR)
        score_label.pack(side='top', fill='x', pady=10)
        question_label.pack(side='top', fill='x', pady=10)

        buttons_frame = tk.Frame(popup)
        play_again_button = tk.Button(popup,
                                      **PLAY_AGAIN_BUTTON_STYLE,
                                      command=play_again)
        quit_button = tk.Button(popup, **QUIT_BUTTON_STYLE, command=quit_cmd)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        play_again_button.pack(side=tk.LEFT, padx=(40, 0), pady=5)
        quit_button.pack(side=tk.RIGHT, padx=(0, 40))

        popup.mainloop()

    def play_button_sound(self, sound_file,
                          channel=DEFAULT_CHANNEL,
                          volume=DEFAULT_VOLUME,
                          clear_mixer=False):
        """
        This method plays sounds effect when buttons on the GUI are pressed.
        """
        if pygame_imported:
            if clear_mixer:
                pygame.mixer.pause()

            sound = pygame.mixer.Sound(sound_file)
            pygame.mixer.Channel(channel).set_volume(volume)
            pygame.mixer.Channel(channel).play(sound)
