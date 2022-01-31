"""
file: hw1.py
description: CSCI 630, HW 1-P
language: Python
author: Abhishek Shah, as5553@rit.edu
"""


import collections
from collections import defaultdict
from collections import deque
import sys

def get_start_word():
    """
    This method will return the begin word
    """
    start = sys.argv[1]
    return start

def get_target_word():
    """
    This method will return the target word
    """
    target = sys.argv[2]
    return target

def get_file_name():
    """
    This method will return the file name
    """
    file_name = sys.argv[3]
    return file_name

def read_word_file(file_name):
    """
    This method will read contents from the file
    """
    words_list = []
    with open(file_name) as file:
        for word in file.readlines():
            words_list.append(word.strip())
    return words_list


def wordSearch(beginWord, endWord, wordList):
    """
    This method prints the shortest list of words that connects the two given words
    """
    if endWord not in wordList or beginWord == endWord:
        print("No Solution")
        return 0

    # Create adjacency list
    neighbors = defaultdict(list)
    for word in wordList:
        for index in range(len(word)):
            pattern = word[:index] + "*" + word[index + 1:]
            neighbors[pattern].append(word)

    queue = deque([beginWord])
    visited = set([beginWord])
    depth = 1

    # Initiate BFS
    while queue:
        for _ in range(len(queue)):
            word = queue.popleft()
            if word == endWord:
                print(endWord)
                return depth
            for index in range(len(word)):
                pattern = word[:index] + "*" + word[index + 1:]

                # Visit Neighbors
                for neighbor in neighbors[pattern]:
                    if neighbor not in visited:
                        # print(neighbor)
                        visited.add(neighbor)
                        queue.append(neighbor)
        print(word)
        depth += 1 # node explored, depth++

    print("No Solution")
    return 0

if __name__ == '__main__':
    start = get_start_word()
    target = get_target_word()
    filename = get_file_name()
    words_list = read_word_file(file_name=filename)

    wordSearch(start, target, words_list)
