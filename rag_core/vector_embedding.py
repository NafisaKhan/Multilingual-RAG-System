from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os

class VectorDB:
    def __init__(self, model_name="sentence-transformers/distiluse-base-multilingual-cased-v1"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.db = None

    def prepare_documents(self, chunks):
        docs = []
        for chunk in chunks:
            if isinstance(chunk, dict):
                if chunk.get("type") == "mcq":
                    content = chunk.get("question", "")
                    options_text = " ".join([f"({k}) {v}" for k, v in chunk.get("options", {}).items()])
                    content = f"{content} {options_text}".strip()
                else:
                    content = chunk.get("text", "")
                docs.append(Document(page_content=content, metadata=chunk))
            else:
                docs.append(Document(page_content=chunk, metadata={}))
        return docs

    def create_index(self, chunks, save_path="kb_vectorstore"):
        docs = self.prepare_documents(chunks)
        self.db = FAISS.from_documents(docs, self.embeddings)
        self.db.save_local(save_path)
        print(f"FAISS index is created.")

    def load_index(self, load_path="kb_vectorstore"):
        self.db = FAISS.load_local(
            load_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"FAISS index is loaded from {load_path}")

    def query(self, question, top_k=3):
        if self.db is None:
            raise ValueError("Vector DB not loaded.")
        results = self.db.similarity_search(question, k=top_k)
        return [
            {
                "text": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in results
        ]

    def query_scores(self, query, top_k=3):
        if self.db is None:
            raise ValueError("Vector DB not loaded.")
        results = self.db.similarity_search_with_score(query, k=top_k)
        return [{"text": doc.page_content, "score": score} for doc, score in results]
