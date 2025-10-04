from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from .config import OPENAI_API_KEY, MODEL
from .prompts import SYSTEM_PROMPT
from .tools import fetch_and_extract

class NandaAgent:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set")
        self.llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=MODEL, temperature=0.2)

    async def run(self, messages: List[Dict[str, Any]]) -> str:
        """
        messages: list of {"role": "user"|"assistant"|"system", "content": str}
        Optional convention: if last user message contains a URL, fetch it.
        """
        user_text = ""
        url = None
        for m in messages:
            if m.get("role") == "user":
                user_text = m.get("content", user_text)
        # naive URL sniff
        import re
        m = re.search(r'(https?://\S+)', user_text or "")
        if m:
            url = m.group(1)

        fetched = ""
        if url:
            fetched = await fetch_and_extract(url)

        prompt_blocks = [SystemMessage(content=SYSTEM_PROMPT)]
        if fetched:
            prompt_blocks.append(HumanMessage(content=f"Fetched content from {url}:\n{fetched}"))
        prompt_blocks.append(HumanMessage(content=user_text))

        resp = await self.llm.ainvoke(prompt_blocks)
        return resp.content
