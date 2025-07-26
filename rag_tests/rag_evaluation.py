import os
import csv
from rag_core.answer_generation import AnswerGenerator
from rag_core.vector_embedding import VectorDB

test_cases_path = "rag_tests/test-cases.txt"
evaluation_results_path = "rag_tests/evaluation_results.csv"

def load_test_cases(file_path):
    test_cases = []
    with open(file_path, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) == 2:
                question = lines[0].replace("User Question: ", "").strip()
                expected = lines[1].replace("Expected Answer: ", "").strip()
                test_cases.append({"question": question, "expected": expected})
    return test_cases

def check_groundedness(predicted, chunks):
    return any(predicted.strip() in chunk for chunk in chunks)

def check_relevance(expected, chunks):
    return any(expected.strip() in chunk for chunk in chunks)

def run_evaluation():
    test_cases = load_test_cases(test_cases_path)
    qa = AnswerGenerator(reset_memory=True)
    vector_db = VectorDB()
    vector_db.load_index("vectorstore")

    os.makedirs("rag_tests", exist_ok=True)
    results = []
    print(f"Running evaluation on {len(test_cases)} test cases:")
    for i, test in enumerate(test_cases, 1):
        question = test["question"]
        expected = test["expected"]

        #Top 3 chunks with similarity scores
        chunks_scores = vector_db.query_scores(question, top_k=3)
        chunks = [item["text"] for item in chunks_scores]
        scores = [item["score"] for item in chunks_scores]

        predicted = qa.generate_answer(question)
        if predicted is None:
            predicted = "No answer generated"
        #Evaluation Metrics
        human_match = predicted.strip() == expected.strip()
        grounded = check_groundedness(predicted, chunks)
        relevant = check_relevance(expected, chunks)
        results.append({
            "Test Case": i,
            "Question": question,
            "Expected": expected,
            "Predicted": predicted,
            "Human-Labeled Match": "Yes" if human_match else "No",
            "Grounded": "Yes" if grounded else "No",
            "Relevant": "Yes" if relevant else "No",
            "Cosine Similarity (Top 1)": round(scores[0], 4)
        })

    #Evaluation Results
    with open(evaluation_results_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Evaluation completed and result is saved to {evaluation_results_path}")
