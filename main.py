from dotenv import load_dotenv
load_dotenv()

import os
from rag_core.pdf_preprocessor import extract_text_ocr, save_text
from rag_core.text_chunking import generate_chunks, save_chunks
from rag_core.vector_embedding import VectorDB
from rag_tests.rag_evaluation import run_evaluation

#File paths
pdf_path = "knowledge-base/HSC26-Bangla1st-Paper.pdf"
preprocessed_path = "outputs/preprocessed_text.txt"
chunks_path = "outputs/all_chunks.jsonl"
index_path = "vectorstore"
poppler_path = "C:/poppler/Library/bin"

#Preprocessing
text = extract_text_ocr(pdf_path, poppler_path=poppler_path)
save_text(text, preprocessed_path)
print(f"Preprocessing completed and saved to '{preprocessed_path}'\n")

#Chunking
chunks = generate_chunks(text)
save_chunks(chunks, chunks_path)
print(f"Chunked into {len(chunks)} pieces and saved to '{chunks_path}'\n")

#Embedding
os.makedirs(index_path, exist_ok=True)
vector_db = VectorDB()
vector_db.create_index(chunks, save_path=index_path)
print(f"Embedding completed and saved to '{index_path}'\n")


#RAG evaluation
run_evaluation()
