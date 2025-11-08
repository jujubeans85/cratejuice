from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
def home():
    return {"crate": "juice", "status": "spinning"}

@app.get("/health")
def health():
    return {"ok": True}
