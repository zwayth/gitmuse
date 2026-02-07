"""
GitMuse - AI Provider Factory
Creates appropriate AI provider based on configuration.
"""

from typing import Dict
from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """Base class for AI providers."""
    
    def __init__(self, config):
        """Initialize the AI provider with configuration."""
        self.config = config
    
    @abstractmethod
    async def generate_commit_message(self, analysis: Dict, temperature: float = 0.7) -> str:
        """
        Generate a commit message based on code analysis.
        
        Args:
            analysis: Dictionary containing code change analysis
            temperature: Creativity temperature (0.0-1.0)
            
        Returns:
            Generated commit message string
        """
        pass
    
    def _build_prompt(self, analysis: Dict) -> str:
        """Build the prompt for the AI model."""
        
        # Determine style
        style = self.config.get('style', 'conventional')
        use_emoji = self.config.get('emoji', False)
        
        prompt = f"""You are an expert at writing git commit messages.

Analyze the following code changes and generate a single, concise commit message.

CODE ANALYSIS:
- Files changed: {analysis['files_changed']}
- Type detected: {analysis['detected_type']}
- Scope: {analysis.get('scope', 'N/A')}
- Lines added: {analysis['lines_added']}
- Lines removed: {analysis['lines_removed']}
- Breaking change: {analysis.get('is_breaking', False)}

FILES:
{chr(10).join('- ' + f for f in analysis['files_list'][:5])}

DIFF PREVIEW:
{analysis['raw_diff']}

"""
        
        if style == 'conventional':
            prompt += """
REQUIREMENTS:
1. Follow Conventional Commits format: type(scope): description
2. Types: feat, fix, docs, style, refactor, test, chore
3. Keep subject line under 72 characters
4. Use imperative mood (e.g., "add" not "added")
5. Don't capitalize first letter after colon
6. No period at the end
"""
        
        if use_emoji:
            prompt += """
7. Add appropriate emoji prefix:
   - ✨ for feat
   - 🐛 for fix
   - 📝 for docs
   - 💄 for style
   - ♻️ for refactor
   - ✅ for test
   - 🔧 for chore
"""
        
        prompt += """
Generate only the commit message, nothing else. Be specific and descriptive.
"""
        
        return prompt


class AIProviderFactory:
    """Factory for creating AI provider instances."""
    
    @staticmethod
    def create(config) -> BaseAIProvider:
        """
        Create an AI provider based on configuration.
        
        Args:
            config: Configuration object
            
        Returns:
            Instance of appropriate AI provider
        """
        provider_name = config.get('ai.provider', 'openai')
        
        if provider_name == 'openai':
            from .openai import OpenAIProvider
            return OpenAIProvider(config)
        elif provider_name == 'claude':
            from .claude import ClaudeProvider
            return ClaudeProvider(config)
        elif provider_name == 'local':
            from .local import LocalProvider
            return LocalProvider(config)
        else:
            raise ValueError(f"Unknown AI provider: {provider_name}")
