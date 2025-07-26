import streamlit as st
import requests

#Streamlit app for the system
st.set_page_config(page_title="Multilingual RAG System", layout="centered")
st.title("Multilingual RAG System")
st.markdown("Ask any question from the **HSC Bangla 1st Paper** textbook.")
query = st.text_input("Enter your question:")

#Button handling
if st.button("Get Answer") and query.strip():
    with st.spinner("Searching answer..."):
        try:
            response = requests.post("http://localhost:8000/query", json={"question": query})
            data = response.json()
            st.success("Answer:")
            st.markdown(data["answer"])
        except Exception as e:
            st.error(f"Error: {e}")
  