import streamlit as st
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import numpy as np

st.title("Mutual Fund FAQ Assistant")

st.write("Facts-only. No investment advice.")

st.write("Example questions you can try:")

st.write("• What is the expense ratio of SBI Bluechip Fund?")
st.write("• What is the ELSS lock-in period?")
st.write("• How can I download my capital gains statement?")
st.write("• What is the exit load of SBI Bluechip Fund?")

st.write("---")
st.write("AMC Covered: SBI Mutual Fund")

st.write("Schemes included:")
st.write("- SBI Bluechip Fund (Large Cap)")
st.write("- SBI Flexicap Fund")
st.write("- SBI Long Term Equity Fund (ELSS)")

st.write("Data sources: SBI Mutual Fund, AMFI India, SEBI and CAMS public pages.")

urls = [
"https://www.sbimf.com/en-us/individual-schemes/sbi-bluechip-fund",
"https://www.sbimf.com/en-us/individual-schemes/sbi-flexicap-fund",
"https://www.sbimf.com/en-us/individual-schemes/sbi-long-term-equity-fund",
"https://www.amfiindia.com/investor-corner/knowledge-center/what-are-mutual-funds",
"https://www.sebi.gov.in",
"https://www.camsonline.com/investors"
]

documents = []

for url in urls:
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        documents.append(soup.get_text())
    except:
        pass

chunks = []

for doc in documents:
    for i in range(0, len(doc), 500):
        chunks.append(doc[i:i+500])

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

def search(question):

    q_embedding = model.encode([question])[0]

    scores = np.dot(embeddings, q_embedding)

    best_index = np.argmax(scores)

    return chunks[best_index]

def chatbot(question):

    blocked_words = ["buy", "sell", "invest", "recommend", "best", "should i"]

    for word in blocked_words:
        if word in question.lower():
            return (
                "I provide factual information only and cannot give investment advice. "
                "Please refer to the official scheme documents.\n\n"
                "Source: https://www.amfiindia.com\n"
                "Last updated from sources: 2026"
            )

    result = search(question)

    answer = result[:300]

    return (
        f"{answer}...\n\n"
        "Source: https://www.sbimf.com/en-us/individual-schemes/sbi-bluechip-fund\n"
        "Last updated from sources: 2026"
    )

with st.form("question_form", clear_on_submit=True):

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input form
with st.form("question_form", clear_on_submit=True):

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input form
with st.form("question_form", clear_on_submit=True):

    question = st.text_input("Ask a question about mutual funds")

    submit = st.form_submit_button("Ask")

# Process question
if submit and question:

    answer = chatbot(question)

    st.session_state.history.append((question, answer))

# Show conversation history
for q, a in st.session_state.history:
    st.write("**User:**", q)
    st.write("**Assistant:**", a)
    st.write("---")

st.write("---")
st.write("Disclaimer: This assistant provides factual information from official public sources only. It does not provide investment advice.")
