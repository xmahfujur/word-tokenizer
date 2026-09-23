from collections import Counter
import re


class WordTokenizer:
    def __init__(self):

        self.token_to_id = {}
        self.id_to_token = {}


        self.token_to_id['<UNK>'] = 0
        self.id_to_token[0] = '<UNK>'

        self.tokens = []

        with open('data.txt', 'r', encoding='utf-8') as f:

            text = f.read()

        self.tokens = re.findall(r"\w+|[^\w\s]|\s+", text)

    def train(self, tokens):

        i = 1

        while i < len(tokens):
            for token in tokens:
                self.token_to_id[token] = i
                self.id_to_token[i] = token
                i+=1

    def encode(self, input):
        tokens = re.findall(r"\w+|[^\w\s]|\s+", input)

        ids = []

        for token in tokens:
            if token not in self.token_to_id:
                ids.append(self.token_to_id['<UNK>'])
            else:
                ids.append(self.token_to_id[token])

        return ids

    def decode(self, ids):
        
        return ''.join(self.id_to_token[id] for id in ids)

