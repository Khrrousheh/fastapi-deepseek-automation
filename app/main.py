from fastapi import FastAPI, HTTPException
from app.config import settings
import httpx
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/generate")
async def generate_text(prompt: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY.get_secret_value()}",  # Access secret
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.DEEPSEEK_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30.0,
            )
            response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx
            return response.json()

    except httpx.HTTPStatusError as e:
        logger.error(f"DeepSeek API error: {e.response.text}")
        raise HTTPException(status_code=502, detail="API request failed")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")