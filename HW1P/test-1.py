import collections
import sys
from collections import deque


def read_word_file(file_name):
    words_list = []
    with open(file_name) as file:
        for word in file.readlines():
            words_list.append(word.strip())
    return words_list


def get_file_name():
    file_name = sys.argv[1]
    return file_name


if __name__ == '__main__':
    file_name = get_file_name()
    words_list = read_word_file(file_name=file_name)
