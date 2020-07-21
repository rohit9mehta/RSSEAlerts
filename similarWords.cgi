#!/usr/bin/env python
import cgi;
import cgitb;cgitb.enable()
print("Content-Type: text/plain;charset=utf-8")
print()

print("Hello World!")

import nltk
import nltk.text
import nltk.corpus
import sys
import io
import readRSS
import re
import json

import mysql.connector

def similarWords():
    print("program started")
    try:
        cnx = mysql.connector.connect(host="162.244.65.29:3306", user="userprefs", password="iz2X6z1^", database="admin_")
        cursor = cnx.cursor()
        cursor.execute("SELECT email, preferences FROM userInput")   # Syntax error in query
        cnx.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    print("Able to read")
    myresult = mycursor.fetchall()

    dbDict = {}
    for x in myresult:
        for each in x:
            email = x[0]
            listOfDictionaries = x[1]
            for dictionary in listOfDictionaries:
                word = list(dictionary.values())[0]
                dbDict.setdefault(email, [])
                dbDict[email] += [word]

    allWords = []
    for x in dbDict.keys():
        allWords += dbDict[x]

    setOfWordsString = ''
    for x in allWords:
        x = re.sub(r'[^\w\s]','', x)
        setOfWordsString += x

    setOfWords = list(set(setOfWordsString.split()))
    #print(setOfWords)
    dictOfWords = {x: 0 for x in setOfWords}
    readRSS.reader('https://www.planeteria.com/feed/')
    with open('test.json') as articles:
        dbOfArticles = json.load(articles)
    for x in dbOfArticles.values():
        x = x.lower()
    # dbOfArticles = open('test.txt').read().lower()
    indexOfWords = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
    save = []
    tokens = ''
    dictOfSimilarWords = {}
    userList = []
    userToArticle = {}
    #print(indexOfWords.similar("launch"))
    similar_words = []
    exact_words = []
    #so far for one input of tags (1 user). To expand, we would get tags from 
    #mult sources and assign each tag to the user tag maybe in a dictionary
    for x in setOfWords:
        # print(x)
        for word in nltk.word_tokenize(x):
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
    for x in list(dbOfArticles):
        for eachWord in nltk.word_tokenize(dbOfArticles[x]):
            eachWord = eachWord.lower()
            # if (eachWord.isdigit() and len(eachWord) == 3):
            #     key = int(eachWord)
            #     untilNextItem = False
            if untilNextItem:
                continue
            for word in exact_words:
                if word == eachWord:
                    userList.append(x)
                    dictOfWords[word] = x
                    untilNextItem = True
                    break
            for word in similar_words:
                if word == eachWord:
                    score += 1
        

    #similar words finding: have to find algo
    # if score / len(dbOfArticles) > 0.05:
    #     userList.append(key)
    #     dictOfWords[word] = key
    #     untilNextItem = True
    for i in list(dictOfWords):
        if dictOfWords[i] == 0:
            dictOfWords.pop(i)
    # print(userList)
    print(dictOfWords)


    # for users in userPrefs that have a word that is a key in dictOfWords:
    #     key: userID, value: article ID (dictofWords[word])
    #     dump as json file
    # with open('userPrefsDict.json') as f:
    #     dbDict = json.load(f)

    sql = "INSERT INTO userArticleMappings (userID, keywords, articles) VALUES (%s, %s, %s)"
    val = []
    for x in list(dbDict):
        email = x
        keywords = re.sub(r'[^\w\s]','', dbDict[x])
        article = dbOfArticles[x]
        val += [(email, keywords, article)]

    mycursor.executemany(sql, val)

    mydb.commit()

# for user in list(dbDict):
#     usersWordsString = ''
#     x = re.sub(r'[^\w\s]','', dbDict[user])
#     usersWordsString += x
#     usersWords = list(set(usersWordsString.split()))
#     for i in usersWords:
#         if i in list(dictOfWords):
#             userToArticle[user] = dictOfWords[i]
#             with open('userToArticle.json', 'w') as theFile:
#                 json.dump(userToArticle, theFile)

#####


# # db = open('userPrefs.txt', 'r').read().lower()
# setOfWordsString = ''
# with open('userPrefsDict.json') as f:
#     dbDict = json.load(f)
# for x in dbDict.values():
#     x = re.sub(r'[^\w\s]','', x)
#     setOfWordsString += x
# setOfWords = list(set(setOfWordsString.split()))
# print(setOfWords)
# dictOfWords = {x: 0 for x in setOfWords}
# readRSS.reader('https://www.planeteria.com/feed/')
# with open('test.json') as articles:
#     dbOfArticles = json.load(articles)
# for x in dbOfArticles.values():
#     x = x.lower()
# # dbOfArticles = open('test.txt').read().lower()
# indexOfWords = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
# save = []
# tokens = ''
# dictOfSimilarWords = {}
# userList = []
# userToArticle = {}
# #print(indexOfWords.similar("launch"))
# similar_words = []
# exact_words = []
# #so far for one input of tags (1 user). To expand, we would get tags from 
# #mult sources and assign each tag to the user tag maybe in a dictionary
# for x in setOfWords:
#     # print(x)
#     for word in nltk.word_tokenize(x):
#         word = word.lower()
#         exact_words.append(word)
#         orig_stdout = sys.stdout
#         out = io.StringIO()
#         sys.stdout = out
#         indexOfWords.similar(word)
#         storable_output = out.getvalue()
#         sys.stdout = orig_stdout
#         similar_words.extend(storable_output.split())
#         #print(storable_output)
#         similar_words = list(set(similar_words))
#         #save.append(indexOfWords.similar_words(word))

# score = 0
# key = 0
# counter = 0
# untilNextItem = False
# for x in list(dbOfArticles):
#     for eachWord in nltk.word_tokenize(dbOfArticles[x]):
#         eachWord = eachWord.lower()
#         # if (eachWord.isdigit() and len(eachWord) == 3):
#         #     key = int(eachWord)
#         #     untilNextItem = False
#         if untilNextItem:
#             continue
#         for word in exact_words:
#             if word == eachWord:
#                 userList.append(x)
#                 dictOfWords[word] = x
#                 untilNextItem = True
#                 break
#         for word in similar_words:
#             if word == eachWord:
#                 score += 1
    

# #similar words finding: have to find algo
# # if score / len(dbOfArticles) > 0.05:
# #     userList.append(key)
# #     dictOfWords[word] = key
# #     untilNextItem = True
# for i in list(dictOfWords):
#     if dictOfWords[i] == 0:
#         dictOfWords.pop(i)
# # print(userList)
# print(dictOfWords)


# # for users in userPrefs that have a word that is a key in dictOfWords:
# #     key: userID, value: article ID (dictofWords[word])
# #     dump as json file
# with open('userPrefsDict.json') as f:
#     dbDict = json.load(f)

# for user in list(dbDict):
#     usersWordsString = ''
#     x = re.sub(r'[^\w\s]','', dbDict[user])
#     usersWordsString += x
#     usersWords = list(set(usersWordsString.split()))
#     for i in usersWords:
#         if i in list(dictOfWords):
#             userToArticle[user] = dictOfWords[i]
#             with open('userToArticle.json', 'w') as theFile:
#                 json.dump(userToArticle, theFile)