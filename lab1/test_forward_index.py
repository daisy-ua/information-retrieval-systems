import unittest
from forward_index import ForwardIndex

from helper import Database


document1 = {
    'id': 0,
    'text': 'This is document 1'
}

document2 = {
    'id': 1,
    'text': 'This is document 2'
}


class ForwardIndexTest(unittest.TestCase):

    def test_index_document(self):
        db = Database()
        index = ForwardIndex(db)
        index.index_document(document1)
        index.index_document(document2)

        result = index.__repr__()
        expected = str({0: ['This', 'is', 'document', '1'],
                       1: ['This', 'is', 'document', '2']})
        self.assertEqual(result, expected)

    def test_search_term_exist(self):
        db = Database()
        index = ForwardIndex(db)
        index.index_document(document1)
        index.index_document(document2)

        query = 'This 2'
        result = str(index.lookup_query(query))
        expected = str({0: ['This'], 1: ['This', '2']})
        self.assertEqual(result, expected)

    def test_search_term_not_exist(self):
        db = Database()
        index = ForwardIndex(db)
        index.index_document(document1)
        index.index_document(document2)

        query = '3'
        result = str(index.lookup_query(query))
        expected = str({})
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
