import tensorflow as tf

import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import readRSS
import json


module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
model = hub.load(module_url)
print ("module %s loaded" % module_url)
def embed(input):
  return model(input)


alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def plot_similarity(labels, keyword_labels, features, keyword_features, rotation, messages_):
  corr = np.inner(features, keyword_features)
  for word in keyword_labels:
    for wrd in word.split():
      for message_ in messages_:
        if wrd.lower() in message_.lower():
        #if wrd.lower() in message_.lower() and not re.search("\w", str(message_.lower()[message_.lower().index(wrd.lower()) + 1]) + str(message_.lower()[message_.lower().index(wrd.lower()) - 1])):
          corr[messages_.index(message_)][keyword_labels.index(word)] = 1

  print(corr)
  sns.set(font_scale=1.2)
  g = sns.heatmap(
      corr,
      xticklabels=keyword_labels,
      yticklabels=labels,
      vmin=0,
      vmax=1,
      cmap="YlOrRd")
  g.set_xticklabels(keyword_labels, rotation=rotation)
  g.set_title("Semantic Textual Similarity")
  return corr

def run_and_plot(message_ids_, messages_, keywords_):
  message_embeddings_ = embed(messages_)
  keyword_embeddings_ = embed(keywords_)
  #print(messages_[:10])
  # print(message_embeddings_)
  corr = plot_similarity(message_ids_, keywords_, message_embeddings_, keyword_embeddings_, 90, messages_)
  for articleIndex in range(len(corr)):
    for keywordCorrelationIndex in range(len(corr[articleIndex])):
      if corr[articleIndex][keywordCorrelationIndex] >= 0.1:
        keyword = keywords[keywordCorrelationIndex]
        article = message_ids[articleIndex]
        if article in articleToKeyword:
          articleToKeyword[article].append(keyword)
        else:
          articleToKeyword[article] = [keyword]
  for key, value in articleToKeyword.items():
    print(key, ' : ', value)

readRSS.reader('https://planeteria.com/feed')
with open('test.json') as articles:
    dbOfArticlesDict = json.load(articles)

messages = list(dbOfArticlesDict.values())
#     #542
#     "Coronavirus update. Dear valued client, With so much uncertainty at this time, we wanted to assure you of continuity with our services. As a company, we are taking measures to keep our employees and their families healthy and safe. Planeteria is uniquely set up to handle remote and virtual meetings because of the multiple geographic locations of.",
#     #235
#     "Lextran & BCRTA Transit Operators Launch New Sites With First Of Its Kind GTFS+ Integration Santa Rosa, CA, Release: April 7th, 2020. For Immediate release Lextran in Lexington, KY and Butler County Regional Transit Authority (BCRTA) in Hamilton, OH have both launched new websites, designed and developed by Planeteria Media. These sites focus on riders, potential riders, and the rider experience. The sites offer practical information for trip planning, schedules",
#     #989
#     "What Should Be the Top Priorities of an Inbound Marketing Campaign? As you start to learn about inbound marketing, you may wonder how you are supposed to accomplish all those tasks along with having time for your other duties. It helps to step back and focus on the top three priorities. SEO The top priority should be to improve your site\u2019s SEO. An active blog is [&#8230;]\nThe post What Should Be the Top Priorities of an Inbound Marketing Campaign? appeared first on Planeteria Media.",
#     #421
#     "How to Create a Positive Image of Your Construction Company Creating a positive image for your company is essential for a number of reasons. Everything from bringing in new customers to retaining old customers and meeting your revenue goals depends on your construction company\u2019s image. If your company has a negative public image or no image at all, it\u2019s more likely to be passed over [&#8230;]\nThe post How to Create a Positive Image of Your Construction Company appeared first on Planeteria Media.",
#     #498
#     "Website Launch Announcement \u2013 Watersavers Irrigation Inc. Website launch announcement! Watersavers Irrigation Inc. recently launched their new website!\nThe post Website Launch Announcement &#8211; Watersavers Irrigation Inc. appeared first on Planeteria Media.",
#     #359
#     "Website Launch Announcement \u2013 Meydenbauer Center The Meydenbauer Center opened in 1993 as the Greater Seattle area\u2019s second largest convention facility. Meydenbauer Center was built to grow and sustain Bellevue\u2019s economic vitality. The Center includes 54,000 square-feet of event space including 36,000 square foot Center Hall, and nine meeting rooms totaling 12,000 square-feet. Also included is a 2,500 square-foot Executive Conference [&#8230;]\nThe post Website Launch Announcement &#8211; Meydenbauer Center appeared first on Planeteria Media.",
#     #861
#     "Happy New Year from Planeteria Happy New Year from our team to yours. How are you celebrating the New Year? As we head into 2020, here at Planeteria, we are celebrating our 20th successful year in business and we expecting 2021 to come with some grand goals to make it the best year yet. Thanks to our clients, old and [&#8230;]\nThe post Happy New Year from Planeteria appeared first on Planeteria Media.",
#     #799
#     "Website Strategy & Social Media Content Calendar &#x1f4c5;\u00a0Free Website Strategy &#38; Social Media Content Calendar Planner Designed for Municipalities and Private Enterprise Organizations https://www.planeteria.com/deskcalendar/ This desk calendar can help you with day to day content planning and overall website strategy. As a marketing professional, website manager or content creator this calendar can sit on your desk and help you single everyday. How [&#8230;]\nThe post Website Strategy &#038; Social Media Content Calendar appeared first on Planeteria Media.",
#     #250
#     "Website Launch Announcement \u2013 Belcampo Belcampo is a farm, butcher shop, and restaurant experience. Since 2012, they\u2019ve led the way in reinventing how things are done to bring you the best Organic meat possible. Belcampo raise their animals on a farm at the base of Mt. Shasta in California. Their farm, and process, are crafted with compassion and sustainability at [&#8230;]\nThe post Website Launch Announcement &#8211; Belcampo appeared first on Planeteria Media.",
# ]
message_ids = list(dbOfArticlesDict.keys())
    # 542,
    # 235,
    # 989,
    # 421,
    # 498,
    # 359,
    # 861,
    # 799,
    # 250,
#]

keywords = [
    "coronavirus",
    "health",
    "consumer",
]
print(messages)
articleToKeyword = {}
run_and_plot(message_ids, messages, keywords)