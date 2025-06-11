import httpx
import asyncio
from app.config import settings

async def test_call():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY.get_secret_value()}"},
            json={
                "model": settings.DEEPSEEK_MODEL,
                "messages": [{"role": "user", "content": "Hello, DeepSeek!"}],
            },
        )
        print(response.status_code)
        print(response.json())

asyncio.run(test_call())