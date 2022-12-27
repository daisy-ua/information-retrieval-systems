import os
import re
import sys
from common_elements import common_elements
from invered_index import Database, InvertedIndex


def create_index(files, index, file_titles):
    for idx, file in enumerate(files):
        with open(file) as f:
            read = f.read()

        file_titles[file] = read.partition('\n')[0]

        document = {
            'id': file,
            'text': read
        }

        index.index_document(document)


def search(index, query):
    terms = re.split(' |\n', query)

    if not all(term in index.index.keys() for term in terms):
        return []

    first = terms.pop(0)

    result = index.index[first]
    result = mapSearch(result)

    for term in terms:
        result = common_elements(result, mapSearch(index.index[term]))
    return result


def mapSearch(result):
    return list(map(lambda x: x.doc_id, result))


def input_search(index, file_titles):
    while True:
        query = input('Query (empty query to stop): ')
        query = query.lower()

        if query == '':
            break

        results = search(index, query)
        display_search_result(query, results, file_titles)


def display_search_result(query, results, file_titles):
    print(f'Results for query "{query}":')
    if results:
        for i in range(len(results)):
            title = file_titles[results[i]]
            print(f'{str(i + 1)}. Title: {title} File: {results[i]}')
    else:
        print("No results match that query.")


def textfiles_in_dir(directory):
    filenames = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filenames.append(os.path.join(directory, filename))

    return filenames


def main():
    db = Database()
    index = InvertedIndex(db)

    directory_name = sys.argv[1]

    if os.path.exists(directory_name):
        files = textfiles_in_dir(directory_name)
        file_titles = {}

        create_index(files, index, file_titles)

        if len(sys.argv) == 3 and sys.argv[2] == '-s':
            input_search(index, file_titles)
        elif len(sys.argv) > 2:
            query = sys.argv[2].strip('"')
            results = search(index, query)
            display_search_result(query, results, file_titles)

    else:
        print(f'Cannot find directory "{directory_name}"')


if __name__ == '__main__':
    main()
