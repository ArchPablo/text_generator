from nltk import WhitespaceTokenizer
from nltk import bigrams as _bigrams
from nltk import trigrams
from collections import Counter
from random import choices
from random import choice
import re


class Markov_chain:
    PUNCTUATION = {".", "!", "?"}

    def __init__(self):
        self.markov_chain = dict()
        self.tokens = list()

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


    def get_trigrams(self, corpus: str):
        wst = WhitespaceTokenizer()
        self.tokens = wst.tokenize(corpus)
        trig = list(trigrams(self.tokens))
        return trig

    def get_chain_trig(self, trig: list):
        for word in trig:
            double_head = word[0] + ' ' + word[1]
            self.markov_chain.setdefault(double_head, {})
            self.markov_chain[double_head].setdefault(word[2], 0)
            self.markov_chain[double_head][word[2]] += 1
        return self.markov_chain

    def get_stat(self, head_token: str):
        print(f'Head: {head_token}')
        for tail in self.markov_chain[head_token]:
            print(f'Tail: {tail}  Count: {self.markov_chain[head_token][tail]}')

    def get_st_text(self):
        for _ in range(10):
            text = []
            prev_word = choice(list(self.markov_chain.keys()))
            text.append(prev_word)
            for i in range(9):
                list_word = list(self.markov_chain[prev_word])
                weights_ = tuple(self.markov_chain[prev_word].values())
                word = choices(list_word, weights=weights_)
                text.append(word[0])
                prev_word = word[0]
            print(' '.join(text))

    def get_first_word(self):
        while True:
            word = choice(self.tokens)
            cap_letter = bool(re.match(r'[A-Z]', word[0]))
            if cap_letter and word[-1] not in self.PUNCTUATION:
                return word
            else:
                pass

    def get_text(self):
        sentence = 10
        while sentence != 0:
            word = self.get_first_word()
            text = word
            while True:
                len_sentence = len(text.split(' '))
                tails = []
                weight = []
                for tail in self.markov_chain[word]:
                    tails.append(tail)
                    weight.append(self.markov_chain[word][tail])
                word = choices(tails, weight, k=1)[0]
                text += f' {word}'
                if word[-1] in self.PUNCTUATION and len_sentence >= 4:
                    break
            print(text)
            sentence -= 1


generator = Markov_chain()
path_file = str(input(''))
corpus = generator.get_corpus(path_file)
bigram = generator.get_trigrams(corpus)
generator.get_chain_trig(bigram)
generator.get_text()
