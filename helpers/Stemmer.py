from nltk import SnowballStemmer
import en


# old list: Original word - rank - DocumentID - Positions
# new list: Stemmed word - Original word - rank - DocumentID - Positions


class Stemmer:
    be = ["am", "is", "are", "was", "were", "has", "hasn't", "isn't", "wasn't", "weren't"]

    def stem_word(self, word):
        try:
            return en.verb.present(word)
        except:
            stemmer = SnowballStemmer("english")
            return stemmer.stem(word)
