from typing import List, Tuple, Dict, Optional

# Constants:
ROW_INDEX = 0
COLUMN_INDEX = 1
COORD_NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1)]


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

    for coord in path:
        row_index, col_index = coord[ROW_INDEX], coord[COLUMN_INDEX]
        if coord_in_board(coord, board):
            word += board[row_index][col_index]

    if word in words:
        return word

    return


def coord_in_board(coord: Tuple[int, int], board: List[List[str]]) -> bool:
    """

    :param coord:
    :param board:
    :return:
    """
    board_size: int = len(board)  # Board should always be a square.
    row_index, col_index = coord[ROW_INDEX], coord[COLUMN_INDEX]

    if 0 <= row_index < board_size and 0 <= col_index < board_size:
        return True

    return False


def possible_cells(path: List[Tuple[int,int]],
                   board: List[List[str]]) -> List[Tuple[int, int]]:
    """
    TODO
    :param path:
    :param board:
    :return:
    """
    current_coord: Tuple[int, int] = path[-1]
    coord_row = current_coord[ROW_INDEX]
    coord_col = current_coord[COLUMN_INDEX]

    possible_neighbors: List[Tuple[int, int]] = []
    for neighbor in COORD_NEIGHBORS:
        neighbor = (neighbor[ROW_INDEX] + coord_row,
                    neighbor[COLUMN_INDEX] + coord_col)

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
    # start the helper function, from any coordinate in the board:
    for row in range(len(board)):
        for col in range(len(board)):
            all_valid_paths.extend(
                list(_helper_find_length_n_words(n, board, words,
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
    if len(curr_path) == n:
        if is_valid_path(board, curr_path, words):
            valid_paths_list.append((curr_word, curr_path))
        return valid_paths_list

    for cell in possible_cells(curr_path, board):
        _helper_find_length_n_words(n, board, words,
                                    curr_word + board[cell[0]][cell[1]],
                                    curr_path + [cell], valid_paths_list)

    return valid_paths_list
