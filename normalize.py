import re
import wordninja

txt = open("1(extracted).txt")


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]+', '', text)
    text = re.sub(r'\s+', ' ', text)


    return text.strip()


normalized_text = wordninja.split(normalize_text(txt.read()))
with open("1(normalized).txt", 'w', encoding="utf-8") as f:
    f.write(' '.join(normalized_text))