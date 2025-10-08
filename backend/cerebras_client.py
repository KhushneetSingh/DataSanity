import httpx
import json
from typing import Optional, Dict, Any

class CerebrasClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "YOUR_CEREBRAS_API_KEY"
        self.base_url = "https://api.cerebras.ai/v1"
        self.model = "llama2-13b"
    
    def generate(self, prompt: str, max_tokens: int = 512) -> Dict[str, Any]:
        """
        Generate text using Cerebras API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens
        }
        
        try:
            # In a real implementation, we would call the Cerebras API
            # For this MVP, we'll return a simulated response
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30.0
            )
            
            # Simulate API response for MVP
            return {
                "success": True,
                "response": f"Simulated Cerebras API response for prompt: {prompt[:100]}...",
                "data": "Placeholder data based on the prompt"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }
    
    def set_model(self, model: str):
        """
        Set the model to use for generation.
        """
        self.model = model

# Global instance of the Cerebras client
cerebras_client = CerebrasClient()