from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse, DocumentListResponse
from app.services.rag_service import get_documents, get_rag_answer

router = APIRouter(prefix="/api")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return await get_rag_answer(query=request.query, user_id=request.user_id)


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents() -> DocumentListResponse:
    documents = await get_documents()
    return DocumentListResponse(documents=documents)
