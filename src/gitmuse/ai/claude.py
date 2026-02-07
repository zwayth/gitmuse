"""
GitMuse - Claude Provider
Integrates with Anthropic's Claude for commit message generation.
"""

import os
from typing import Dict
from .factory import BaseAIProvider


class ClaudeProvider(BaseAIProvider):
    """Anthropic Claude-based commit message generator."""
    
    def __init__(self, config):
        """Initialize Claude provider."""
        super().__init__(config)
        self.api_key = os.getenv('ANTHROPIC_API_KEY') or config.get('ai.api_key')
        self.model = config.get('ai.model', 'claude-3-5-sonnet-20241022')
        
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable "
                "or configure it in .gitmuserc"
            )
    
    async def generate_commit_message(self, analysis: Dict, temperature: float = 0.7) -> str:
        """Generate commit message using Claude API."""
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )
        
        client = anthropic.AsyncAnthropic(api_key=self.api_key)
        
        prompt = self._build_prompt(analysis)
        
        try:
            message = await client.messages.create(
                model=self.model,
                max_tokens=100,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            commit_msg = message.content[0].text.strip()
            
            # Clean up formatting
            commit_msg = commit_msg.replace('`', '').replace('*', '')
            
            return commit_msg
            
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
