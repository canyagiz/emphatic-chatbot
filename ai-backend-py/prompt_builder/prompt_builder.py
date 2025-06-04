from typing import List, Dict

def format_user_info(user_metadata: Dict) -> str:
    if not user_metadata:
        return "No user metadata available."
    
    lines = [f"- {key}: {value}" for key, value in user_metadata.items()]
    return "\n".join(lines)


def format_chat_history(history: List[Dict]) -> str:
    messages = []
    for msg in history:
        role = msg["role"]
        content = msg["content"]
        messages.append(f"{role.capitalize()}: {content}")
    return "\n".join(messages)


def format_memories(memories: List[Dict]) -> str:
    if not memories:
        return "No relevant memories found."
    return "\n".join(f"- {m['content']}" for m in memories)

def format_session_summaries(summaries: List[Dict]) -> str:
    if not summaries:
        return "No previous summaries."
    return "\n\n".join(f"Summary {i+1}:\n{s['summary_text']}" for i, s in enumerate(summaries))


def build_prompt(
    user_prompt: str,
    user_metadata: Dict,
    session_summaries: List[Dict],
    session_history: List[Dict],
    relevant_memories: List[Dict],
) -> str:
    return f"""
# 👤 Known user information:
{format_user_info(user_metadata)}

# 🧠 Relevant memories:
{format_memories(relevant_memories)}

# 📚 Conversation summary so far:
{format_session_summaries(session_summaries)}

# 💬 Ongoing session history (not yet summarized):
{format_chat_history(session_history)}

# 🗣️ User's latest message:
User: {user_prompt}
"""

