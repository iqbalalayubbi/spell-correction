import re
from collections import Counter
import sys, os
import numpy as np

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


kamusPath = resource_path('autocorrect.txt')

def words(text): return re.findall(r'\w+', text.lower())

allWord = Counter(words(open(kamusPath).read()))

def wordProbability(word, N=sum(allWord.values())):
    return allWord[word] / N

def correction(word):
    return max(candidates(word), key=wordProbability)

def candidates(word):
    # return (known([word]) or [word])
    # return (known([word]) or known(basicEdit(word)) or [word])
    return (known([word]) or known(basicEdit(word)) or known(doubleEdit(word)) or [word])

def known(words):
    return set(w for w in words if w in allWord)

def basicEdit(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    # makan -> akan, mkan
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    # makan -> amkan, mkaan
    replaces = [L + c + R[1:] for L, R in splits for c in letters]
    # makan -> bakac
    inserts = [L + c + R for L, R in splits for c in letters]
    # makan -> amakan, makana
    return set(deletes + transposes + replaces + inserts)

def doubleEdit(word):
    return (e2 for e1 in basicEdit(word) for e2 in basicEdit(e1))