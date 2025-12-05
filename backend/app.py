from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import ingestion_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(ingestion_router.router, prefix="/admin", tags=["upload"])

@app.get("/health")
def check_health():
    return {"status": "ok"}

