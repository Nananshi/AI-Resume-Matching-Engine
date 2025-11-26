import spacy
import os

# Load spaCy transformer model
nlp = spacy.load("en_core_web_trf")

# Keyword sets
SKILL_KEYWORDS = {
    "python", "java", "c++", "machine learning", "deep learning", "data science",
    "sql", "power bi", "excel", "pandas", "numpy", "matplotlib", "seaborn",
    "tensorflow", "keras", "pytorch", "nlp", "transformers", "scikit-learn",
    "flask", "django", "fastapi", "aws", "azure", "git", "github", "linux"
}

EXPERIENCE_KEYWORDS = {
    "internship", "project", "developed", "engineer", "research",
    "experience", "worked", "implemented", "analyzed", "designed", "built"
}

EDU_KEYWORDS = {"b.tech", "m.tech", "bachelor", "master", "phd", "university", "college", "institute"}

def parse_text_to_structured(ner_file, skill_file, output_file):
    """Parse text for structured data using NER + keywords."""
    # --- NER-friendly text
    with open(ner_file, "r", encoding="utf-8") as f:
        text = f.read()
    doc = nlp(text)

    # --- Skills-friendly lowercase token text
    with open(skill_file, "r", encoding="utf-8") as f:
        skill_text = f.read().lower()

    structured_data = {
        "NAME": set(),
        "ORG": set(),
        "EDUCATION": set(),
        "EXPERIENCE": set(),
        "SKILLS": set(),
        "PROJECTS": set()
    }

    # --- NER extraction ---
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            structured_data["NAME"].add(ent.text)
        elif ent.label_ == "ORG":
            structured_data["ORG"].add(ent.text)
        elif ent.label_ in ["EDUCATION", "FAC"]:
            structured_data["EDUCATION"].add(ent.text)
        elif ent.label_ in ["WORK_OF_ART", "PRODUCT"]:
            structured_data["PROJECTS"].add(ent.text)

    # --- Keyword matching ---
    for skill in SKILL_KEYWORDS:
        if skill in skill_text:
            structured_data["SKILLS"].add(skill)

    for exp_word in EXPERIENCE_KEYWORDS:
        if exp_word in skill_text:
            structured_data["EXPERIENCE"].add(exp_word)

    # --- Convert sets to lists ---
    structured_data = {k: sorted(list(v)) for k, v in structured_data.items()}

    # --- Save structured data ---
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as out:
        for k, v in structured_data.items():
            out.write(f"{k}: {v}\n")

    print(f"✅ Parsed data saved at: {output_file}")
    return structured_data

if __name__ == "__main__":
    parse_text_to_structured("CV/CV_cleaned_for_ner.txt", "CV/CV_cleaned.txt", "CV/CV_NER_output.txt")
    parse_text_to_structured("JD/JD_cleaned_for_ner.txt", "JD/JD_cleaned.txt", "JD/JD_NER_output.txt")
