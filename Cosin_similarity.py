# # 3_rewriter_template.py
# import os
# from docx import Document
# from sentence_transformers import SentenceTransformer, util
# import torch
# import ast
#
#
# def extract_section(file_path, section_name):
#     """Extract a list from parsed NER output."""
#     with open(file_path, "r", encoding="utf-8") as f:
#         for line in f:
#             if line.startswith(f"{section_name}:"):
#                 return ast.literal_eval(line.split(":", 1)[1].strip())
#     return []
#
#
# def generate_ats_resume(cv_data_path, jd_data_path, output_dir):
#     # --- Extract data
#     cv_skills = extract_section(cv_data_path, "SKILLS")
#     jd_skills = extract_section(jd_data_path, "SKILLS")
#     cv_exp = extract_section(cv_data_path, "EXPERIENCE")
#     cv_projects = extract_section(cv_data_path, "PROJECTS")
#     cv_education = extract_section(cv_data_path, "EDUCATION")
#     cv_name = extract_section(cv_data_path, "NAME")
#
#     # --- Compute matched skills
#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     if cv_skills and jd_skills:
#         cv_emb = model.encode(cv_skills, convert_to_tensor=True)
#         jd_emb = model.encode(jd_skills, convert_to_tensor=True)
#         cosine_scores = util.cos_sim(cv_emb, jd_emb)
#         matched_skills = [cv_skills[i] for i in range(len(cv_skills))
#                           if torch.max(cosine_scores[i]) > 0.5]
#     else:
#         matched_skills = cv_skills
#
#     # --- Missing / recommended skills
#     missing_skills = [s for s in jd_skills if s not in matched_skills]
#
#     # --- Rewriting experience with skill tags
#     rewritten_exp = []
#     for sentence in cv_exp:
#         relevant_skills = [s for s in matched_skills if s.lower() in sentence.lower()]
#         if relevant_skills:
#             rewritten_exp.append(f"{sentence} (Skills: {', '.join(relevant_skills)})")
#         else:
#             rewritten_exp.append(sentence)
#
#     # --- Create DOCX using ATS template ---
#     doc = Document()
#
#     # Name & Contact Info (placeholder)
#     if cv_name:
#         doc.add_heading(cv_name[0], level=0)
#     doc.add_paragraph("Email: [your email] | Phone: [your phone] | LinkedIn: [your linkedin]")
#
#     # Professional Summary
#     doc.add_heading("Professional Summary", level=1)
#     doc.add_paragraph(
#         "Experienced software professional seeking roles in data science and machine learning. "
#         "Skilled in software development, machine learning, and AI applications."
#     )
#
#     # Skills
#     doc.add_heading("Skills", level=1)
#     doc.add_paragraph(", ".join(matched_skills))
#
#     # Recommended Skills
#     doc.add_heading("Recommended Skills to Learn", level=1)
#     doc.add_paragraph(", ".join(missing_skills))
#
#     # Experience / Projects
#     doc.add_heading("Experience / Projects", level=1)
#     for exp in rewritten_exp:
#         doc.add_paragraph(exp)
#     for proj in cv_projects:
#         doc.add_paragraph(proj)
#
#     # Education
#     doc.add_heading("Education", level=1)
#     for edu in cv_education:
#         doc.add_paragraph(edu)
#
#     # Optional: Other info / certifications
#     doc.add_heading("Additional Information", level=1)
#     doc.add_paragraph("Certifications, Achievements, or Interests can be added here.")
#
#     # Save
#     os.makedirs(output_dir, exist_ok=True)
#     save_path = os.path.join(output_dir, "ATS_Optimized_Resume.docx")
#     doc.save(save_path)
#     print(f"✅ ATS Resume saved at {save_path}")
#
#
# if __name__ == "__main__":
#     generate_ats_resume(
#         "ML/CV/CV_NER_output.txt",
#         "ML/Job_Description/JD_NER_output.txt",
#         r"C:\Users\HP\OneDrive\Desktop\Major"
#     )



from sentence_transformers import SentenceTransformer, util
import ast

# File paths
CV_file_path = "ML/CV/CV_NER_output.txt"
JD_file_path = "ML/Job_Description/JD_NER_output.txt"
output_file = "cos_sim_output.txt"

# Function to extract SKILLS from structured NER output
def extract_skills(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("SKILLS:"):
                skills_str = line.split(":", 1)[1].strip()
                return ast.literal_eval(skills_str)
    return []

# Extract skills from CV and JD
cv_skills = extract_skills(CV_file_path)
jd_skills = extract_skills(JD_file_path)

# Clean data: remove None or non-string entries
cv_skills = [s for s in cv_skills if s and isinstance(s, str)]
jd_skills = [s for s in jd_skills if s and isinstance(s, str)]

# Load SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode skills into embeddings
cv_emb = model.encode(cv_skills, convert_to_tensor=True)
jd_emb = model.encode(jd_skills, convert_to_tensor=True)

# Compute cosine similarity
cosine_scores = util.cos_sim(cv_emb, jd_emb)

# Threshold for matching
threshold = 0.5

# Write all matches above threshold to file
with open(output_file, "w", encoding="utf-8") as out:
    for i, cv_skill in enumerate(cv_skills):
        for j, jd_skill in enumerate(jd_skills):
            score = float(cosine_scores[i][j])  # Convert tensor to float
            if score <= threshold:
                line = f"CV skill '{cv_skill}' matches JD skill '{jd_skill}' with similarity {score:.2f}\n"
                # line = str(score)+", "
                out.write(line)
                print(line.strip())

print(f"\n✅ All matches above {threshold} saved to '{output_file}' successfully!")