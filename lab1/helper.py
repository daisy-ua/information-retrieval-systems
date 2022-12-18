import os


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


def highlight_term(id, term, text):
    replaced_text = text.replace(
        term, "\033[1;32;40m {term} \033[0;0m".format(term=term))
    return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)


def index_files(index):
    files = os.listdir('data/')

    for idx, file in enumerate(files):
        with open('data/' + file) as f:
            document = {
                'id': idx,
                'text': f.read()
            }

        index.index_document(document)
