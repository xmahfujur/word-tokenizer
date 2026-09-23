from loader import load_pdf
from Tokenizer import WordTokenizer

DATASETS_PATH = 'datasets'


load_pdf(DATASETS_PATH)

tokenizer = WordTokenizer()

tokenizer.train(tokenizer.tokens)

ids = tokenizer.encode('Hello My name is Mahfujur')
print(ids)
print(tokenizer.decode(ids))