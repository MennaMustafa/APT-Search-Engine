# from . import en
#
#
# def EditQuery(Query):
#     cList = {
#         "ain't": "am not",
#         "aren't": "are not",
#         "can't": "cannot",
#         "can't've": "cannot have",
#         "'cause": "because",
#         "could've": "could have",
#         "couldn't": "could not",
#         "couldn't've": "could not have",
#         "didn't": "did not",
#         "doesn't": "does not",
#         "don't": "do not",
#         "hadn't": "had not",
#         "hadn't've": "had not have",
#         "hasn't": "has not",
#         "haven't": "have not",
#         "he'd": ["he would", "he had"],
#         "he'd've": "he would have",
#         "he'll": "he will",
#         "he'll've": "he will have",
#         "he's": ["he is", "he has"],
#         "how'd": ["how did", "how would"],
#         "how'd'y": "how do you",
#         "how'll": "how will",
#         "how's": ["how is", "how has", "how does"],
#         "I'd": ["I would", "I had"],
#         "I'd've": "I would have",
#         "I'll": "I will",
#         "I'll've": "I will have",
#         "I'm": "I am",
#         "I've": "I have",
#         "isn't": "is not",
#         "it'd": "it had",
#         "it'd've": "it would have",
#         "it'll": "it will",
#         "it'll've": "it will have",
#         "it's": ["it is", "it has"],
#         "let's": "let us",
#         "ma'am": "madam",
#         "mayn't": "may not",
#         "might've": "might have",
#         "mightn't": "might not",
#         "mightn't've": "might not have",
#         "must've": "must have",
#         "mustn't": "must not",
#         "mustn't've": "must not have",
#         "needn't": "need not",
#         "needn't've": "need not have",
#         "o'clock": "of the clock",
#         "oughtn't": "ought not",
#         "oughtn't've": "ought not have",
#         "shan't": "shall not",
#         "sha'n't": "shall not",
#         "shan't've": "shall not have",
#         "she'd": ["she would", "she had"],
#         "she'd've": "she would have",
#         "she'll": "she will",
#         "she'll've": "she will have",
#         "she's": ["she is", "she has"],
#         "should've": "should have",
#         "shouldn't": "should not",
#         "shouldn't've": "should not have",
#         "so've": "so have",
#         "so's": "so is",
#         "that'd": "that would",
#         "that'd've": "that would have",
#         "that's": "that is",
#         "there'd": "there had",
#         "there'd've": "there would have",
#         "there's": "there is",
#         "they'd": "they would",
#         "they'd've": "they would have",
#         "they'll": "they will",
#         "they'll've": "they will have",
#         "they're": "they are",
#         "they've": "they have",
#         "to've": "to have",
#         "wasn't": "was not",
#         "we'd": "we had",
#         "we'd've": "we would have",
#         "we'll": "we will",
#         "we'll've": "we will have",
#         "we're": "we are",
#         "we've": "we have",
#         "weren't": "were not",
#         "what'll": "what will",
#         "what'll've": "what will have",
#         "what're": "what are",
#         "what's": "what is",
#         "what've": "what have",
#         "when's": "when is",
#         "when've": "when have",
#         "where'd": "where did",
#         "where's": "where is",
#         "where've": "where have",
#         "who'll": "who will",
#         "who'll've": "who will have",
#         "who's": "who is",
#         "who've": "who have",
#         "why's": "why is",
#         "why've": "why have",
#         "will've": "will have",
#         "won't": "will not",
#         "won't've": "will not have",
#         "would've": "would have",
#         "wouldn't": "would not",
#         "wouldn't've": "would not have",
#         "y'all": "you all",
#         "y'alls": "you alls",
#         "y'all'd": "you all would",
#         "y'all'd've": "you all would have",
#         "y'all're": "you all are",
#         "y'all've": "you all have",
#         "you'd": ["you would", "you had"],
#         "you'd've": "you would have",
#         "you'll": "you will",
#         "you'll've": "you you will have",
#         "you're": "you are",
#         "you've": "you have"
#     }
#
#     xwords = Query.split()
#     c = 0
#     for word in xwords:
#         if word in cList:
#             try:
#                 print "here"
#                 tense = en.verb.tense(xwords[c + 1])
#                 if tense == "past" or tense == "past participle":
#                     if isinstance(cList[word], list):
#                         xwords[c] = cList[word][1]
#                     else:
#                         xwords[c] = cList[word]
#                 elif tense == "present participle" or tense == "1st singular present" or tense == "infinitive":
#                     print "right here"
#                     if isinstance(cList[word], list):
#                         xwords[c] = cList[word][0]
#                     else:
#                         xwords[c] = cList[word]
#             except:
#                 xwords[c] = cList[word][0]
#         c += 1
#     final_query = ' '.join(xwords)
#     return final_query

# d = [[1,5,7],[1,4,5],[7,1,3,4,5]]
# print list(reduce(set.intersection, [set(item) for item in d ]))
# print(sum(map(len, d)))
#
# import re
# import os
# import shutil
#
# drc = 'files'
# pattern = re.compile('thank you')
# oldstr = 'thank you'
#
# for dirpath, dirname, filename in os.walk(drc):  # Getting a list of the full paths of files
#     for fname in filename:
#         path = os.path.join(dirpath, fname)  # Joining dirpath and filenames
#         strg = open(path).read()  # Opening the files for reading only
#         if re.search(pattern, strg):  # If we find the pattern ....
#             print path

from pymongo import MongoClient
import os
import html2text
import sys
reload(sys)
sys.setdefaultencoding('utf8')

client = MongoClient()
db = client.Indexer  # use a database called "test_database"
collection = db.files  # and inside that DB, a collection called "files"
i = 1
os.chdir("files")
while i<1689:
    file_name = str(i)+'.html'
    f = open(file_name)  # open a file
    text = f.read()    # read the entire contents, should be UTF-8 text
    # build a document to be inserted
    html2text.html2text(text)
    text_file_doc = {"file_name": file_name, "contents" : text }
    # insert the contents into the "file" collection
    collection.insert(text_file_doc)
    print file_name+" inserted"
    i +=1














