from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
import pytest
import httpx

client = TestClient(app)


# tests/test_main.py
from unittest.mock import patch

def test_api_call():
    with patch("app.config.settings") as mock_settings:
        mock_settings.DEEPSEEK_API_KEY = "mock_test_key_123"  # 🔒 Fake key
        # Run your test...

@pytest.fixture
def mock_deepseek_response():
    return {
        "choices": [{
            "message": {
                "content": "Mocked DeepSeek response",
                "role": "assistant"
            }
        }]
    }


@pytest.mark.asyncio
async def test_generate_text_success(respx_mock, mock_deepseek_response):
    respx_mock.post(
        f"{settings.DEEPSEEK_BASE_URL}/chat/completions"
    ).mock(return_value=httpx.Response(200, json=mock_deepseek_response))

    response = client.post(
        "/generate",
        json={"prompt": "Hello DeepSeek", "max_tokens": 100}
    )

    assert response.status_code == 200
    assert response.json()["response"] == "Mocked DeepSeek response"


@pytest.mark.asyncio
async def test_generate_text_failure(respx_mock):
    respx_mock.post(
        f"{settings.DEEPSEEK_BASE_URL}/chat/completions"
    ).mock(return_value=httpx.Response(500, json={"error": "API error"}))

    response = client.post(
        "/generate",
        json={"prompt": "Hello DeepSeek"}
    )

    assert response.status_code == 500