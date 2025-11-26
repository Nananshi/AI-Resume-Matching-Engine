import nltk     # Sometimes required if error persists
from nltk.tokenize import word_tokenize

# nltk.download('punkt')           # Make sure this runs without errors
# nltk.download('punkt_tab')

with open("1(normalized).txt", 'r', encoding='utf-8') as f:
    txt = f.read()


def tokenize(text):
    return word_tokenize(text)


tokenized_text = tokenize(txt)
with open("1(tokenized).txt", 'w', encoding="utf-8") as f:
    f.write(str(tokenized_text))