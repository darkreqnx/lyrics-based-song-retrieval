import csv
from nltk.tokenize import word_tokenize
from collections import defaultdict
import re
import utils.soundex as soundex

# import pprint
import json

ans = defaultdict(lambda: defaultdict(list))


def pos_intersect(p1, p2, k):
    answer = []

    doc1 = p1["doc"]
    len1 = len(doc1)
    doc2 = p2["doc"]
    len2 = len(doc2)

    i = j = 0

    while i != len1 and j != len2:
        if doc1[i] == doc2[i]:
            li = []

            pos1 = p1[doc1[i]]
            lp1 = len(pos1)
            pos2 = p2[doc2[i]]
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
                    answer.append([doc1[i], pos1[ii], ps])

                ii += 1
            i += 1

            j += 1

        elif doc1[i] < doc2[j]:
            i += 1

        else:
            j += 1

    return answer


# Indexer.
with open('../data/songdata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:

            normalised = ""

            for k in row[4].split("\n"):
                normalised += re.sub(r"[^a-zA-Z0-9' ]+", '', k).lower()
                normalised += "\n"

            tokens = word_tokenize(normalised)

            for index, token in enumerate(tokens):

                if not ans[token][row[0]]:
                    ans[token]["doc"].append(row[0])

                ans[token][row[0]].append(index)

            print('Processed {line_count} songs.')
            line_count += 1
            # if line_count == 3:
            #     break

word_count = 0

for index, key in enumerate(ans):
    ans[key]['doc'] = sorted(ans[key]['doc'])
    word_count += 1
    print('Processed {key}, Count : {word_count}')

# print and store index
# pprint.pprint(ans)

print("Writing to files")

w = csv.writer(open("output.csv", "w"))
for key, val in ans.items():
    w.writerow([key, val])

with open("index.json", 'w') as f:
    json.dump(ans, f)

print("Write Complete")

print("Building Soundex Index")

soundex.build_soundex()


print('Processed {line_count} songs. Completed')
