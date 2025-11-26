import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Step 1: Read tokenized CV from file
with open("1(tokenized).txt", "r", encoding="utf-8") as f:
    tokens = f.read().split()  # assuming tokens are space-separated

# Step 1a: Capitalize tokens to help NER
capitalized_tokens = [t.capitalize() for t in tokens]

# Convert tokens back to string
cv_text = " ".join(capitalized_tokens)

# Step 2: Apply NER
doc = nlp(cv_text)
entities = [(ent.text, ent.label_) for ent in doc.ents]

print("NER Entities:")
for e in entities:
    print(e)

# Step 3: Parse into sections
section_headers = ["Name", "Education", "Experience", "Skills", "Projects", "Certifications"]
pattern = r'(?i)(name|education|experience|skills|projects|certifications)\s*:?'  # optional colon
sections = re.split(pattern, cv_text)

# Build structured CV dictionary
cv_data = {}
current_section = "Name"  # assume first section is Name
cv_data[current_section] = sections[0].strip()  # text before first header

for i in range(1, len(sections), 2):
    header = sections[i].replace(":", "").strip()
    content = sections[i+1].strip() if i + 1 < len(sections) else ""
    cv_data[header] = content

# Step 4: Map NER entities to sections
for ent_text, ent_label in entities:
    if ent_label == "PERSON" and "Name" in cv_data and not cv_data["Name"]:
        cv_data["Name"] = ent_text
    elif ent_label == "ORG":
        if "Education" in cv_data and cv_data["Education"]:
            if ent_text not in cv_data["Education"]:
                cv_data["Education"] += f", {ent_text}"
        elif "Experience" in cv_data:
            if ent_text not in cv_data["Experience"]:
                cv_data["Experience"] += f", {ent_text}"
    elif ent_label == "DATE":
        if "Education" in cv_data and re.search(r'\d{4}', cv_data["Education"]):
            cv_data["Education"] += f", {ent_text}"
        elif "Experience" in cv_data:
            cv_data["Experience"] += f", {ent_text}"

# Step 5: Optional: extract skills from keyword list
skills_list = ["Python", "C++", "Java", "Machine Learning", "Data Science"]
cv_data["Skills"] = [skill for skill in skills_list if skill in cv_text]

# Step 6: Output structured CV
print("\nStructured CV Dictionary:")
for key, value in cv_data.items():
    print(f"{key}: {value}")

# ✅ Fixed NER display
print("\nExtracting NER:")
for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")
