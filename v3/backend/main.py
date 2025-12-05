from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS is already set, but keep this pattern if you edit:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or lock to your Netlify domains later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"ok": True, "service": "cratejuice-backend", "routes": ["/health"]}

@app.get("/health")
def health():
    return {"ok": True}
