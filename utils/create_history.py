import csv
import os
from pathlib import Path
from decouple import config
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories.file import FileChatMessageHistory

DIALOGS_CSV_FILE = config('DIALOGS_CSV_FILE')

def get_history(session_id: str) -> BaseChatMessageHistory:
    history_dir = Path("chat_history")
    history_dir.mkdir(exist_ok=True)
    return FileChatMessageHistory(file_path=str(history_dir / f"user_id_{session_id}.json"))

def log_dialog(user_id, user_name, timestamp, request, response):
    with open(DIALOGS_CSV_FILE, "a", encoding="utf-8") as f:
        f.write(f"id: {user_id}\n")
        f.write(f"name: {user_name}\n")
        f.write(f"datetime: {timestamp}\n")
        f.write(f'request: "{request}"\n')
        f.write(f'response: "{response}"\n')
        f.write("\n")

def get_dialogue_for_prompt(user_id: int, limit: int = 4) -> str:
    if not os.path.exists(DIALOGS_CSV_FILE):
        return ""

    with open(DIALOGS_CSV_FILE, encoding="utf-8") as f:
        raw = f.read().strip()
    if not raw:
        return ""

    blocks = raw.split("\n\n")
    filtered = [b for b in blocks if b.startswith(f"id: {user_id}\n")]
    last_blocks = filtered[-limit:]

    dialogue_lines = []
    for block in last_blocks:
        lines = block.splitlines()
        req = lines[3].split("request: ", 1)[1].strip().strip('"')
        resp = lines[4].split("response: ", 1)[1].strip().strip('"')
        dialogue_lines.append(f"Клиент: {req}")
        dialogue_lines.append(f"Менеджер: {resp}")

    return "\n".join(dialogue_lines)