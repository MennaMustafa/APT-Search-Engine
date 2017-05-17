from helpers.DB_Manager import DB_Manager
from helpers.Stemmer import Stemmer
from help_functions import generalize_data
import en
import mmap

class PhraseProcessor:
    __myDb = DB_Manager()
    list_of_common_documents = []
    documents_union = [] #List of lists, each list corresponds to not-stemmed word of query
    query_words = []
    word_poistions = {}
    final_documents = []
    query = ""

    def GetAllDocs(self,Query):
        self.query = Query.lower()
        words = generalize_data(self.query)
        self.query_words = words.split()
        for word in self.query_words:
            l = self.__myDb.select_docs_contain_word("words",word,False)
            self.documents_union.append(l)
        return self.documents_union

    def GetCommonDocs(self): #Intersection
        All_docs = self.documents_union
        self.list_of_common_documents= list(reduce(set.intersection, [set(item) for item in All_docs]))
        return self.list_of_common_documents

    def GetFinalDocs(self):
        LOD = self.list_of_common_documents
        for file in LOD:
            s = open(file, 'r').read().lower()
            if s.find(self.query.lower()) != -1:
              self.final_documents.append(file)
        return self.final_documents


# P = PhraseProcessor()
# P.GetAllDocs("Portal:Geography - Wikipedia")
# l = P.GetCommonDocs()
# P.GetFinalDocs()
# print P.final_documents

# for file in l:
#     f = open(file)
#     s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
#     if s.find("thank you") != -1:
#       exact_list.append(file)

