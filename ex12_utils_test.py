from ex12_utils import *
from boggle_board_randomizer import *

WORDS_1 = load_words_dict("TESTS/tests_words_dict.txt")
BOARD_1 = [
    ['n', 'i', 'm', 'r'],
    ['a', 'a', 'd', 'o'],
    ['o', 'r', 'a', 'r'],
    ['r', 'r', 'd', 'e']
]
BOARD_2 = [
    ['a', 'b', 'c', 'd'],
    ['h', 'g', 'f', 'e'],
    ['i', 'j', 'k', 'l'],
    ['p', 'o', 'n', 'm']
]
BOARD_3 = [
    ['n', 'qu', 'e', 'r'],
    ['a', 'a', 's', 'o'],
    ['o', 'r', 't', 'r'],
    ['r', 'r', 'd', 'e']
]

nimrod = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 2)]
or_1, or_2, or_3, or_4, or_5 = [(2, 0), (2, 1)], [(1, 3), (2, 3)], [(1,3), (0,3)], [(2,0), (3,0)], [(2,0), (3,1)]
naor = [(0, 0), (1, 0), (2, 0), (3, 0)]
dre = [(3, 2), (2, 3), (3, 3)]
dr_dre = [(1, 2), (2, 1), (3, 2), (2, 3), (3, 3)]
more = [(0, 2), (1, 3), (2, 3), (3, 3)]
ora_1 = [(2, 0), (2, 1), (1, 1)]
ora_2 = [(2, 0), (2, 1), (1, 0)]
dad_1 = [(3, 2), (2, 2), (1, 2)]
dad_2 = [(1, 2), (2, 2), (3, 2)]
all_chars_1 = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2), (1,1), (1,0), (2,0),
              (2,1), (2,2), (2,3), (3,3), (3,2), (3,1), (3,0)]
all_chars_2 = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2), (1,1), (1,0), (2,0),
               (3, 1), (2, 2), (2, 3), (3, 3), (3, 2), (2, 1), (3, 0)]
double_char = [(0,1), (0,2), (1,2), (2,2)]
invalid_1 = [(-1, 13), (25, 2), (0, 0)]
invalid_2 = [(0, 0), (0, 1), (1, 1)]
invalid_3 = [(0,0), (1,3)]
invalid_dred = [(3,2), (2,3),(3,3), (3,2)]


def test_load_words_dict():
    assert load_words_dict("TESTS\load_dict_test_text.txt") == {"or": True, "o":
                            True, "m m": True, "ss": True, "    ab": True}


def test_is_valid_path():
    assert is_valid_path(BOARD_1, nimrod, WORDS_1) == "nimrod"
    assert is_valid_path(BOARD_1, or_1, WORDS_1) == "or"
    assert is_valid_path(BOARD_1, or_2, WORDS_1) == "or"
    assert is_valid_path(BOARD_1, naor, WORDS_1) == "naor"
    assert is_valid_path(BOARD_1, dre, WORDS_1) == "dre"
    assert is_valid_path(BOARD_1, more, WORDS_1) == "more"
    assert is_valid_path(BOARD_1, ora_1, WORDS_1) == "ora"
    assert is_valid_path(BOARD_1, ora_2, WORDS_1) == "ora"
    assert is_valid_path(BOARD_1, dad_1, WORDS_1) == "dad"
    assert is_valid_path(BOARD_1, dad_2, WORDS_1) == "dad"
    assert is_valid_path(BOARD_1, dr_dre, WORDS_1) == "drdre"
    assert is_valid_path(BOARD_1, all_chars_1, WORDS_1) == "nimrodaaoraredrr"
    assert is_valid_path(BOARD_2, all_chars_1, WORDS_1) == "abcdefghijklmnop"
    assert is_valid_path(BOARD_3, double_char, WORDS_1) == "quest"
    assert is_valid_path(BOARD_1, invalid_1, WORDS_1) is None
    assert is_valid_path(BOARD_1, invalid_2, WORDS_1) is None
    assert is_valid_path(BOARD_1, invalid_3, WORDS_1) is None
    assert is_valid_path(BOARD_1, invalid_dred, WORDS_1) is None


def test_possible_cells():
    path_1 = [(0,0), (0,1)]
    path_2 = [(0,0), (0,1), (1,1)]
    path_3 = [(0,0), (0,1), (1,1), (1,0)]
    path_4 = [(0,1), (1,1), (1,0), (0,0)]

    assert sorted(possible_cells(path_1, BOARD_1)) == sorted([(0,2), (1,0), (1,1), (1,2)])
    assert sorted(possible_cells(path_2, BOARD_1)) == sorted([(1,0), (0,2), (1,2), (2,0), (2,1), (2,2)])
    assert sorted(possible_cells(path_3, BOARD_1)) == sorted([(2,0), (2,1)])
    assert sorted(possible_cells(path_4, BOARD_1)) == []
    assert sorted(possible_cells(all_chars_1, BOARD_1)) == []


def test_find_length_n_words():
    find_6 = find_length_n_words(6, BOARD_1, WORDS_1)
    assert sorted(find_6) == sorted([("nimrod", nimrod)])
    find_16 = find_length_n_words(16, BOARD_1, WORDS_1)
    assert sorted(find_16) == sorted([("nimrodaaoraredrr", all_chars_1),(("nimrodaaoraredrr", all_chars_2))])
    find_16_abc = find_length_n_words(16, BOARD_2, WORDS_1)
    assert sorted(find_16_abc) == sorted([("abcdefghijklmnop", all_chars_1)])
