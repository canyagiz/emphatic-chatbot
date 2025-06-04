from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os
from dotenv import load_dotenv
   
from prompt_builder.prompt_builder import build_prompt
# from memory.embedding import get_embedding
# from memory.vector_search import get_similar_memories
from supabase_client import get_user_metadata, get_session_history, insert_message

from session_utils.session_utils import get_all_session_summaries, calculate_token_count,get_chat_history_after,insert_session_summary, summarize_session 
from longterm_memory.vector_search import get_similar_memories  
from longterm_memory.vector_memory import insert_vector_memory

load_dotenv()
router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(data: ChatRequest):
    try:
        # 1. Girdi
        user_prompt = data.message
        user_id = data.user_id
        session_id = data.session_id

        # 2. Kullanıcı verileri + session_summary + context dışı memory
        user_metadata = get_user_metadata(user_id)
        session_summaries = get_all_session_summaries(session_id)

        # 3. Mevcut özetlerin kapsadığı son mesaj id'sini bul
        max_end_id = max((s["message_end_id"] for s in session_summaries if s["message_end_id"]), default=0)

        # 4. Özetlenmemiş chat geçmişini çek
        session_history = get_chat_history_after(session_id, max_end_id)

        # 5. Eğer token sayısı çok arttıysa yeni summary üret
        token_count = calculate_token_count(session_history)
        if token_count > 200 and session_history:
            summary_text = summarize_session(session_history)
            insert_session_summary(
                user_id=user_id,
                session_id=session_id,
                summary_text=summary_text,
                message_start_id=session_history[0]["id"],
                message_end_id=session_history[-1]["id"]
            )
            print("HEREERERERER")
            insert_vector_memory(
                user_id=user_id,
                content=summary_text,
                #tags=["summary"]
            )
            # yeni summary oluştuğu için prompta eski history'yi koyma
            session_summaries = get_all_session_summaries(session_id)
            session_history = []

        # 6. Vector memory 
        relevant_memories = [
            {"content": c}
            for c in get_similar_memories(user_id=user_id, query=user_prompt, top_k=5) # Stringify List[str]
        ]
        print(relevant_memories)

        # 7. Prompt oluştur
        prompt = build_prompt(
            user_prompt=user_prompt,
            user_metadata=user_metadata,
            session_summaries=session_summaries,
            session_history=session_history,
            relevant_memories=relevant_memories
        )
        print(prompt)
        print("/n----------------------/n")
        
        # 8. Chat Completion al
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": os.getenv("SYSTEM_PROMPT")},
                {"role": "user", "content": prompt}
            ]
        )
        assistant_reply = completion.choices[0].message.content

        # 9. DB'ye kaydet
        insert_message(user_id, session_id, "user", user_prompt)
        insert_message(user_id, session_id, "assistant", assistant_reply)

        return ChatResponse(response=assistant_reply)

    except Exception as e:
        print("Chat endpoint error:", e)
        raise HTTPException(status_code=500, detail=str(e))
