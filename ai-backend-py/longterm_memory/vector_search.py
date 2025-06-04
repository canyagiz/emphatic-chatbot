from typing import List
from supabase_client import supabase
from longterm_memory.embedding import get_embedding


def get_similar_memories(user_id: str, query: str, top_k: int = 5) -> List[str]:
    if not query.strip():
        return []

    query_embedding = get_embedding(query)

    try:
        response = supabase.rpc(
            "match_vector_memory",
            {
                "query_embedding": query_embedding,
                "match_user_id": user_id,
                "match_count": top_k
            }
        ).execute()

        if not hasattr(response, "data") or response.data is None:
            raise Exception("No data returned from RPC match_vector_memory.")

        return [record["content"] for record in response.data]

    except Exception as e:
        raise Exception(f"Benzer memory sorgusunda hata: {str(e)}")
