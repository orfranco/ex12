##############################################################################
# FILE: boggle.py
# WRITERS:
#         Nimrod Bar Giora , nimrodnm , 207090622
#         Or Franco, or.franco, 209498666
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A Module that runs Boggle games.
##############################################################################
import ex12_utils as utils
from boggle_board_randomizer import *
from boggle_gui import BoggleGui
from boggle_logic import BoggleLogic, Timer
from typing import Any, Tuple, Callable

# Constants:
WORDS_FILE = "boggle_dict.txt"
GAME_DURATION = 180
CHAR_INDEX = 0
COORD_INDEX = 1


class BoggleController:
    """
    This is a class that creates and runs Boggle games,
    by using 2 other classes:
    One for the logic of the game - BoggleLogic,
    and another for the GUI - Boggle_Gui.
    """
    def __init__(self):
        """
        The constructor of the BoggleController class.
        """
        # Create a random board, and load a dictionary of words for the game:
        self.__board = randomize_board()
        self.__words_dict = utils.load_words_dict(WORDS_FILE)

        # Create Logic and GUI objects:
        self.__gui = BoggleGui(self.__board, Timer(GAME_DURATION))
        self.__logic = BoggleLogic(self.__words_dict, self.__board)

        # Create a function for the start/stop button of the GUI, and set it:
        start_stop_action = self._create_start_stop_button_action()
        self.__gui.set_start_stop_command(start_stop_action)

        # Create functions for the chars buttons of the GUI, and set them:
        for button, data in self.__gui.get_chars_buttons().items():
            action = self._create_grid_button_action(data[COORD_INDEX], button)
            self.__gui.set_grid_button_command(button, action)

        # Create a function for the clear button of the GUI, and set it:
        clear_action = self._create_clear_button_action()
        self.__gui.set_clear_command(clear_action)
        # Create a function for the check button of the GUI, and set it:
        check_action = self._create_check_button_action()
        self.__gui.set_check_command(check_action)

        # Set the start/stop command to run when the time is over:
        timer_action = start_stop_action
        self.__gui.set_end_timer_action_command(timer_action)

    def _create_start_stop_button_action(self) -> Callable:
        """
        this function creates and returns a function that calls the start_stop
        game functions on the logic and gui classes.
        """
        def command():
            self.__board = randomize_board()
            self.__logic.start_game(self.__board)
            self.__gui.start_stop_game(self.__board)

        return command

    def _create_grid_button_action(self, coord: Tuple[int,int], button: Any) \
            -> Callable:
        """
        this function creates and returns a function that calls the updating
        current word functions from the logic and gui classes.
        :param coord: the coord thats been clicked.
        :param button: the button thats been clicked.
        """
        def command():
            if button["text"]:
                self.__logic.insert_coord_to_path(coord)
                self.__gui.update_curr_word_label(button["text"])

        return command

    def _create_clear_button_action(self) -> Callable:
        """
        this function creates and returns a function that calls the clear
        current word functions from the logic and gui classes.
        """
        def command():
            self.__logic.clear_path()
            self.__gui.update_curr_word_label("", True)
        return command

    def _create_check_button_action(self) -> Callable:
        """
        this function creates and returns a function that calls the submit
        current word functions from the logic and gui classes.
        :return:
        """
        def command():
            word = self.__logic.submit_word()
            if word:
                self.__gui.good_choice(self.__logic.get_score(), word)
            self.__gui.update_curr_word_label("", True)

        return command

    def run(self):
        """
        This function starts the mainloop of the gui.

        """
        self.__gui.run()


if __name__ == '__main__':
    BoggleController().run()
