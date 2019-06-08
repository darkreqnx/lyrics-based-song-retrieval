
import re
from collections import Counter

def all_words(text): return re.findall(r'\w+', text.lower())

DICT = Counter(all_words(open('back/utils/lyrics.txt').read()))

def Prob(w, N=sum(DICT.values())): 
    
    return DICT[w] / N

def corrected(w): 
    
    return max(possibilities(w), key=Prob)

def possibilities(w): 
    
    return (present([w]) or present(e_dist1(w)) or present(e_dist2(w)) or [w])

def present(w): 
    
    return set(i for i in w if i in DICT)

def e_dist1(w):
   
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    split = [(w[:i], w[i:]) for i in range(len(w) + 1)]
    delete = [L + R[1:] for L, R in split if R]
    transpose = [L + R[1] + R[0] + R[2:] for L, R in split if len(R)>1]
    replace = [L + c + R[1:] for L, R in split if R for c in alphabet]
    insert = [L + c + R for L, R in split for c in alphabet]
    return set(delete + transpose + replace + insert)

def e_dist2(w): 
    
    return (e2 for e1 in e_dist1(w) for e2 in e_dist1(e1))

def e_dist3(w):

	return (e3 for e1 in e_dist1(w) for e2 in e_dist1(e1) for e3 in e_dist1(e2))

if __name__ == '__main__':
	while True:
		word = input("Enter incorrect word\n")
		print(corrected(word))
		check = input("one more?\n")
		if check == 'n':
			break