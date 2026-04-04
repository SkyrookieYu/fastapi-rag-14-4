from app.models.schemas import ChatResponse, Document


async def get_rag_answer(query: str, user_id: str) -> ChatResponse:
    return ChatResponse(
        answer=f"這是針對「{query}」的模擬 RAG 回答。",
        sources=["docs/faq.md", "docs/manual.pdf"],
        user_id=user_id,
    )


async def get_documents() -> list[Document]:
    return [
        Document(id="1", title="常見問題集", content="這是 FAQ 文件的內容。"),
        Document(id="2", title="使用手冊", content="這是使用手冊的內容。"),
        Document(id="3", title="API 規格書", content="這是 API 規格書的內容。"),
    ]
