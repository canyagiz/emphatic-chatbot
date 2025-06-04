from supabase import create_client, Client
from openai import OpenAI

import tiktoken

import os
from dotenv import load_dotenv

from typing import List, Dict

load_dotenv()

SUPABASE_URL = os.getenv("PUBLIC_URL")
SUPABASE_KEY = os.getenv("PUBLIC_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_all_session_summaries(session_id: str) -> List[dict]:
    response = supabase.table("session_summary") \
                .select("summary_text, message_start_id, message_end_id") \
                .eq("session_id", session_id) \
                .order("created_at", desc=False) \
                .execute()

    return response.data or []

def get_chat_history_after(session_id: str, after_id: int) -> List[dict]:
    response = supabase.table("chat_history") \
        .select("id, role, content, created_at") \
        .eq("session_id", session_id) \
        .gt("id", after_id) \
        .order("created_at", desc=False) \
        .execute()
    return response.data or []

def insert_session_summary(
    user_id: str,
    session_id: str,
    summary_text: str,
    message_start_id: int,
    message_end_id: int
) -> None:
    supabase.table("session_summary").insert({
        "user_id": user_id,
        "session_id": session_id,
        "summary_text": summary_text,
        "message_start_id": message_start_id,
        "message_end_id": message_end_id
    }).execute()

def calculate_token_count(messages: List[Dict]) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    total_tokens = 0
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        # token count for role + content 
        tokens = len(encoding.encode(role)) + len(encoding.encode(content))
        # Overhead
        total_tokens += tokens + 4

    return total_tokens

def summarize_session(history: List[Dict]) -> str:
    # Chat geçmişini string olarak biçimlendir
    formatted = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in history)

    system_prompt = (
        "You are an assistant that summarizes conversations.\n"
        "Summarize the following user-assistant interaction in a concise and informative way.\n"
        "Keep important context, emotions, and topics.\n"
        "Output should be neutral and 3–5 sentences max.\n"
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": formatted}
        ],
        temperature=0.3,
        max_tokens=300
    )

    return completion.choices[0].message.content.strip()
