"""
GitMuse - Local Model Provider
Uses local LLMs via Ollama for completely offline commit generation.
"""

from typing import Dict
from .factory import BaseAIProvider


class LocalProvider(BaseAIProvider):
    """Local model provider using Ollama."""
    
    def __init__(self, config):
        """Initialize local provider."""
        super().__init__(config)
        self.model = config.get('ai.model', 'codellama')
        self.base_url = config.get('ai.base_url', 'http://localhost:11434')
    
    async def generate_commit_message(self, analysis: Dict, temperature: float = 0.7) -> str:
        """Generate commit message using local Ollama model."""
        try:
            import aiohttp
        except ImportError:
            raise ImportError(
                "aiohttp package not installed. Install with: pip install aiohttp"
            )
        
        prompt = self._build_prompt(analysis)
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": 100
                        }
                    }
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Ollama API error: {response.status}")
                    
                    data = await response.json()
                    message = data.get('response', '').strip()
                    
                    # Clean up formatting
                    message = message.replace('`', '').replace('*', '')
                    
                    # Extract first line if multi-line response
                    if '\n' in message:
                        message = message.split('\n')[0]
                    
                    return message
                    
            except aiohttp.ClientError as e:
                raise Exception(
                    f"Could not connect to Ollama. Make sure Ollama is running: {str(e)}\n"
                    "Install from: https://ollama.ai"
                )
