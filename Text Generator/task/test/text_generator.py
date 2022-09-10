from nltk import WhitespaceTokenizer
from nltk import bigrams as _bigrams
from collections import Counter
from collections import defaultdict


class Markov_chain():

    def __init__(self):
        self.markov_chain = defaultdict(list)

    def get_corpus(self, name_file: str):
        f = open(f'{name_file}', "r", encoding="utf-8")
        corpus_text = f.read()
        f.close()
        return corpus_text

    def get_counter(self, corpus):
        wst = WhitespaceTokenizer()
        tokens = wst.tokenize(corpus)
        bow_counter = Counter(tokens)
        return bow_counter

    def get_bigram(self, corpus: str):
        wst = WhitespaceTokenizer()
        tokens = wst.tokenize(corpus)
        bigrams = list(_bigrams(tokens))
        return bigrams

    def get_chain(self, bigrams: list):
        for bigram in bigrams:
            self.markov_chain[bigram[0]].append(bigram[1])
        return self.markov_chain

    def get_stat(self, head_token: str):
        print(f'Head: {head_token}')
        counter = Counter(self.markov_chain[head_token])
        set_chain = set(self.markov_chain[head_token])
        order = defaultdict(int)
        for word in set_chain:
            order[word] = counter[word]
        order = dict(sorted(order.items(), reverse=True, key=lambda item: item[1]))
        for tail, counter in order.items():
            print(f'Tail: {tail}  Count: {counter}')


generator = Markov_chain()
path_file = str(input('Enter path file: '))
corpus = generator.get_corpus(path_file)
bigram = generator.get_bigram(corpus)
generator.get_chain(bigram)
while True:
    try:
        token = input('Enter word: ')
        if token == 'exit':
            break
        generator.get_stat(token)
    except KeyError:
        print('Key Error. The requested word is not in the model. Please input another word.')

