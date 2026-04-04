from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    user_id: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    user_id: str


class Document(BaseModel):
    id: str
    title: str
    content: str


class DocumentListResponse(BaseModel):
    documents: list[Document]


class HealthResponse(BaseModel):
    status: str
