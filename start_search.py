from QueryProcessor import QueryProcessor
from page_ranker import my_page_ranker
from PhraseProcessor import PhraseProcessor

class search_class:
    def __init__(self):
        self.__query_processor = QueryProcessor()
        self.__page_ranker = my_page_ranker()
        self.__phrase_processor = PhraseProcessor()

    def start_search(self, query):
        query = str(query)
        if query[0] == '"' and query[len(query) - 1] == '"':
            query = query[1:len(query)-1]
            self.__phrase_processor.GetAllDocs(query)
            self.__phrase_processor.GetCommonDocs()
            self.__phrase_processor.GetFinalDocs()
            final_docs = self.__phrase_processor.final_documents
            return self.__page_ranker.order_pages([], final_docs, query, True)
        else:
            stemmed = self.__query_processor.StemQuery(query)
            union = self.__query_processor.GetDocsUnion()
            intersection = self.__query_processor.GetDocsIntersect()
            return self.__page_ranker.order_pages(union, intersection, stemmed, False)

# query = str(raw_input("search for: "))
# search_class().start_search(query)
