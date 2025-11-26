import fitz
import re
import wordninja
import nltk
from nltk.corpus import stopwords
import os

nltk.download("stopwords", quiet=True)

def extract_text_from_pdf(pdf_path):
    """Extract raw text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# --- NER-friendly preprocessing ---
def preprocess_for_parsing(pdf_path, output_file):
    """Keep natural casing for NER, remove only unwanted symbols."""
    text = extract_text_from_pdf(pdf_path)
    # Remove weird characters but keep punctuation for NER
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\-\(\)]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Preprocessed text for parsing saved at: {output_file}")

# --- Skills-friendly preprocessing ---
def preprocess_for_skills(pdf_path, output_file):
    """Lowercase, tokenize, remove stopwords for skill matching."""
    text = extract_text_from_pdf(pdf_path)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    tokens = wordninja.split(text)
    stop_words = set(stopwords.words("english"))
    filtered = [t for t in tokens if t not in stop_words]
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(filtered))
    print(f"✅ Preprocessed text for skills saved at: {output_file}")

if __name__ == "__main__":
    os.makedirs("CV", exist_ok=True)
    os.makedirs("JD", exist_ok=True)

    # Input files
    cv_pdf = "1.pdf"
    jd_pdf = "ML.pdf"

    # Preprocess
    preprocess_for_parsing(cv_pdf, "CV/CV_cleaned_for_ner.txt")
    preprocess_for_skills(cv_pdf, "CV/CV_cleaned.txt")

    preprocess_for_parsing(jd_pdf, "JD/JD_cleaned_for_ner.txt")
    preprocess_for_skills(jd_pdf, "JD/JD_cleaned.txt")
