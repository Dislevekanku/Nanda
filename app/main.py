from fastapi import FastAPI, Body, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .agent import NandaAgent
from .config import HOST, PORT, NANDA_SHARED_SECRET

app = FastAPI(title="NANDA Adapter Wrapped Agent")
agent = NandaAgent()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.get("/")
async def root():
    return {
        "message": "Trust-First Agentic Web Explainer",
        "description": "A LangChain-powered agent specializing in MCP, A2A, and agent interoperability",
        "endpoints": {
            "health": "/health",
            "chat": "/chat"
        },
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

# If the adapter expects /chat or /invoke, mirror that route:
@app.post("/chat")
async def chat(req: ChatRequest, x_nanda_secret: Optional[str] = Header(default=None)):
    # Optional shared secret check (if adapter enforces)
    # Disabled for local testing - uncomment for production
    # if NANDA_SHARED_SECRET and NANDA_SHARED_SECRET != "changeme" and x_nanda_secret != NANDA_SHARED_SECRET:
    #     return JSONResponse(status_code=401, content={"error": "unauthorized"})
    messages = [m.model_dump() for m in req.messages]
    answer = await agent.run(messages)
    # Return shape the adapter expects, commonly: {"reply": "..."} or {"content": "..."}
    return {"reply": answer}
