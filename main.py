#!/usr/bin/python3.3
import codecs
import numpy as np
from numpy.random import choice
import re
import sys

class ParseTXT(object):
    def __init__(self, fileName, nb=20, length=7):
        self._fileName = fileName
        self._nb = int(nb)
        self._length = int(length)
        self._count = np.zeros((256, 256, 256), dtype='int32')

    def start(self):
        with codecs.open(self._fileName, "r", encoding="latin-1") as lines:
            for w in lines:
                word = re.split("\n", w)[0]
                if word.find(" "):
                    word = re.split(" ", w)[0]
                i = 0
                j = 0
                for k in [ord(c) for c in list(word)]:
                    self._count[i, j, k] += 1
                    i = j
                    j = k

    def generatWords(self):
        s = self._count.sum(axis=2)
        st = np.tile(s.T, (256, 1, 1)).T
        prob = self._count.astype(dtype='float', order='C', casting='unsafe') / st
        prob[np.isnan(prob)] = 0
        nb = 0
        while not nb == self._nb:
            i = 0
            j = 0
            a = 0
            res = ""
            while not a == self._length:
                k = choice(range(256), 1, p=prob[i, j , :])[0]
                res += str(chr(k))
                i = j
                j = k
                a += 1
            print(res)
            nb += 1
if len(sys.argv) >= 3:
    try:
        #test = ParseTXT("./liste.de.mots.francais.frgut.txt", sys.argv[1], sys.argv[2])
        test = ParseTXT("./dictionnaire_adjectifs_fr_freq.txt", sys.argv[1], sys.argv[2])
        test.start()
        test.generatWords()
    except ValueError:
        print("ERROR")
        exit(42)
else:
    test = ParseTXT("./dictionnaire_adjectifs_fr_freq.txt", 20, 7)
    test.start()
    test.generatWords()
exit(0)