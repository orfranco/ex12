import ex12_utils as utils
from boggle_board_randomizer import *
from boggle_gui import BoggleGui
from boggle_logic import BoggleLogic, Timer


WORDS_FILE = "boggle_dict.txt"
CHAR_INDEX = 0
COORD_INDEX = 1


class BoggleController:
    """
    TODO
    """
    def __init__(self):
        self.__board = randomize_board()
        self.__words_dict = utils.load_words_dict(WORDS_FILE)
        self.__gui = BoggleGui(self.__board, Timer())
        self.__logic = BoggleLogic(self.__words_dict, self.__board)

        for button, data in self.__gui.get_chars_buttons().items():
            action = self._create_grid_button_action(data[COORD_INDEX], button)
            self.__gui.set_grid_button_command(button, action)

        clear_action = self._create_clear_button_action()
        self.__gui.set_clear_command(clear_action)

        check_action = self._create_check_button_action()
        self.__gui.set_check_command(check_action)

    def _create_grid_button_action(self, coord, button):
        def command():
            if button["text"]:
                self.__logic.insert_coord_to_path(coord)
                self.__gui.update_curr_word_label(button["text"])

        return command

    def _create_clear_button_action(self):
        def command():
            self.__logic.clear_path()
            self.__gui.update_curr_word_label("", True)
        return command

    def _create_check_button_action(self):
        word = self.__logic.check_path()
        if word:
            self.__gui.good_choice(self.__logic.get_score(), word)
        self.__logic.clear_path()
        self.__gui.update_curr_word_label("", True)


    def run(self):
        self.__gui.run()


BoggleController().run()
