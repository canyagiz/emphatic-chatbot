# emphatic-chatbot

**Long-Term Memory Chatbot with Supabase, Embeddings & Context Management**

This project implements a full-stack AI chatbot system powered by **Supabase** (PostgreSQL-based backend), **OpenAI embeddings**, and dynamic **context window management** for long-term memory support.

###  Key Features

* **Supabase Authentication & Policies**
  User management is handled via Supabase's `auth.users` and `public.users` tables with secure row-level security (RLS). A PostgreSQL trigger ensures each new auth user is mirrored in the public schema.

* **Session & Message Tracking**
  Each conversation is associated with a `session` and tracked in `chat_history`, enabling per-user memory storage and analysis. A `/sessions` endpoint allows listing and creating session records.

* **Embedding-Based Memory Search**
  Each user message is vectorized and stored in `vector_memory`. A custom Supabase RPC function retrieves semantically similar past messages using pgvector and cosine similarity.

* **Context Window Management**
  During each chat interaction, the current message is enriched with relevant past messages using similarity search and optional session summaries. A dynamic prompt builder assembles the context to fit within a model's token limit.

* **Session Summarization**
  Long sessions are periodically summarized and stored in `session_summary` for efficient recall and context compression.

###  Stack

* **Backend:** FastAPI (Python), OpenAI API
* **Database:** Supabase (PostgreSQL, pgvector, RLS, triggers)
* **Frontend:** Next.js 
* **Deployment:** Docker (planned)

###  UI
#### Sign Up Page
![image](https://github.com/user-attachments/assets/22c2726a-e019-4e19-bcfb-885426cbce0c)

#### Login Page
![image](https://github.com/user-attachments/assets/dc50f5b3-7d97-4bc7-be62-f01f7fb0c14e)

#### Welcoming Page
![image](https://github.com/user-attachments/assets/7eac584b-7cb7-4d19-a735-7268d747902f)

#### First Dialogue
![image](https://github.com/user-attachments/assets/eb09935b-5f51-4a44-a956-fc31f9f55ca8)

##### Initial Context window builded via embeddings and chat_history & session_summary tables
-  👤 Known user information:
No user metadata available.

# 🧠 Relevant memories:
No memory available.

# 📚 Conversation summary so far:
No previous summaries.

# 💬 Ongoing session history (not yet summarized):
User: Hello, I'm yağız
Assistant: Hello Yağız! How are you feeling today?
User: I have an exam tomorrow and I feel anxious
Assistant: I understand that you're feeling anxious about your exam tomorrow, Yağız. It's completely normal to feel that way before a big test. Remember, you've prepared well in advance, and you have the knowledge and skills needed to do your best. Is there anything specific that's triggering your anxiety right now, or would you like to talk more about how you're feeling?

# 🗣️ User's latest message:
User: I failed the first midterm and even if I've prepared well, ı will fail again...


##### Final Context window builded via embeddings and chat_history & session_summary tables
# 👤 Known user information:
Username: Yağız

# 🧠 Relevant memories:
- The user expressed feeling anxious about an upcoming exam despite being well-prepared. They sought tips beyond basic advice like deep breathing. The assistant suggested visualization techniques, creating a study routine with breaks, staying hydrated, eating well, and getting enough rest as specific ways to manage exam anxiety. The user was encouraged to practice these strategies to feel more prepared and confident for the exam.

# 📚 Conversation summary so far:
No previous summaries.

# 💬 Ongoing session history (not yet summarized):
User: Hello, I'm yağız
Assistant: Hello Yağız! How are you feeling today?
User: I have an exam tomorrow and I feel anxious
Assistant: I understand that you're feeling anxious about your exam tomorrow, Yağız. It's completely normal to feel that way before a big test. Remember, you've prepared well in advance, and you have the knowledge and skills needed to do your best. Is there anything specific that's triggering your anxiety right now, or would you like to talk more about how you're feeling?

# 🗣️ User's latest message:
User: I failed the first midterm and even if I've prepared well, ı will fail again...

/n----------------------/n
INFO:     192.168.1.66:63767 - "POST /chat HTTP/1.1" 200 OK
[{'content': 'The user expressed feeling anxious about an upcoming exam despite being well-prepared. They sought tips beyond basic advice like deep breathing. The assistant suggested visualization techniques, creating a study routine with breaks, staying hydrated, eating well, and getting enough rest as specific ways to manage exam anxiety. The user was encouraged to practice these strategies to feel more prepared and confident for the exam.'}]

# 👤 Known user information:
No user metadata available.

# 🧠 Relevant memories:
- The user expressed feeling anxious about an upcoming exam despite being well-prepared. They sought tips beyond basic advice like deep breathing. The assistant suggested visualization techniques, creating a study routine with breaks, staying hydrated, eating well, and getting enough rest as specific ways to manage exam anxiety. The user was encouraged to practice these strategies to feel more prepared and confident for the exam.

# 📚 Conversation summary so far:
No previous summaries.

# 💬 Ongoing session history (not yet summarized):


# 🗣️ User's latest message:
User: Hello again



# 👤 Known user information:
No user metadata available.

# 🧠 Relevant memories:
- The user expressed feeling anxious about an upcoming exam despite being well-prepared. They sought tips beyond basic advice like deep breathing. The assistant suggested visualization techniques, creating a study routine with breaks, staying hydrated, eating well, and getting enough rest as specific ways to manage exam anxiety. The user was encouraged to practice these strategies to feel more prepared and confident for the exam.
- User: Yağız
Assistant: Acknowledged user's name.
User: Feeling anxious about an upcoming exam.
Assistant: Validated user's feelings of anxiety and reassured them of their preparation. Encouraged user to focus on their progress and resilience. Discussed the impact of past failure on current anxiety and suggested reflecting on improvements made since then. Offered support and encouraged further discussion.

# 📚 Conversation summary so far:
Summary 1:
User: Yağız
Assistant: Acknowledged user's name.
User: Feeling anxious about an upcoming exam.
Assistant: Validated user's feelings of anxiety and reassured them of their preparation. Encouraged user to focus on their progress and resilience. Discussed the impact of past failure on current anxiety and suggested refle user was encouraged to practice these strategies to feel more prepared and confident for the exam.
- User: Yağız
Assistant: Acknowledged user's name.
User: Feeling anxious about an upcoming exam.
Assistant: Validated user's feelings of anxiety and reassured them of their preparation. Encouraged user to focus on their progress and resilience. Discussed the impact of past failure on current anxiety and suggested reflecting on improvements made since then. Offered support and encouraged further discussion.

# 📚 Conversation summary so far:
Summary 1:
User: Yağız
Assistant: Acknowledged user's name.
User: Feeling anxious about an upcoming exam.
Assistant: Validated user's feelings of anxiety and reassured them of their preparation. Encouraged user to focus on their progress and resilience. Discussed the impact of past failure on current anxiety.



# 💬 Ongoing session history (not yet summarized):



# 🗣️ User's latest message:
I dunno what to do...

#### Second Dialogue



