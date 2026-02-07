"""
GitMuse - OpenAI Provider
Integrates with OpenAI's GPT models for commit message generation.
"""

import os
from typing import Dict
from .factory import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    """OpenAI GPT-based commit message generator."""
    
    def __init__(self, config):
        """Initialize OpenAI provider."""
        super().__init__(config)
        self.api_key = os.getenv('OPENAI_API_KEY') or config.get('ai.api_key')
        self.model = config.get('ai.model', 'gpt-4')
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or configure it in .gitmuserc"
            )
    
    async def generate_commit_message(self, analysis: Dict, temperature: float = 0.7) -> str:
        """Generate commit message using OpenAI API."""
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )
        
        client = openai.AsyncOpenAI(api_key=self.api_key)
        
        prompt = self._build_prompt(analysis)
        
        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at writing concise, meaningful git commit messages."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=100
            )
            
            message = response.choices[0].message.content.strip()
            
            # Clean up any markdown formatting
            message = message.replace('`', '').replace('*', '')
            
            return message
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
