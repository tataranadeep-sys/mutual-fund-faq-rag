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

    blocked_words = ["buy","sell","invest","recommend","best"]

    for word in blocked_words:
        if word in question.lower():
            return "I provide factual information only. I cannot give investment advice. Please refer to official mutual fund documents."

    result = search(question)

    return result[:400]

question = st.text_input("Ask a question about mutual funds")

if question:

    answer = chatbot(question)

    st.write("Answer:")
    st.write(answer)

    st.write("Source: Official AMC / SEBI / AMFI page")
