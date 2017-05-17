from pymongo import *

class DB_Manager:
    client = MongoClient()
    db = client.Indexer
    Words_in_url = []
    Urls_contain_word = []
    word_positions_in_doc = []
    Error = "Ops! Error happened w da barra 3nny, please don't try again msh na2sa :v"

    def insert_word(self, collection_name, s, w, r, url, positions):
        """A function to insert a new record in collection, parameters are:
        w: word, r: rank, url: Document identifier, positions: array of word's positions in certain document"""
        if self.db.get_collection(collection_name).find({"word": w}, {"DocID": url}).count() > 0:
            return "already exist"
        else:
            returned_ID = self.db.get_collection(collection_name).insert({
                "Stemmed_word": s,
                "Original_word": w,
                "rank": r,
                "DocID": url,
                "Positions": positions,
                "WriteResults": 1
            })
            err = self.db.get_collection(collection_name).find({"_id": returned_ID}, {"WriteResults": 1})
            for c in err:
                if (c.get("WriteResults")) != 1:
                    print(self.Error)
            return "Insert Success"

    def remove_word_from_all(self,collection_name, w, flag):
        """A function to remove word record in all documents
        parameters, w: word to be removed"""
        result = ""
        # if flag=true -> remove all stemmed
        # if flag==false -> remove only original
        if (flag):
            result = self.db.get_collection(collection_name).remove({"Stemmed_word": w})
        else:
            result = self.db.get_collection(collection_name).remove({"Original_word": w})
        if result.get("ok") != 1:
            print(self.Error)

    def remove_word_from_document(self, collection_name, w, url, flag):
        """A function to remove word record in a certain one document
        parameters, w: word to be removed, url: document that we want to remove word from"""
        result = ""
        if (flag):
            result = self.db.get_collection(collection_name).remove({"Stemmed_word": w}, {"DocID": url})
        else:
            result = self.db.get_collection(collection_name).remove({"Original_word": w}, {"DocID": url})

        if result.get("ok") != 1:
            print(self.Error)

    def select_words_in_doc(self, collection_name, doc):
        """A function to select all words that exists in certain document and return them in array Words_in_url
        parameters, doc: document that we want its words"""
        result = self.db.get_collection(collection_name).find({"DocID": doc}, {"word": 1})
        for c in result:
            self.Words_in_url.append(c.get("word"))
        return self.Words_in_url

    def select_docs_contain_word(self, collection_name, word, searchStemmedOrNot):
        """A function to select all documents that contain certain word and return them in array Urls_contain_word
        parameters, w: word that we search where is it"""
        result = ""
        self.Urls_contain_word = []
        if (searchStemmedOrNot):
            result = self.db.get_collection(collection_name).find({"Stemmed_word": word}, {"DocID": 1})
        else:
            result = self.db.get_collection(collection_name).find({"Original_word": word}, {"DocID": 1})
        for c in result:
            self.Urls_contain_word.append(c.get("DocID"))
        return self.Urls_contain_word

    def select_word_positions(self,collection_name,word,doc_id):
        self.word_positions_in_doc = []
        result = self.db.get_collection(collection_name).find({"DocID":doc_id,"Original_word": word})
        for record in result:
            self.word_positions_in_doc.append(record.get("Positions"))
        return self.word_positions_in_doc

    def clear_db(self, collection_name):
        """A function to remove all records from the collection"""
        self.db.get_collection(collection_name).remove({})

    def check_page_existence(self, collection_name, doc):
        return self.db.get_collection(collection_name).count({"DocID": doc}) > 0

    def create_collection(self, collection_name):
        """A function to create new collection in Indexer DB"""
        self.db.create_collection(collection_name)

    def insert_all(self, collection_name, myList):
        """A function to insert many new record in collection, parameters are:
                w: word, r: rank, url: Document identifier, positions: array of word's positions in certain document"""
        self.lock.acquire()
        self.db.get_collection(collection_name).insert_many(myList)
        self.lock.release()

    def get_page_rank(self, collection_name, page_name):
        result = self.db.get_collection(collection_name).find_one({"name": page_name})
        return result

    def get_word_rank_in_doc(self, collection_name, page_name, word):
        my_result = self.db.get_collection(collection_name).find_one({"Stemmed_word": str(word), "DocID": str(page_name)})
        if my_result is None:
            return 0
        else:
            return my_result["rank"]

#res = (DB_Manager()).get_word_rank_in_doc("words", "temp/97.html", "he")
#print res
#(DB_Manager()).clear_db();
