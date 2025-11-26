import fitz

#
doc = fitz.open("1.pdf")
text = ""
for page in doc:
    text += page.get_text()

print(text)
# saving the file
with open("1(extracted).txt", "w", encoding="utf-8") as f:
    f.write(text)