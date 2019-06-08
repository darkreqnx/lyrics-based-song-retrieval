from nltk.tokenize import word_tokenize
import pprint
import json
import re
from collections import defaultdict
import back.utils.spellcheck as spellcheck
import back.utils.soundex as soundex

clustered = defaultdict(list)


def soundex_check(tok):
    if tok.find('\\') > 0:
        print('Soundex on {tok}')
        return True


def add_trial(l, pos1, pos2):

    if not l:
        li = []
        li.append(pos1)
        li.append(pos2)

        l.append(li)
        return

    for x in l:
        if x[len(x) - 1] == pos1:
            x.append(pos2)
            return

    li = []
    li.append(pos1)
    li.append(pos2)
    l.append(li)


def pos_intersect(p1, p2, k):

    doc1 = p1["doc"]
    len1 = len(doc1)
    doc2 = p2["doc"]
    len2 = len(doc2)

    i = j = 0

    while i != len1 and j != len2:

        if doc1[i] == doc2[j]:
            li = []

            pos1 = p1[doc1[i]]
            lp1 = len(pos1)
            pos2 = p2[doc2[j]]
            lp2 = len(pos2)

            ii = jj = 0

            while ii != lp1:

                while jj != lp2:

                    if abs(pos1[ii] - pos2[jj]) <= k:

                        li.append(pos2[jj])

                    elif pos2[jj] > pos1[ii]:
                        break

                    jj += 1

                while li != [] and abs(li[0] - pos1[ii]) > k:
                    li.remove(li[0])

                for ps in li:

                    add_trial(clustered[doc1[i]], pos1[ii], ps)

                ii += 1
            i += 1

            j += 1

        elif doc1[i] < doc2[j]:
            i += 1

        else:
            j += 1

    return clustered

def loadJSON():
    print("Loading Index...")
    with open("back/index.json") as f:
        ind = json.load(f)

    print("Load Complete")



def search(query,ind ):

    normalised = ""

    for k in query.split("\n"):
        normalised += re.sub(r"[^a-zA-Z0-9' ]+", '', k).lower()
        normalised += "\n"

    tokens = word_tokenize(normalised)

    i = 0
    while i < len(tokens):
        x = spellcheck.corrected(tokens[i])

        if x != tokens[i]:
            tokens[i] = x
            print('Changed to {tokens[i]}')

        i += 1

    print(tokens)

    for x in tokens:
        if x not in ind.keys():
            print('{x} not in Corpus ')
            tokens.remove(x)

    print(tokens)

    i = 0
    while i < len(tokens) - 1:
        pos_intersect(ind[tokens[i]], ind[tokens[i + 1]], 1)
        i += 1

    n = len(tokens)
    counts = defaultdict(list)
    ranks = defaultdict(int)

    pprint.pprint(clustered)
# Excludes pair only results
    # for index, key in enumerate(clustered):

    #     lis = clustered[key]
    #     for x in lis:

    #         if len(x) < 3:

    #             lis.remove(x)

# Counting the number of phrases recorded
    for index, key in enumerate(clustered):
        counts[key] = [0] * (n + 1)
        i = 0
        lis = clustered[key]
        while i < len(lis):

            counts[key][len(lis[i])] += 1
            i += 1

    for index, key in enumerate(counts):
        i = 0
        r = 0
        while i < len(counts[key]):
            r += i * i * i * i * counts[key][i]
            i += 1

        ranks[key] = r

    ranks = sorted(ranks.items(), key=lambda kv: kv[1], reverse=True)

    resultdocs = []
    i = 0
    for key, value in ranks:
        if i > 20:
            break
        resultdocs.append(key)
        # pprint.pprint(clustered[key])
        i += 1

    pprint.pprint(resultdocs)
    return resultdocs, clustered

    # check = str(input("\nAnother Query? (Y / n)"))

    # if check == 'n':
    #     i = 0
