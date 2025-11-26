import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

with open("1(tokenized).txt", 'r', encoding='utf-8') as f:
    text = f.read()

txt = eval(text)

stop_word = set(stopwords.words('english'))


def remove_stopword(tokens):
    return [w for w in tokens if w not in stop_word]


stop_wordless = remove_stopword(txt)
with open("1(stopped_word).txt", 'w', encoding="utf-8") as f:
    f.write(str(stop_wordless))

print('Number of words:', len(stop_wordless))