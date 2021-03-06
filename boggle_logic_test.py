from boggle_logic import *
from ex12_utils import load_words_dict


def test_convert_to_minutes_format():
    assert convert_to_minutes_format(130) == "2:10"
    assert convert_to_minutes_format(131) == "2:11"
    assert convert_to_minutes_format(171) == "2:51"
    assert convert_to_minutes_format(180) == "3:00"
    assert convert_to_minutes_format(3) == "0:03"


# def test_timer():
#     timer = Timer(180)
#     timer.start_timer()
#     for i in range(3):
#         time.sleep(1)
#         assert timer.get_time() == f"2:{59 - i}"


