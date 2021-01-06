from typing import List, Tuple, Dict, Optional

# Constants:
ROW_COORD_IND = 0
COLUMN_COORD_IND = 1


def load_words_dict(file_path):
    words_dict = dict()

    with open(file_path, 'r') as words_file:
        line = words_file.readline().replace("\n", "")
        while line:
            words_dict[line] = True
            line = words_file.readline().replace("\n", "")

    return words_dict


def is_valid_path(board: List[List[str]],
                  path: List[Tuple[int, int]],
                  words: Dict) -> Optional[str]:
    """
    TODO
    :param board:
    :param path:
    :param words:
    :return:
    """
    # TODO: Should we make sure the board contains only string (and not ints)?
    #       Should we raise exception when a coordinate is outside the board?
    board_size: int = len(board)  # Should be a square
    word: str = ""

    for coord in path:
        row_index, col_index = coord[ROW_COORD_IND], coord[COLUMN_COORD_IND]

        if 0 <= row_index < board_size and 0 <= col_index < board_size:
            word += board[row_index][col_index]

    if word in words:
        return word

    return


def find_length_n_words(n, board, words):
    pass
