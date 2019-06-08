import re
from collections import defaultdict
import json


def index(str_input):
	result = str_input[0].upper()

	str_input = re.sub('[hw]', '', str_input, flags=re.I)
	str_input = re.sub('[bfpv]+', '1', str_input, flags=re.I)
	str_input = re.sub('[cgjkqsxz]+', '2', str_input, flags=re.I)
	str_input = re.sub('[dt]+', '3', str_input, flags=re.I)
	str_input = re.sub('l+', '4', str_input, flags=re.I)
	str_input = re.sub('[mn]+', '5', str_input, flags=re.I)
	str_input = re.sub('r+', '6', str_input, flags=re.I)


	str_input = str_input[1:]

	str_input = re.sub('[aeiouy]','', str_input, flags=re.I)

	result += str_input[0:3]

	if len(result) < 4:
	    result += '0'*(4-len(result))

	return result

def build_soundex():
	dictionary = defaultdict(list)
	with open("index.json") as f:
		ans = json.load(f)
	f.close()
	for key in ans:
		value = index(key)
		dictionary[value].append(key)
	with open("soundex.json", 'w') as f:
		json.dump(dictionary, f)
	f.close()

def similar_words(index_val):
	with open("soundex.json") as f:
		ans = json.load(f)
	f.close()
	return ans[index_val]

if __name__ == '__main__':
	check = input("Build?\n")
	if check == 'y':
		build_soundex()
	word = input("Type something\n")
	print(sorted(similar_words(index(word))))


