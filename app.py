import streamlit as st
import tempfile
import os
import PyPDF2
import re
import cohere

# ✅ Hard-coded API Key (replace with your key)
co = cohere.Client("d3cNfKXM9EbiHe6Y15D2Se7TDAf6edgPD4bjjePp")

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

# ✅ Summarization using Cohere Chat API
def cohere_summarize(text):
    if not text.strip():
        return "Document is empty."

    response = co.chat(
        model="command",
        message=f"Summarize the following document clearly:\n\n{text[:4000]}"
    )
    return response.text.strip()

# ✅ Answer Generation using Cohere Chat API
def cohere_generate_answer(document_text, question):
    if not document_text.strip() or not question.strip():
        return "Empty input."

    response = co.chat(
        model="command",
        message=f"Answer the question strictly based on the given document.\n\nDocument:\n{document_text[:4000]}\n\nQuestion: {question}\nAnswer:"
    )
    return response.text.strip()

# ✅ Challenge Question Generator
def generate_dynamic_logic_questions(document_text):
    response = co.chat(
        model="command",
        message=f"Generate exactly 3 logical comprehension questions based on this document:\n\n{document_text[:4000]}\n\nProvide each question on a new line."
    )

    questions = response.text.strip().splitlines()
    return [q.strip("-• ").strip() for q in questions if q.strip()][:3]

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

st.set_page_config(page_title="GenAI Research Assistant", layout="centered")
st.title("GenAI Research Assistant")

st.header("Upload Document")
doc_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if doc_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=doc_file.name[-4:]) as tmp_file:
        tmp_file.write(doc_file.read())
        path = tmp_file.name

    file_type = 'pdf' if doc_file.name.endswith(".pdf") else 'txt'
    if file_type == 'pdf':
        pages_content = extract_text_with_page_numbers(path)
        full_text = " ".join([clean_text(content) for _, content in pages_content])
    else:
        with open(path, "r", encoding="utf-8") as f:
            full_text = clean_text(f.read())
        pages_content = [(1, full_text)]

    st.success("✅ File uploaded and processed successfully!")

    st.subheader("Summary")
    summary = cohere_summarize(full_text)
    st.info(summary)

    st.header("2. Ask Anything")
    question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if question:
            answer = cohere_generate_answer(full_text, question)
            paragraph, page = search_best_paragraph_with_reference(pages_content, question)
            st.success("Answer:")
            st.write(answer)
            st.caption(f"📄 Reference: Page {page if page else 'Unknown'}")
            st.code(paragraph, language="markdown")
        else:
            st.warning("Please enter a question.")

    st.header("3. Challenge Me!")
    if 'challenge_questions' not in st.session_state:
        st.session_state['challenge_questions'] = []
        st.session_state['challenge_started'] = False

    if st.button("🎯 Generate Challenge"):
        st.session_state['challenge_questions'] = generate_dynamic_logic_questions(full_text)
        st.session_state['challenge_started'] = True

    if st.session_state.get("challenge_started") and st.session_state['challenge_questions']:
        st.subheader("Answer These 3 Questions:")
        for i, q in enumerate(st.session_state['challenge_questions'][:3], 1):
            st.markdown(f"**Q{i}:** {q}")

        user_response = st.text_area("Write your answers (one per line):")

        if st.button("Submit Answers"):
            answers = user_response.strip().split("\n")
            if len(answers) != 3:
                st.error("⚠️ Please answer all 3 questions.")
            else:
                st.subheader("✅ Feedback:")
                for i, (q, ans) in enumerate(zip(st.session_state['challenge_questions'][:3], answers), 1):
                    correct = cohere_generate_answer(full_text, q)
                    para, page = search_best_paragraph_with_reference(pages_content, q)
                    st.markdown(f"**Q{i}:** {q}")
                    st.markdown(f"**Your Answer:** {ans}")
                    st.markdown(f"**Correct Answer:** {correct}")
                    st.caption(f"📄 Page {page if page else 'Unknown'}")
                    st.code(para, language="markdown")
                    st.write("---")

    os.remove(path)
