# Python Program to implement
# the above approach
from collections import deque
from typing import Deque, List, Set
import sys


def get_file_name():
    file_name = sys.argv[3]
    return file_name


def read_word_file(file_name):
    words_list = []
    with open(file_name) as file:
        for word in file.readlines():
            words_list.append(word.strip())
    return words_list


# Function to print all possible shortest
# sequences starting from start to target.
def displaypath(res: List[List[str]]):
    for i in res:
        print("[ ", end="")
        for j in i:
            print(j, end=", ")
        print("]")


# Find words differing by a single
# character with word
def addWord(word: str, Dict: Set):
    res: List[str] = []
    wrd = list(word)

    # Find next word in dict by changing
    # each element from 'a' to 'z'
    for i in range(len(wrd)):
        s = wrd[i]
        c = 'a'
        while c <= 'z':
            wrd[i] = c
            if ''.join(wrd) in Dict:
                res.append(''.join(wrd))
            c = chr(ord(c) + 1)
        wrd[i] = s
    return res


# Function to get all the shortest possible
# sequences starting from 'start' to 'target'
def wordSearch(beginWord, endWord, Dictt):
    # Store all the shortest path.
    res: List[List[str]] = []

    # Store visited words in list
    visit = set()

    # Queue used to find the shortest path
    q: Deque[List[str]] = deque()

    # Stores the distinct words from given list
    Dict = set()
    for i in Dictt:
        Dict.add(i)
    q.append([beginWord])

    # Stores whether the shortest
    # path is found or not
    flag = False
    while q:
        size = len(q)
        for i in range(size):

            # Explore the next level
            cur = q[0]
            q.popleft()
            newadd = []

            # Find words differing by a
            # single character
            newadd = addWord(cur[-1], Dict)

            # Add words to the path.
            for j in range(len(newadd)):
                newline = cur.copy()
                newline.append(newadd[j])

                # Found the target
                if (newadd[j] == endWord):
                    flag = True
                    res.append(newline)

                visit.add(newadd[j])
                q.append(newline)

        # If already reached target
        if (flag):
            break

        # Erase all visited words.
        for it in visit:
            Dict.remove(it)
        visit.clear()
    return res


if __name__ == '__main__':
    start = sys.argv[1]
    target = sys.argv[2]
    filename = get_file_name()
    words_list = read_word_file(file_name=filename)

    res = wordSearch(start, target, words_list)
    displaypath(res)
