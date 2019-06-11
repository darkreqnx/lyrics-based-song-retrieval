# Lyrics-based Song Retrieval

The application is designed to retrieve information about a song given the user knows more than two words from its lyrics. Retrieved information includes song name, artist name, lyrics, and a link to the page from which the lyrics were drawn from. Primarily engineered using NLTK and PyQT.

## General Specs/Installation
* Download dataset from https://www.kaggle.com/mousehead/songlyrics and rename it as songdata.csv and store it in data/
* Download Dependencies with the yml file 
* PyQt5 is a must for the GUI to run
* Run indexer.py - The script builds the index and stores it in the same directory as index.json
* Run app.py to launch application window - Startup Time takes atleast 15s as it loads the index and the song data

## Application Architecture

On the highest level, the application can be broken down into an Indexer, a Search operator, a Ranking mechanism, and the basic user interface.

### Indexer
The first step towards indexing the corpus is tokenising the lyrics of all the songs in the dataset. Besides the lyrics, the dataset includes the song id, song name, artist, artist gender, and a link to the source of the lyrics. The lyrics are tokenised into singleton terms, and then indexed using positional indexing. In general, for any term t<sub>i</sub>, doc ids d<sub>i</sub>, and occurrences p<sub>i</sub> (for n occurrences),

t<sub>i</sub> : d<sub>i</sub> : p<sub>1</sub>, p<sub>2</sub>, p<sub>3</sub>, ….., p<sub>i</sub>, ….., p<sub>n</sub>

denotes the method the indexer stores the positional indexes for every term’s occurrences.

The final results of the positional indexing operation are stored as a JSON file.

### Search

The query is split into biwords and searched with a proximity constant k, which denotes how far apart the constituents of the biword are from each other. In other words, the smaller the k value, the closer the phrase is to a potential search result. Also, the application processes a string through a spell check and phonetic mapping to minimise user error.

#### Spell Check using Edit Distance

Each word of the user query is first run through an edit distance module that first checks if that particular word is a case of poor spelling. If it isn’t, it returns the same term and checks the next. If it is a case of poor spelling, then it first checks for the term in the index, and returns the same term if found within the index. If not even found within the index, then the application runs the edit distance algorithm (each edit corresponds to a replacement, deletion, or addition):

E_dist1, E_dist2 (functions within the spell check module) consecutively check for edit distance corrections and replace the user query term with a term that it finds in the index. If E_dist1 (i.e. using one edit) is able to find any such term, then the spell check for that term terminates right there. Only in the case of an event where E_dist1 finds no words to replace the current term, will it pass on to E_dist2 which keeps a target of finding a suitable replacement in two edits.

The final choice for the word is made based on the probability of occurrence in the index. E_dist1 and E_dist2 don’t directly replace words but add “candidate” replacements to a list, and then a pick one among them based on higher probability of occurrences.

#### Phonetic tolerance using Soundex Codes

On the chance that even E_dist1 and E_dist2 are not able to find any replacements from within the index, then it is probable that the user’s mistake lies with his/her phonetic interpretation of the lyric and not the spelling. For this, we compare the Soundex code for that particular term to those of all the indexed terms and see if it can return any.

Similar to the edit distance module, this too chooses the replacement term that has the highest probability of occurrence.

### Merge and Ranking

Positional indices of each term in the biword are observed and recorded if occurring consecutively. Biword/triword/simultaneous occurrences are recorded as lists with position elements.

e.g. query: “in the cloud”

Biwords here would be “in the” and “the cloud”. Let’s say positions recorder are [71, 72], and [72, 73] among many others. Then these would be merged to an inner list [71, 72, 73], thus, a list of lists would constitute the value part of a key-value dictionary. Ranking is based on two metrics, first on the length of the inner strings, and secondly on the number of such lists. After empirical trials, it was found that the equation

r<sub>i</sub> = (lengthi)<sup>4</sup> x n(occurence<sub>i</sub>)

returned the better rank. Here, r<sub>i</sub> = contribution to rank of song from the ith inner list, length<sub>i</sub> = length of inner list i, n(occurence<sub>i</sub>) = number of times an inner list of the same length occurs. Based on this, the songs are ranked and returned accordingly to the front end.

---
_The corpus in its raw form is a .csv file with over 55,000 songs, with headers: id, song_name, lyric_link, lyric_text, and artist_gender._
_Pre-processing involves curating data from the corpus for efficient indexing. For this, the text was regularised into lower case, all punctuation marks and articles were also removed._


_Completed in collaboration with [Monith Sourya](https://github.com/monith-sourya), [Sanjay Devprasad](https://github.com/Sanjay-D), and [Vishnu Teja](https://github.com/vishnteja)._
