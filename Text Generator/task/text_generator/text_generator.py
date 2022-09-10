from nltk import WhitespaceTokenizer, trigrams
from random import choices, choice
import re


class TextGenerator:
    PUNCTUATION = {".", "!", "?"}

    def __init__(self):
        self.markov_chain = dict()
        self.corpus = str()
        self.tokens = list()

    def get_corpus(self, path: str):
        f = open(f'{path}', "r", encoding="utf-8")
        self.corpus = f.read()
        f.close()
        return self.corpus

    def get_token(self):
        wst = WhitespaceTokenizer()
        self.tokens = wst.tokenize(self.corpus)
        return self.tokens

    def get_trigrams(self):
        trigram = list(trigrams(self.tokens))
        return trigram

    def get_chain(self, trigram: list):
        for word in trigram:
            double_head = " ".join([word[0], word[1]])
            self.markov_chain.setdefault(double_head, {})
            self.markov_chain[double_head].setdefault(word[2], 0)
            self.markov_chain[double_head][word[2]] += 1
        return self.markov_chain

    def get_first_part(self):
        while True:
            part = choice(list(self.markov_chain.keys()))
            two_word = part.split()
            cap_letter = bool(re.match(r'[A-Z]', part[0]))
            if cap_letter and two_word[0][-1] not in self.PUNCTUATION and two_word[1][-1] not in self.PUNCTUATION:
                return part
            else:
                pass

    def generate_sentence(self, count_sentence: int):
        while count_sentence != 0:
            word = self.get_first_part()
            text_split = word.split()
            while True:
                current_tail = " ".join([text_split[-2], text_split[-1]])
                len_sentence = len(text_split)
                tails = []
                weight = []
                for tail in self.markov_chain[current_tail]:
                    tails.append(tail)
                    weight.append(self.markov_chain[current_tail][tail])
                word = choices(tails, weight, k=1)[0]
                text_split.append(word)
                if word[-1] in self.PUNCTUATION and len_sentence >= 4:
                    break
            print(' '.join(text_split))
            count_sentence -= 1

    def get_stat_head(self, head_token: str):
        print(f'Head: {head_token}')
        for tail in self.markov_chain[head_token]:
            print(f'Tail: {tail}  Count: {self.markov_chain[head_token][tail]}')


generator = TextGenerator()
path_file = str(input(''))
corpus = generator.get_corpus(path_file)
generator.get_token()
trigrams = generator.get_trigrams()
generator.get_chain(trigrams)
generator.generate_sentence(10)

