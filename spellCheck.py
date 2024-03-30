import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

allWord = Counter(words(open('katadasar.txt').read()))

def wordProbability(word, N=sum(allWord.values())):
    return allWord[word] / N

def correction(word):
    return max(candidates(word), key=wordProbability)

def candidates(word):
    # return (known([word]) or [word])
    return (known([word]) or known(basicEdit(word)) or [word])
    # return (known([word]) or known(basicEdit(word)) or known(doubleEdit(word)) or [word])

def known(words):
    return set(w for w in words if w in allWord)

def basicEdit(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces = [L + c + R[1:] for L, R in splits for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]    
    return set(deletes + transposes + replaces + inserts)

def doubleEdit(word):
    return (e2 for e1 in basicEdit(word) for e2 in basicEdit(e1))