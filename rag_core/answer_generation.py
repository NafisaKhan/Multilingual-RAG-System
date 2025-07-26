import os
from dotenv import load_dotenv
from rag_core.chat_history import load_chat_history, save_chat_history, reset_chat_history
from rag_core.chunk_retrieval import ChunkRetriever

#Load API key
load_dotenv()

#Gemini Setup
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    GEMINI_MODEL = "models/gemini-1.5-pro-latest"
    GEMINI_ENABLED = True
except ImportError:
    GEMINI_ENABLED = False

class AnswerGenerator:
    def __init__(self, vectorstore_path="vectorstore", reset_memory=True):
        self.retriever = ChunkRetriever(vectorstore_path=vectorstore_path)
        if reset_memory:
            reset_chat_history()

    def generate_with_gemini(self, query, context):
        if not GEMINI_ENABLED:
            return None
        try:
            prompt = f"""You are assisting users using information from a Bangla educational book. Generate only context-relevant answers."


Retrieved Context:
{context}


Question:
{query}

Answer:
"""
            model = genai.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(prompt)
            return response.text.strip() if response.text else None
        except Exception as e:
            print(f"[Gemini Error] {e}")
            return None

    def generate_answer(self, query, top_k=3):
        chunks = self.retriever.retrieve_chunks(query, top_k=top_k)

        os.makedirs("outputs", exist_ok=True)
        #Short-term memory context
        history = load_chat_history(limit=6)
        history_context = "\n".join([
            f"User: {h['user']}\nSystem: {h['system']}" for h in history
        ])
        doc_context = "\n\n".join([chunk["text"] for chunk in chunks])

        full_context = f"""
Recent Conversation:
{history_context}

Document Context:
{doc_context}
"""

        #Generate answer using Gemini
        answer = self.generate_with_gemini(query, full_context)
        if not answer:
            print(f"[Warning] Gemini failed to answer: {query}")
            answer = "No answer found."

        #Save to short-term memory
        save_chat_history(query, answer)

        #Save final answer
        with open("outputs/generated_answers.txt", "a", encoding="utf-8") as f:
            f.write(f"Question: {query}\n")
            f.write(f"Answer: {answer}\n\n")
        return answer
