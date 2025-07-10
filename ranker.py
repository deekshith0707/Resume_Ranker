import os
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Failed to process {pdf_path}: {e}")
        return ""

def rank_resumes():
    resumes_dir = 'resumes'
    job_desc_file = 'job_description.txt'

    with open(job_desc_file, 'r') as f:
        job_description = f.read()

    resumes = []
    resume_files = os.listdir(resumes_dir)

    for file in resume_files:
        if file.endswith('.pdf'):
            resume_path = os.path.join(resumes_dir, file)
            text = extract_text_from_pdf(resume_path)
            if text.strip():
                resumes.append((file, text))

    if not resumes:
        print("No resumes found or text could not be extracted.")
        return []

    documents = [job_description] + [r[1] for r in resumes]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    if tfidf_matrix.shape[0] < 2:
        print("Insufficient data for comparison.")
        return []

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    ranked = sorted(zip([r[0] for r in resumes], similarity_scores), key=lambda x: x[1], reverse=True)

    return ranked
