from helpers.Stemmer import Stemmer
from helpers.htmlParser import MyHTMLParser
from helpers.DB_Manager import DB_Manager
import sys
import os
import time


class MyIndexer:
    __myDbManager = DB_Manager()
    __num_of_indexers = 5
    __num_of_pages_per_indexer = 1
    __all_files_names = []
    __files_path = "files/"
    __words_collection_name = "words"
    __info_collection_name = "pages_info"

    def __init__(self, files_path="", words_collection_name="", info_collection_name = ""):
        self.__stemmer = Stemmer()
        self.__myParser = MyHTMLParser()
        self.__myDbManager = DB_Manager()
        self.__pages_info = dict()
        if len(files_path) > 0:
            self.__files_path = files_path
        if len(words_collection_name) > 0:
            self.__words_collection_name = words_collection_name
        if len(info_collection_name) > 0:
            self.__info_collection_name = info_collection_name
        self.__all_files_names = os.listdir(self.__files_path)

    def index_these_files(self, files_names):
        for page_name in files_names:
            page_name = str(self.__files_path + page_name)
            if not page_name.endswith(".html"):
                print page_name + " is not a html page"
            # elif self.__myDbManager.check_page_existence(self.__words_collection_name, page_name):
            #     print page_name + " was indexed before"
            else:
                self.__pages_info[page_name] = self.__myParser.index_this_page(page_name).copy()
        self.add_to_the_db(self.__pages_info)
        self.__pages_info = dict()

    def index_files(self):
        self.index_these_files(self.__all_files_names)

    def add_to_the_db(self, pages_info):
        words_list = []
        info_dictionary = dict()
        out_links = dict()
        page_title = ""
        for page_name, page_info in pages_info.items():
            if page_info["title"]:
                page_title = page_info["title"]
            out_links[page_info["link"]] = page_info["out_links"]
            info_dictionary[page_name] = [page_title, page_info["link"]]
            words_dictionary = page_info["words_dictionary"]
            words_list.extend(self.create_words_input_list(page_name, words_dictionary))
        info_list = self.create_information_input_list(info_dictionary.copy(), self.create_page_rank(out_links).copy())
        self.__myDbManager.insert_all(self.__words_collection_name, words_list)
        self.__myDbManager.insert_all(self.__info_collection_name, info_list)

    def create_words_input_list(self, page_name, orderedDictionary):
        input_list = []
        for word, indexesAndRank in orderedDictionary.items():
            # rank is indexesAndRank[1] and indexed is [0]
            dic = {"Stemmed_word": self.__stemmer.stem_word(word), "Original_word": word, "rank": indexesAndRank[1], "DocID": page_name, "Positions": indexesAndRank[0], "WriteResults": 1}
            input_list.append(dic.copy())
        return input_list

    def create_information_input_list(self, info_dic, page_rank_dic):
        input_list = []
        for page_name, page_info in info_dic.items():
            # title is page_info[0], link is [1]
            dic = {"name": page_name, "title": page_info[0], "link": page_info[1], "page_rank": page_rank_dic[page_info[1]]}
            input_list.append(dic.copy())
        return input_list

    def create_page_rank(self, out_links_dic):
        in_links = dict()
        for main_page in out_links_dic.keys():
            in_links[main_page] = [page for page in out_links_dic.keys() if main_page in out_links_dic[page] and page != main_page]
        old_PR = {page_name: 1 for page_name in out_links_dic.keys()}
        new_PR = {page_name: 0 for page_name in out_links_dic.keys()}
        dampping_factor = 0.85
        difference = sum([abs(old_PR[page_name] - new_PR[page_name]) for page_name in out_links_dic.keys()])
        while difference > 0.001:
            old_PR = new_PR.copy()
            for page_name in out_links_dic.keys():
                new_PR[page_name] = (1 - dampping_factor) + dampping_factor * sum(
                    [old_PR[page] / len(out_links_dic[page]) for page in in_links[page_name]])
            difference = sum([abs(old_PR[page_name] - new_PR[page_name]) for page_name in out_links_dic.keys()])
        return new_PR

reload(sys)
sys.setdefaultencoding("utf-8")
path = "temp/"
words_collection_name = "words"
files = os.listdir(path)
startTime = time.clock()
print "The indexer started at " + str(startTime)
indexer = MyIndexer(path, words_collection_name)
indexer.index_files()
endTime = time.clock()
print "It took the indexer " + str(endTime - startTime) + " to finish"
