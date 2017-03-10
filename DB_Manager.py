from pymongo import *
class DB_Manager:
    client = MongoClient()
    db = client.Indexer
    Words_in_url = []
    Urls_contain_word = []
    Error = "Ops! Error happened w da barra 3nny, please don't try again msh na2sa :v"

    def insert_word(self,w,r,url):
        r = self.db.words.insert({
            "word": w,
            "rank": r,
            "DocID": url
        })
        if r.WriteResult.hasWriteError():
            print(self.Error)
        else:
            print("heeeeeh inserted!")

    def remove_word(self,d):
        result = self.db.words.remove({"DocID":d})
        if result.WriteResult.hasWriteError():
            print(self.Error)

    def select_word(self,doc):
        result = self.db.words.find({"DocID":doc},{"word":1})
        for c in result:
            self.Words_in_url.append(c.get("word"))
        return self.Words_in_url

    def select_doc(self,w):
        result = self.db.words.find({"word":w},{"DocID":1})
        for c in result:
            self.Urls_contain_word.append(c.get("DocID"))
        return self.Urls_contain_word