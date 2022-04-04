import collections
from collections import defaultdict
from collections import deque
import sys


class WordLadder:
    def __init__(self, start, end, wordList):
        self.start = start
        self.end = end
        self.wordList = wordList

    def find(self):
        pathlst = self.ladder(self.start, self.wordList)
        return (pathlst + [self.end])

    def ladder(self, begin, wordList):
        pattern = self.doMatch(begin, self.end)
        if self.counts(pattern) != None:
            return ([begin])

        wlist = []
        for word in wordList:
            wpat = self.doMatch(begin, word)
            indx = self.counts(wpat)
            if indx != None:
                if wpat[indx] == pattern[indx]:
                    wlist.insert(0, word)
                else:
                    wlist.append(word)

        shortest_path = []
        for word in wlist:
            pattern = self.doMatch(begin, word)
            if self.counts(pattern) != None:
                remain = wordList[:]
                remain.remove(word)
                pathlst = self.ladder(word, remain)
                if shortest_path == []:
                    shortest_path = pathlst
                elif pathlst != [] and (len(pathlst) <= len(shortest_path)):
                    shortest_path = pathlst
        if shortest_path != []:
            return ([begin] + shortest_path)
        else:
            return ([])

    def doMatch(self, wordl, wordr):
        pattern = []
        for (cl, cr) in zip(wordl, wordr):
            if cl == cr:
                pattern.append('*')
            else:
                pattern.append(cr)
        return ("".join(pattern))

    def counts(self, pattern):
        # return (len(pattern) - pattern.count('*') == 1)
        counts = len(pattern) - pattern.count('*') == 1
        if not counts:
            return (None)
        else:
            for i, c in enumerate(pattern):
                if c != '*':
                    return (i)


if __name__ == '__main__':
    start = sys.argv[1]
    end = sys.argv[2]
    filename = sys.argv[3]
    # words_list = read_word_file(file_name=filename)
    wordList = []
    with open(filename) as file:
        for word in file.readlines():
            wordList.append(word.strip())

    wl = WordLadder(start, end, wordList)
    print(wl.find())
