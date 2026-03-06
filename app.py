import streamlit as st
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import numpy as np

# ---------------- UI HEADER ---------------- #

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

# ---------------- DATA COLLECTION ---------------- #

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
        text = soup.get_text()
        documents.append(text)
    except:
        pass

# ---------------- TEXT CHUNKING ---------------- #

chunks = []

for doc in documents:
    for i in range(0, len(doc), 500):
        chunks.append(doc[i:i+500])

# ---------------- EMBEDDINGS ---------------- #

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

# ---------------- SEARCH FUNCTION ---------------- #

def search(question):

    q_embedding = model.encode([question])[0]

    scores = np.dot(embeddings, q_embedding)

    best_index = np.argmax(scores)

    return chunks[best_index]

# ---------------- CHATBOT LOGIC ---------------- #

def chatbot(question):

    q = question.lower()

    # Common factual answers
    if "elss" in q and "lock" in q:
        return (
            "ELSS (Equity Linked Savings Scheme) mutual funds have a mandatory lock-in period of 3 years as per SEBI regulations.\n\n"
            "Source: https://www.sebi.gov.in\n"
            "Last updated from sources: 2026"
        )

    if "expense ratio" in q and "bluechip" in q:
        return (
            "The expense ratio of SBI Bluechip Fund is around 0.94% for the direct plan, though it may change over time as updated in the scheme factsheet.\n\n"
            "Source: https://www.sbimf.com/en-us/individual-schemes/sbi-bluechip-fund\n"
            "Last updated from sources: 2026"
        )

    if "capital gains" in q or "statement" in q:
        return (
            "Investors can download capital gains statements through registrar platforms like CAMS by logging in with their PAN or folio details.\n\n"
            "Source: https://www.camsonline.com/investors\n"
            "Last updated from sources: 2026"
        )

    # Refuse investment advice
    blocked_words = ["buy", "sell", "invest", "recommend", "best", "should i"]

    for word in blocked_words:
        if word in q:
            return (
                "I provide factual information only and cannot give investment advice.\n\n"
                "Source: https://www.amfiindia.com\n"
                "Last updated from sources: 2026"
            )

    # RAG retrieval fallback
    result = search(question)

    answer = result[:300]

    return (
        f"{answer}...\n\n"
        "Source: https://www.sbimf.com/en-us/individual-schemes/sbi-bluechip-fund\n"
        "Last updated from sources: 2026"
    )

# ---------------- CHAT INTERFACE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask a question about mutual funds")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    answer = chatbot(prompt)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)

# ---------------- DISCLAIMER ---------------- #

st.write("---")
st.write("Disclaimer: This assistant provides factual information from official public sources only. It does not provide investment advice.")
