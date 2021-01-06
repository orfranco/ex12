from ex12_utils import *
from boggle_board_randomizer import *

WORDS_1 = load_words_dict("TESTS/tests_words_dict.txt")
BOARD_1 = [
    ['n', 'i', 'm', 'r'],
    ['a', 'a', 'd', 'o'],
    ['o', 'r', 'a', 'r'],
    ['r', 'r', 'd', 'e']
]


def test_load_words_dict():
    assert load_words_dict("TESTS\load_dict_test_text.txt") == {"or": True, "o":
                            True, "m m": True, "ss": True, "    ab": True}


def test_is_valid_path():
    nimrod = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2)]
    or_1, or_2 = [(2,0), (2,1)], [(1,3), (2,3)]
    naor = [(0,0), (1,0), (2,0), (3,0)]
    dre = [(3,2), (2,3), (3,3)]
    more = [(0,2), (1,3), (2,3), (3,3)]
    ora_1 = [(2,0), (2,1), (1,1)]
    ora_2 = [(2,0), (2,1), (1,0)]
    dad_1 = [(3,2), (2,2), (1,2)]
    dad_2 = [(1,2), (2,2), (3,2)]
    invalid_1 = [(-1,13), (25,2), (0,0)]
    invalid_2 = [(0,0), (0,1), (1,1)]

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
    assert is_valid_path(BOARD_1, invalid_1, WORDS_1) is None
    assert is_valid_path(BOARD_1, invalid_2, WORDS_1) is None


