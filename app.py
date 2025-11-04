import streamlit as st
import tempfile
import os
import PyPDF2
import re
import google.generativeai as genai

# ✅ Hard-coded Gemini API Key
genai.configure(api_key="AIzaSyBJIy3kfLXupoBelBR0_ekjsgPxXzlzHRU")

model = genai.GenerativeModel("gemini-pro")

def extract_text_with_page_numbers(file_path):
    text_pages = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text_pages.append((i + 1, page_text.strip()))
    return text_pages

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# ✅ Summarization using Gemini
def gemini_summarize(text):
    if not text.strip():
        return "Document is empty."
    response = model.generate_content(f"Summarize clearly:\n\n{text[:6000]}")
    return response.text.strip()

# ✅ Answer generation using Gemini
def gemini_answer(document_text, question):
    response = model.generate_content(
        f"Answer the question based strictly on the document.\n\nDocument:\n{document_text[:6000]}\n\nQuestion: {question}\nAnswer:"
    )
    return response.text.strip()

# ✅ Generate 3 challenge questions
def generate_challenge_questions(document_text):
    response = model.generate_content(
        f"Generate exactly 3 comprehension questions based on this document:\n\n{document_text[:6000]}\n\nOne per line:"
    )
    questions = response.text.strip().splitlines()
    return [q.strip("-• ").strip() for q in questions][:3]

# ✅ Simple keyword search for reference
def search_best_paragraph_with_reference(text_pages, query):
    best_match = ""
    best_page = 0
    max_overlap = 0
    for page_num, content in text_pages:
        overlap = len(set(query.lower().split()) & set(content.lower().split()))
        if overlap > max_overlap:
            best_match = content[:400]
            best_page = page_num
            max_overlap = overlap
    return best_match.strip(), best_page

# ✅ Streamlit UI
st.set_page_config(page_title="GenAI Research Assistant", layout="centered")
st.title("GenAI Research Assistant")

st.header("Upload Document")
doc_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

if doc_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=doc_file.name[-4:]) as tmp_file:
        tmp_file.write(doc_file.read())
        path = tmp_file.name

    if doc_file.name.endswith(".pdf"):
        pages_content = extract_text_with_page_numbers(path)
        full_text = " ".join([clean_text(c) for _, c in pages_content])
    else:
        with open(path, "r", encoding="utf-8") as f:
            full_text = clean_text(f.read())
        pages_content = [(1, full_text)]

    st.success("✅ File processed!")

    st.subheader("Summary")
    st.info(gemini_summarize(full_text))

    st.header("Ask Anything")
    question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if question:
            answer = gemini_answer(full_text, question)
            paragraph, page = search_best_paragraph_with_reference(pages_content, question)
            st.success("Answer:")
            st.write(answer)
            st.caption(f"📄 Page: {page}")
            st.code(paragraph)
        else:
            st.warning("Enter a question before asking.")

    st.header("Challenge Me!")
    if st.button("Generate Challenge"):
        st.session_state['challenge_questions'] = generate_challenge_questions(full_text)

    if 'challenge_questions' in st.session_state:
        st.subheader("Answer the questions:")
        for i, q in enumerate(st.session_state['challenge_questions'], start=1):
            st.write(f"**Q{i}:** {q}")

    os.remove(path)
