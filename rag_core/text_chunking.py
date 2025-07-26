import re
import json

def extract_mcqs(text):
    block_pattern = re.compile(
        r"([০-৯]{1,3})।\s*(.*?)\s*\(?[ক]\)?\s*(.*?)\s*\(?[খ]\)?\s*(.*?)\s*\(?[গ]\)?\s*(.*?)\s*\(?[ঘ]\)?\s*(.*?)(?=\n[০-৯]{1,3}।|\Z)",
        re.DOTALL
    )
    inline_pattern = re.compile(
        r"([০-৯]{1,3})।\s*(.*?)\s*[ক]\)\s*(.*?)\s*[খ]\)\s*(.*?)\s*[গ]\)\s*(.*?)\s*[ঘ]\)\s*(.*?)(?=\n[০-৯]{1,3}।|\Z)",
        re.DOTALL
    )
    all_matches = block_pattern.findall(text) + inline_pattern.findall(text)
    mcqs = {}

    for match in all_matches:
        num, q, ka, kha, ga, gha = match[:6]
        q = re.sub(r"(?<=\?)\s.*", "", q).strip()
        mcqs[num.strip()] = {
            "type": "mcq",
            "number": num.strip(),
            "question": q,
            "options": {
                "ক": ka.strip(),
                "খ": kha.strip(),
                "গ": ga.strip(),
                "ঘ": gha.strip()
            }
        }
    return mcqs

def extract_global_answer_keys(text):
    return dict(re.findall(r"([০-৯]{1,3})\s*([কখগঘ])", text))

def map_mcq_answers(mcqs, answer_keys):
    for num, mcq in mcqs.items():
        ans = answer_keys.get(num)
        if ans and ans in mcq["options"]:
            mcq["correct_option"] = ans
            mcq["correct_answer"] = mcq["options"][ans]
    return mcqs

def split_into_chunks(text, max_chars=400, overlap=50):
    sentences = re.split(r"(?<=[।!?])\s+", text.strip())
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < max_chars:
            chunk += sentence + " "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + " "
    if chunk.strip():
        chunks.append(chunk.strip())

    #Overlap for context continuity
    final_chunks = []
    for i in range(len(chunks)):
        start = max(0, i - 1)
        combined = " ".join(chunks[start:i+1])
        final_chunks.append({
            "type": "paragraph",
            "text": combined.strip()
        })
    return final_chunks

def generate_chunks(text):
    chunks = []
    global_answers = extract_global_answer_keys(text)
    pages = re.split(r"=== PAGE \d+ ===", text)

    for i, page in enumerate(pages):
        page = page.strip()
        if not page:
            continue
        print(f"Page {i+1}...")

        if len(re.findall(r"[০-৯]{1,3}।", page)) >= 3 and any(opt in page for opt in ["(ক)", "ক)", "(খ)", "খ)"]):
            print("MCQs Content")
            mcqs = extract_mcqs(page)
            mcqs = map_mcq_answers(mcqs, global_answers)
            for mcq in mcqs.values():
                q = mcq["question"]
                opts = mcq["options"]
                mcq["text"] = f"{q}\n(ক) {opts['ক']}\n(খ) {opts['খ']}\n(গ) {opts['গ']}\n(ঘ) {opts['ঘ']}"
                if "correct_option" in mcq:
                    mcq["text"] += f"\nসঠিক উত্তর: ({mcq['correct_option']}) {mcq['correct_answer']}"
                chunks.append(mcq)
        else:
            print("Paragraph Content")
            paragraph_chunks = split_into_chunks(page)
            chunks.extend(paragraph_chunks)

    return chunks

def save_chunks(chunks, path):
    with open(path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
