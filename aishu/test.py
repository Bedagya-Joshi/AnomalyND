import streamlit as st
import docx2txt
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import defaultdict
import tempfile  # Import for temporary files

nltk.download('punkt_tab')  # For word_tokenize
nltk.download('stopwords')

def shingle(text, k):
    shingles = []
    for i in range(len(text) - k + 1):
        shingle = text[i:i+k]
        shingles.append(shingle)
    return shingles

def rabin_karp(text, pattern, q):
    d = 256  # Number of characters in the input alphabet
    m = len(pattern)
    n = len(text)
    h = 1
    p = 0
    t = 0
    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (p * d + ord(pattern[i])) % q
        t = (t * d + ord(text[i])) % q
    i = 0
    while i <= n - m:
        if p == t:
            if pattern == text[i:i+m]:
                return i
        if i < n - m:
            t = (t - ord(text[i]) * h) * d + ord(text[i + m])
            t = t % q
        i += 1
    return -1

def preprocess(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Stem the tokens
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    # Join the stemmed tokens back into a string
    preprocessed_text = " ".join(stemmed_tokens)
    return preprocessed_text

def calculate_similarity(text1, text2, k):
    shingles1 = shingle(preprocess(text1), k)
    shingles2 = shingle(preprocess(text2), k)
    intersection_count = len(set(shingles1) & set(shingles2))
    union_count = len(set(shingles1) | set(shingles2))
    if union_count == 0:
        return 0
    similarity = intersection_count / union_count
    return similarity

def detect_plagiarism(query_document, existing_document):
    similarity = calculate_similarity(query_document, existing_document, k=3)
    return similarity

def main():
    st.title("Plagiarism Detection")

    # Upload files (allow both .txt, .docx, and .pdf)
    uploaded_files = st.file_uploader("Upload Multiple Documents", type=["txt", "docx", "pdf"], accept_multiple_files=True)
    uploaded_file2 = st.file_uploader("Upload Document 2", type=["txt", "docx", "pdf"])

    if uploaded_files and uploaded_file2:
        # Extract text from uploaded files
        def extract_text(file):
            if file.type == "text/plain":
                return file.read().decode()
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return docx2txt.process(file)
            elif file.type == "application/pdf":
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(file.read())
                    # Use the unique temporary filename
                    with open(temp_file.name, 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text()
                        return text
                # Ensure temporary file is deleted after use
                os.remove(temp_file.name)
            else:
                st.error("Unsupported file format. Please upload a .txt, .docx, or .pdf file.")
                return None

        existing_text = extract_text(uploaded_file2)

        if existing_text:
            results = []
            for uploaded_file in uploaded_files:
                query_text = extract_text(uploaded_file)
                if query_text:
                    similarity = detect_plagiarism(query_text, existing_text)
                    results.append({"Document": uploaded_file.name, "Similarity Score": f"{similarity * 100:.2f}%"})
                else:
                    st.error(f"Error extracting text from {uploaded_file.name}")

            if results:
                st.write("Results")
                st.table(results)
        else:
            st.error("Error extracting text from the document to compare.")

if __name__ == "__main__":
    main()
