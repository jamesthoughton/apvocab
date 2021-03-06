import requests
import pickle
import math


def main(): pass


def api_get(url): return requests.get(url + 'client_id=nMPK85cZxV&whitespace=0').json()


def get_terms(set_id): return api_get('https://api.quizlet.com/2.0/sets/' + str(set_id) + '/terms?')


def search_sets(search_term):
    return api_get('https://api.quizlet.com/2.0/search/sets?q=' + search_term.replace(' ', '-') + '&per_page=50&')


def search_page(search_term, page):
    search_term = search_term.replace(' ', '-')
    return api_get('https://api.quizlet.com/2.0/search/sets?q=' + search_term + '&per_page=50&page=' + str(page) + '&')


def add_terms(terms):
    defs = {}
    for i in range(len(terms)):
        if len(terms[i]['definition'].strip()) > 1:
            defs[terms[i]['term']] = terms[i]['definition']
    return defs


def fill_vocab(search_terms, max_terms):
    definitions = {}
    for term in search_terms:
        num_pages = search_sets(term)['total_pages'] - 1
        for page in range(1, num_pages):
            if page % 2 == 0:
                print str(int(math.floor(len(definitions) * 100 / float(max_terms)))) + '% Complete'
            page_sets = search_page(term, page)
            for quiz_set in page_sets['sets']:
                try:
                    definitions.update(add_terms(get_terms(quiz_set['id'])))
                except Exception as e:
                    print e
                if len(definitions) >= max_terms:
                    return definitions
    return definitions

if __name__ == "__main__":
    main()
    max_num_terms = 25000
    terms = ['AP Human Geography']
    vocab = fill_vocab(terms, max_num_terms)
    print len(vocab)

    with open('../static/defs/humangeo_defs.pickle', 'wb') as handle:
        pickle.dump(vocab, handle)


class Filler:
    def __init__(self):
        pass

    def get_vocab(self, search_terms, max_terms):
        return fill_vocab(search_terms, max_terms)
