from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    if not text.strip():
        raise ValueError("Empty text cannot be embedded.")
    
    response = client.embeddings.create(
        input=text,
        model=model
    )

    return response.data[0].embedding
