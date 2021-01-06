def load_words_dict(file_path):
    words_dict = dict()

    with open(file_path, 'r') as words_file:
        line = words_file.readline().replace("\n", "")
        while line:
            words_dict[line] = True
            line = words_file.readline().replace("\n", "")

    return words_dict


def is_valid_path(board, path, words):
    pass


def find_length_n_words(n, board, words):
    pass

print(load_words_dict("README"))