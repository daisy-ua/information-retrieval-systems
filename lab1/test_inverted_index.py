import unittest

from inverted_index import Database, InvertedIndex

document1 = {
    'id': 0,
    'text': 'This is document 1'
}

document2 = {
    'id': 1,
    'text': 'This is document 2'
}


class InvertedIndexTest(unittest.TestCase):

    def test_index_document(self):
        db = Database()
        index = InvertedIndex(db)
        index.index_document(document1)
        index.index_document(document2)

        result = index.__repr__()
        expected = str({'This': [{'docId': 0, 'frequency': 1}, {'docId': 1, 'frequency': 1}], 'is': [{'docId': 0, 'frequency': 1}, {'docId': 1, 'frequency': 1}], 'document': [
                       {'docId': 0, 'frequency': 1}, {'docId': 1, 'frequency': 1}], '1': [{'docId': 0, 'frequency': 1}], '2': [{'docId': 1, 'frequency': 1}]})
        self.assertEqual(result, expected)

    def test_search_term_exist(self):
        db = Database()
        index = InvertedIndex(db)
        index.index_document(document1)
        index.index_document(document2)

        query = 'This'
        result = str(index.lookup_query(query))
        expected = str(
            {'This': [{'docId': 0, 'frequency': 1}, {'docId': 1, 'frequency': 1}]})
        self.assertEqual(result, expected)

    def test_search_term_not_exist(self):
        db = Database()
        index = InvertedIndex(db)
        index.index_document(document1)
        index.index_document(document2)

        query = '3'
        result = str(index.lookup_query(query))
        expected = str({})
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
