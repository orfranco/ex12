from typing import List, Tuple, Dict, Optional

# Constants:
ROW_INDEX = 0
COL_INDEX = 1
COORD_NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1)]
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 16


def load_words_dict(file_path: str):
    """

    :param file_path: the path to the file containing the words.
    :return: a dictionary containing the words on the file as keys, and True
    for all the values.
    """
    # TODO: think about more test cases.
    words_dict = dict()

    with open(file_path, 'r') as words_file:
        for line in words_file.readlines():
            replaced_line = line.replace("\n", "")
            if replaced_line:
                words_dict[line.replace("\n", "")] = True

    return words_dict


def is_valid_path(board: List[List[str]],
                  path: List[Tuple[int, int]],
                  words: Dict) -> Optional[str]:
    """
    This function checks if the given path (list of coordinates on the board)

    :param board:
    :param path:
    :param words:
    :return:
    """
    # TODO: Should we make sure the board contains only string (and not ints)?
    #       Should we raise exception when a coordinate is outside the board?
    word: str = ""

    for index_in_path, coord in enumerate(path):
        row_index, col_index = coord[ROW_INDEX], coord[COL_INDEX]

        if index_in_path == 0:
            if coord_in_board(coord, board):
                word += board[row_index][col_index]

        elif coord in possible_cells(path[:index_in_path], board):
            word += board[row_index][col_index]

    if len(word) == len(path) and word in words:
        return word

    return


def coord_in_board(coord: Tuple[int, int], board: List[List[str]]) -> bool:
    """
    This function checks if the given coordinate is in the given board.
    :param coord: A coordinate on the board.
    :param board: The board. a 2 dimensional list.
    :return: True if the coordinate is in the board, or False otherwise.
    """
    # TODO: Will the board always be a square?
    board_size: int = len(board)  # Board should always be a square.
    row_index, col_index = coord[ROW_INDEX], coord[COL_INDEX]

    if 0 <= row_index < board_size and 0 <= col_index < board_size:
        return True

    return False


def possible_cells(path: List[Tuple[int, int]],
                   board: List[List[str]]) -> List[Tuple[int, int]]:
    """
    This function finds all possible cells that can be added to the given path.
    :param path: A path on the board - list of coordinates.
    :param board: The board - a 2 dimensional list.
    :return: A list of possible coordinates to continue the given path.
    """
    current_coord: Tuple[int, int] = path[-1]
    coord_row = current_coord[ROW_INDEX]
    coord_col = current_coord[COL_INDEX]

    possible_neighbors: List[Tuple[int, int]] = []
    for neighbor in COORD_NEIGHBORS:
        neighbor = (neighbor[ROW_INDEX] + coord_row,
                    neighbor[COL_INDEX] + coord_col)

        if coord_in_board(neighbor, board) and neighbor not in path:
            possible_neighbors.append(neighbor)

    return possible_neighbors


def find_length_n_words(n: int, board: List[List[str]], words: Dict):
    """
    this function finds all the valid words in length n that the given
    board contains.
    :param n: the length of the words needed to be found.
    :param board: the board to search on.
    :param words: a dictionary containing all the valid words that can be found
                    on a board.
    :return: all the valid words from length n, that the board contains.
    """
    all_valid_paths = []
    length_n_words = set(filter(lambda x: len(x) == n, words))

    # start the helper function, from any coordinate in the board:
    if MIN_WORD_LENGTH <= n <= MAX_WORD_LENGTH:
        # TODO: validate the board is a square.
        for row in range(len(board)):
            for col in range(len(board)):
                all_valid_paths.extend(
                    list(_helper_find_length_n_words(n, board, length_n_words,
                                                     board[row][col],
                                                     [(row, col)], [])))

    return all_valid_paths


def _helper_find_length_n_words(n, board, words, curr_word,
                                curr_path, valid_paths_list):
    """
    this function finds all the valid words in length n that the given
    board contains.
    :param n: the length of the words needed to be found.
    :param board: the board to search on.
    :param words: a dictionary containing all the valid words that can be found
                    on a board.
    :param curr_path: a list of tuples, representing the coordinates of the
     characters that the word was formed from.
    :param valid_paths_list: a list that will contains all the
                            valid path lists.
    :return: a list that contains all the valid path lists of words with
            length n.
    """
    # base case:
    if len(curr_word) == n:
        if curr_word in words:
            valid_paths_list.append((curr_word, curr_path))
        return valid_paths_list
    if len(curr_word) > n:
        return valid_paths_list

    good_word = False
    for word in words:
        if word.startswith(curr_word):
            good_word = True
    if not good_word:
        return valid_paths_list

    for cell in possible_cells(curr_path, board):
        _helper_find_length_n_words(n, board, words, curr_word +
                                    board[cell[ROW_INDEX]][cell[COL_INDEX]],
                                    curr_path + [cell], valid_paths_list)

    return valid_paths_list
