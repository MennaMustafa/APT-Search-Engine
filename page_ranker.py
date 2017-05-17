from collections import OrderedDict

from helpers.DB_Manager import DB_Manager
from helpers.Stemmer import Stemmer

class my_page_ranker:
    __db_manager = DB_Manager()
    __intersection_pages = dict()
    __ordered_pages = dict()
    __links = dict()
    __page_titles = dict()
    __visited = list()
    __myStemmer = Stemmer()
    __words_collection_name = "words"
    __info_collection_name = "pages_info"

    def update_page_rank(self, list_of_files, query, intersectionOrNot):
        for page_name in list_of_files:
            if page_name not in self.__visited:
                self.__visited.append(page_name)
                if intersectionOrNot:
                    self.__intersection_pages[page_name] = 0
                else:
                    self.__ordered_pages[page_name] = 0
                page_info = self.__db_manager.get_page_rank(self.__info_collection_name, page_name)
                for word in query.split():
                    word_rank = self.__db_manager.get_word_rank_in_doc(self.__words_collection_name, page_name, self.__myStemmer.stem_word(word))
                    if intersectionOrNot:
                        self.__intersection_pages[page_name] += page_info["page_rank"] * word_rank
                    else:
                        self.__ordered_pages[page_name] += page_info["page_rank"] * word_rank
                    self.__links[page_name] = page_info["link"]
                    self.__page_titles[page_name] = page_info["title"]

    def order_pages(self, list_of_union, list_of_intersection, query, phrase_search):
        print "searching for your words .... "
        self.__intersection_pages = dict()
        self.__ordered_pages = dict()
        self.__links = dict()
        self.__page_titles = dict()
        self.__visited = list()
        self.update_page_rank(list_of_intersection, query, True)
        if not phrase_search:
            l = list()
            for sublist in list_of_union:
                l.extend([item for item in sublist if item not in list_of_intersection and item not in l])
            self.update_page_rank(l, query, False)
        res = list(sorted(self.__intersection_pages, key=self.__intersection_pages.__getitem__, reverse=True)) + list(sorted(self.__ordered_pages, key=self.__ordered_pages.__getitem__, reverse=True))
        ordered_pages = OrderedDict()
        for page in res:
            ordered_pages[self.__page_titles[page]] = self.__links[page]
            if page in self.__intersection_pages.keys():
                print self.__page_titles[page] + " --> " + self.__links[page] + " --> rank = " + str(self.__intersection_pages[page]) + "(all words found here)"
            else:
                print self.__page_titles[page] + " --> " + self.__links[page] + " --> rank = " + str(self.__ordered_pages[page]) + "(some words found here)"
        return ordered_pages.copy()
