from supabase import create_client, Client
import os

from dotenv import load_dotenv
from typing import Optional

load_dotenv()

SUPABASE_URL = os.getenv("PUBLIC_URL")
SUPABASE_KEY = os.getenv("PUBLIC_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# User
def get_user_metadata(user_id: str) -> dict:
    response = supabase.table("users").select("user_metadata").eq("id", user_id).single().execute()
    return response.data["user_metadata"] if response.data else {}

# Chat history
def get_session_history(user_id: str, session_id: str) -> list:
    response = supabase.table("chat_history") \
        .select("role, content") \
        .eq("user_id", user_id) \
        .eq("session_id", session_id) \
        .order("created_at", desc=False) \
        .execute()
    return response.data if response.data else []

def insert_message(user_id: str, session_id: str, role: str, content: str):
    supabase.table("chat_history").insert({
        "user_id": user_id,
        "session_id": session_id,
        "role": role,
        "content": content
    }).execute()

# Session Summary
def get_session_summary(session_id: str) -> Optional[str]:
    response = supabase.table("session_summary").select("summary_text").eq("session_id", session_id).execute()
    if response.data:
        return response.data[0]["summary_text"]
    return None






