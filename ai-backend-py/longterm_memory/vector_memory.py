from typing import List, Optional
from supabase_client import supabase
from longterm_memory.embedding import get_embedding


def insert_vector_memory(user_id: str, content: str, tags: Optional[List[str]] = None) -> None:
    if not content.strip():
        raise ValueError("Empty content cannot be recorded to database.")

    embedding = get_embedding(content)

    record = {
        "user_id": user_id,
        "content": content,
        "embedding": embedding,
        # "tags": tags or [],
    }

    try:
        response = supabase.table("vector_memory").insert(record).execute()

        if not hasattr(response, "data") or response.data is None:
            raise Exception("Insert işleminden veri dönmedi.")
            
    except Exception as e:
        raise Exception(f"Vector memory record unsuccessful: {str(e)}")
