from fastapi import APIRouter
from ..models.schemas import ChatRequest, ChatResponse
from ..core.rag_pipeline import run_rag_stream
from fastapi.responses import StreamingResponse


router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_stream(request: ChatRequest):
    """
    Main RAG chat endpoint
    Accepts a question from the user and returns a context-aware answer
    """
    async def event_generator():
        async for chunk in run_rag_stream(request.question):
            yield chunk
    return StreamingResponse(event_generator(), media_type="text/plain")