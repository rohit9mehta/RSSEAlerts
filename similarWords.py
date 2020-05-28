import nltk
import nltk.text
import nltk.corpus
import sys
import io
import readRSS

db = open('userPrefs.txt', 'r').read().lower()
readRSS.reader('https://www.planeteria.com/feed/')
dbOfArticles = open('test.txt').read().lower()
indexOfWords = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
save = []
tokens = ''
dictOfSimilarWords = {}
userList = []
#print(indexOfWords.similar("launch"))
similar_words = []
exact_words = []
#so far for one input of tags (1 user). To expand, we would get tags from 
#mult sources and assign each tag to the user tag maybe in a dictionary
for word in nltk.word_tokenize(db):
    word = word.lower()
    exact_words.append(word)
    orig_stdout = sys.stdout
    out = io.StringIO()
    sys.stdout = out
    indexOfWords.similar(word)
    storable_output = out.getvalue()
    sys.stdout = orig_stdout
    similar_words.extend(storable_output.split())
    #print(storable_output)
    similar_words = list(set(similar_words))
    #save.append(indexOfWords.similar_words(word))

score = 0
key = 0
counter = 0
untilNextItem = False
for eachWord in nltk.word_tokenize(dbOfArticles):
    eachWord = eachWord.lower()
    if (eachWord.isdigit() and len(eachWord) == 3):
        key = int(eachWord)
        untilNextItem = False
    if untilNextItem:
        if not all((eachWord.isdigit(), len(eachWord) == 3)):
            continue
    for word in exact_words:
        if word == eachWord:
            userList.append(key)
            untilNextItem = True
            break
    for word in similar_words:
        if word == eachWord:
            score += 1

    if score / len(dbOfArticles) > 0.05:
        userList.append(key)
        untilNextItem = True
print(userList)

#indexOfWords.similar("monstrous")

#print(indexOfWords.similar_words("website"))
# with open("test2.txt", 'r') as file:
#     for line in file:
#         tokens += ", ".join(indexOfWords.similar_words(word))
#     # for line in file:
#     #     tokens+=",".join(nltk.word_tokenize(line))
#
# save.append(indexOfWords.similar_words('woman'))
#