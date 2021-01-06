from ex12_utils import *

def test_load_words_dict():
    assert load_words_dict("load_dict_test_text.txt") == {"or": True, "o":
                            True, "m m": True, "ss": True, "    ab": True}

def test_is_valid_path():
    pass
