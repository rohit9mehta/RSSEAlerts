import nltk
import nltk.text
import nltk.corpus
import sys
import io

db = open('test2.txt', 'r').read()
indexOfWords = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
save = []
tokens = ''
dictOfSimilarWords = {}
#print(indexOfWords.similar("launch"))
similar_words = []
#so far for one input of tags (1 user). To expand, we would get tags from 
#mult sources and assign each tag to the user tag maybe in a dictionary
for word in nltk.word_tokenize(db):
    orig_stdout = sys.stdout
    out = io.StringIO()
    sys.stdout = out
    indexOfWords.similar(word)
    storable_output = out.getvalue()
    sys.stdout = orig_stdout
    similar_words.extend(storable_output.split())
    #print(storable_output)
    similar_words = set(similar_words)
    #save.append(indexOfWords.similar_words(word))

for article in articles:
    for word in exact_words:
        if word in article:
            add article to stack
    for word in similar_words:
        if word in article:
            score += 1

    if score is certain level:
        add article to stack
print(similar_words)


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