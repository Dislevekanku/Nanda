import httpx
from bs4 import BeautifulSoup

async def fetch_and_extract(url: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, follow_redirects=True)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            # Simple readability: get visible text
            texts = [t.strip() for t in soup.stripped_strings]
            return " ".join(texts)[:15000]  # cap to avoid huge prompts
    except Exception as e:
        return f"[fetch_error] {e}"
