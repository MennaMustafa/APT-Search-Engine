from helpers.DB_Manager import DB_Manager
from helpers.Stemmer import Stemmer
from help_functions import generalize_data

class QueryProcessor:
    __myDb = DB_Manager()
    __myStemmer = Stemmer()
    stemmed_query = []
    list_of_documents = []
    documents_union = []

    def StemQuery(self,Query):
        stemmed = generalize_data(Query.lower())
        words = stemmed.split()
        for word in words:
            self.stemmed_query.append(self.__myStemmer.stem_word(word))
        return stemmed

    def GetDocsUnion(self):
        for word in self.stemmed_query:
            self.documents_union.append(self.__myDb.select_docs_contain_word("words",word,True))
        return self.documents_union

    def GetDocsIntersect(self):
        All_docs = self.documents_union
        self.list_of_documents = list(reduce(set.intersection, [set(item) for item in All_docs]))
        return self.list_of_documents

# #test code , sha8aaaaaaaaaaaaaaaaaaaaal :v :v
# Q = QueryProcessor()
# Q.StemQuery("he's playing football")
# print(sum(map(len, Q.GetDocsUnion())))
# l= Q.GetDocsIntersect()
# print l
