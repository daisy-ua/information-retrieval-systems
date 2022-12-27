import re
import string
import sys


class Database:
    def __init__(self):
        self.db = dict()

    def __repr__(self):
        return str(self.__dict__)

    def get(self, id):
        return self.db.get(id, None)

    def add(self, document):
        return self.db.update({document['id']: document})

    def remove(self, document):
        return self.db.pop(document['id'], None)


class Appearance:
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __repr__(self):
        return str(self.__dict__)


class InvertedIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

    def index_document(self, document):
        terms = re.split(' |\n', document['text'])
        terms = list(map(lambda term: term.strip(
            string.punctuation).lower(), terms))

        appearances_dict = dict()

        for term in terms:
            if term != "":
                term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
                appearances_dict[term] = Appearance(
                    document['id'], term_frequency + 1)

        update_dict = {key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items()}
        self.index.update(update_dict)

        self.db.add(document)
        return document

    def lookup_query(self, query):
        return {term: self.index[term] for term in query.split(' ') if term in self.index}
