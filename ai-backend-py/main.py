from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chat

app = FastAPI()

# Geliştirme için CORS ayarları (frontend'den gelen istekleri kabul etmek için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production'da "*" yerine spesifik domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"status": "AI backend running"}
