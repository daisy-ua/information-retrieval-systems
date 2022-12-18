import re
import sys
from helper import highlight_term, index_files

from inverted_index import Database


class ForwardIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

    def index_document(self, document):
        clean_text = re.sub(r'[^\w\s]', '', document['text'])
        terms = re.split(' |\n', clean_text)
        keywords_list = list()

        for term in terms:
            if term not in keywords_list:
                keywords_list.append(term)

        doc_id = document['id']

        if doc_id not in self.index:
            update_dict = {doc_id: keywords_list}
            self.index.update(update_dict)

        self.db.add(document)
        return document

    def lookup_query(self, query):
        results = dict()
        terms = query.split(' ')

        for (file_id, keywords) in self.index.items():
            intersections = intersection(keywords, terms)
            if (len(intersections) > 0):
                results.update({file_id: intersections})

        return results


def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def print_results(result, db):
    for doc_id in result.keys():
        for keyword in result[doc_id]:
            document = db.get(doc_id)
            print(highlight_term(doc_id, keyword, document['text']))
        print("-----------------------------")


def main():
    db = Database()
    index = ForwardIndex(db)

    index_files(index)

    query = ' '.join(sys.argv[1:])
    result = index.lookup_query(query)

    print_results(result, db)


if __name__ == '__main__':
    main()
