import httpx
import json
import os
from typing import Optional, Dict, Any


class OpenRouterClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"
        # Free model available on OpenRouter (no credits required)
        self.model = "meta-llama/llama-3.2-3b-instruct:free"

    def generate(self, prompt: str, max_tokens: int = 512) -> Dict[str, Any]:
        """
        Generate text using OpenRouter's free API (OpenAI-compatible).
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://datasanity.app",  # Optional, for OpenRouter rankings
            "X-Title": "DataSanity",                   # Optional, shown in OpenRouter UI
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
        }

        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60.0,
            )
            response.raise_for_status()
            result = response.json()

            content = result["choices"][0]["message"]["content"]
            return {
                "success": True,
                "response": content,
                "data": content,
            }

        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}: {e.response.text}",
                "response": None,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None,
            }

    def set_model(self, model: str):
        """
        Set the model to use for generation.
        See https://openrouter.ai/models?q=free for free models.
        """
        self.model = model


# Global instance — reads OPENROUTER_API_KEY from environment
openrouter_client = OpenRouterClient()
