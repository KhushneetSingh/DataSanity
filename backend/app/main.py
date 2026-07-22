from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload

app = FastAPI(title="DataSanity API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://datasanity.pages.dev", "https://*.pages.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/datasets")
def list_datasets():
    from app.database import get_supabase
    db = get_supabase()
    result = db.table("datasets").select("*").order("created_at", desc=True).limit(20).execute()
    return result.data
