from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from app.config import settings

app = FastAPI()

class PromptInput(BaseModel):
    prompt: str
    max_tokens: int = 100


@app.post("/generate")
async def generate_text(data: PromptInput):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": settings.DEEPSEEK_MODEL,
                    "messages": [{"role": "user", "content": data.prompt}],
                    "max_tokens": data.max_tokens
                },
                timeout=30.0
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text
                )

            result = response.json()
            return {"response": result['choices'][0]['message']['content'].strip()}

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))