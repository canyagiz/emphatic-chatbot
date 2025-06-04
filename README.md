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
* **Frontend:** Next.js (planned)
* **Deployment:** Docker (planned)
