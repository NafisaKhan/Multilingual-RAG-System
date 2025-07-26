import os
from typing import List, Dict

chat_history_path = "outputs/chat_history.txt"
max_history_limit = 6

def load_chat_history(limit=max_history_limit) -> List[Dict[str, str]]:
    if not os.path.exists(chat_history_path):
        return []
    with open(chat_history_path, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
    history = []
    for block in blocks[-limit:]:
        lines = block.strip().split("\n")
        if len(lines) >= 2:
            user = lines[0].replace("User: ", "").strip()
            system = lines[1].replace("System: ", "").strip()
            history.append({"user": user, "system": system})
    return history

def save_chat_history(user_message: str, system_message: str):
    os.makedirs("outputs", exist_ok=True)
    with open(chat_history_path, "a", encoding="utf-8") as f:
        f.write(f"User Question: {user_message}\n")
        f.write(f"System Answer: {system_message}\n\n")

def reset_chat_history():
    os.makedirs("outputs", exist_ok=True)
    with open(chat_history_path, "w", encoding="utf-8") as f:
        f.write("")
