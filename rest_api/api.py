from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from rag_core.answer_generation import AnswerGenerator
import os

# Initialize FastAPI app
app = FastAPI(
    title="Multilingual RAG System API",
    description="Answer questions using RAG pipeline",
    version="1.0"
)

#Load RAG engine
qa = AnswerGenerator()

class QueryRequest(BaseModel):
    question: str

#POST endpoint for answering queries
@app.post("/query")
async def get_answer(request: QueryRequest):
    try:
        question = request.question.strip()
        answer = qa.generate_answer(question)
        with open("outputs/generated_answers.txt", "a", encoding="utf-8") as f:
            f.write(f"Q: {question}\nA: {answer}\n\n")
        return {"question": question, "answer": answer}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
