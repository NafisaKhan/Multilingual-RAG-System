# Multilingual RAG System

This project is a Retrieval-Augmented Generation (RAG) system built to answer questions from knowledge-base, specifically HSC Bangla 1st Paper PDFs. It supports both Bangla and English queries and uses semantic similarity search combined with generative AI (Gemini) for generating context-based answers.

# Setup Guide:

. Step 1: Clone the repository
  git clone https://github.com/NafisaKhan/Multilingual-RAG-System.git
. Step 2: Navigate into the project directory
  cd Multilingual-RAG-System
. Step 3: Create a virtual environment
  python -m venv venv
. Step 4: Activate the virtual environment
  On Windows: venv\Scripts\activate
  On macOS/Linux: source venv/bin/activate
. Step 5: Install required packages
  pip install -r requirements.txt
. Step 6: Create a .env file with your Gemini API key and inside .env file add the line:
  GEMINI_API_KEY=your-gemini-api-key-here
. Step 7: Run the main file (entry-point)
  python main.py
. Step 8: Start the FastAPI server
  uvicorn api:app --reload
. Step 9: Open the frontend in Streamlit UI
  streamlit run app.py


# Used Tools, Libraries, and Packages:

* FastAPI – Used in api.py to create backend endpoints for question answering.
* Streamlit – Used in app.py to build a simple user interface for querying the system.
* google-generativeai – Used in answer_generation.py to call Gemini API for final response generation.
* faiss-cpu – Used in vector_embedding.py for indexing and performing similarity search on embedded chunks.
* langchain – Used throughout the embedding and retrieval flow via vector_embedding.py and chunk_retrieval.py.
* langchain-huggingface – Used to load the HuggingFace embedding model for multilingual vector generation.
* langchain-community, langchain-core, langchain-text-splitters – Required by Langchain modules used for FAISS and document handling.
* sentence-transformers – Used to provide the multilingual embedding model (distiluse-base-multilingual-cased-v1).
* pytesseract – Used in pdf_preprocessor.py to extract text from scanned PDF pages via OCR.
* pdf2image – Used in pdf_preprocessor.py to convert PDF pages to images for OCR.
* Pillow – Used to preprocess images (grayscale, thresholding) before OCR.
* python-dotenv – Used to load environment variables like API keys in multiple files (api.py, main.py, etc.).
* requests – Used in app.py to send POST requests from Streamlit to the FastAPI backend.
* pandas – Used in rag_evaluation.py to manage evaluation result storage and CSV export.
* tqdm – Used in main.py to show progress during processing.
* regex – Used in text_chunking.py and pdf_preprocessor.py for advanced pattern matching and cleanup.
* numpy – Imported as a dependency for other libraries (FAISS).


# Sample Queries and Outputs:


# API Documentation:

  The FastAPI Swagger UI is available at /docs when the server is running and click "Try it out" button in the right and paste the question and get generated answer


# Evaluation Matrix:

  The evaluation script evaluates predicted answers against the given sample test cases using below metrics and results are saved as a CSV file in rag_tests/evaluation_results.csv.
  
  * Human match (exactness with expected answer)
  * Groundedness (whether the answer content appears in retrieved chunks)
  * Relevance (whether expected content appears in retrieved chunks)
  * Cosine similarity score (from FAISS retrieval)


# Assessment Questions:


