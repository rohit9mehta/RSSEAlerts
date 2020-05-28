import numpy
import random
import json
import pandas as pd

def chat():
    dictOfUsers = {}
    userID = 0
    print("Enter in keywords, separated by commas")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        else:
            wordsList = inp.split(",")
            dictOfUsers[userID] = wordsList
            userID += 1