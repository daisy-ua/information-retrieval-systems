import re
import sys

from helper import Database, highlight_term, index_files


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
        clean_text = re.sub(r'[^\w\s]', '', document['text'])
        terms = re.split(' |\n', clean_text)
        appearances_dict = dict()

        for term in terms:
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


def print_results(result, db):
    for term in result.keys():
        for appearance in result[term]:
            document = db.get(appearance.doc_id)
            print(highlight_term(appearance.doc_id, term, document['text']))
        print("-----------------------------")


def main():
    db = Database()
    index = InvertedIndex(db)

    index_files(index)

    query = ' '.join(sys.argv[1:])
    result = index.lookup_query(query)

    print_results(result, db)


if __name__ == '__main__':
    main()
