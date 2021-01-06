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
            action = self._create_button_action(data[COORD_INDEX], button)
            self.__gui.set_button_command(button, action)

    def _create_button_action(self, coord, button):
        def command():
            self.__logic.insert_coord_to_path(coord)
            self.__gui.update_curr_word_label(button)

        return command

    def run(self):
        self.__gui.run()


BoggleController().run()
