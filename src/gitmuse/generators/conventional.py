"""
GitMuse - Conventional Commits Generator
Formats commit messages according to Conventional Commits specification.
"""

from typing import Dict


class ConventionalGenerator:
    """Generates commit messages following Conventional Commits format."""
    
    EMOJI_MAP = {
        'feat': '✨',
        'fix': '🐛',
        'docs': '📝',
        'style': '💄',
        'refactor': '♻️',
        'perf': '⚡',
        'test': '✅',
        'build': '🏗️',
        'ci': '👷',
        'chore': '🔧',
        'revert': '⏪'
    }
    
    def __init__(self, config):
        """Initialize the generator with configuration."""
        self.config = config
        self.use_emoji = config.get('emoji', False)
        self.max_length = config.get('maxLength', 72)
    
    def format(self, commit_type: str, scope: str, description: str, 
               body: str = '', footer: str = '', breaking: bool = False) -> str:
        """
        Format a commit message according to Conventional Commits.
        
        Args:
            commit_type: Type of change (feat, fix, docs, etc.)
            scope: Scope of change (optional)
            description: Brief description
            body: Detailed description (optional)
            footer: Footer with metadata (optional)
            breaking: Whether this is a breaking change
            
        Returns:
            Formatted commit message
        """
        # Build subject line
        subject = commit_type
        
        if scope:
            subject += f"({scope})"
        
        if breaking:
            subject += "!"
        
        subject += f": {description}"
        
        # Add emoji if enabled
        if self.use_emoji and commit_type in self.EMOJI_MAP:
            subject = f"{self.EMOJI_MAP[commit_type]} {subject}"
        
        # Truncate if too long
        if len(subject) > self.max_length:
            # Remove emoji if it doesn't fit
            if self.use_emoji:
                subject = subject.split(' ', 1)[1]
            subject = subject[:self.max_length - 3] + '...'
        
        # Build full message
        message = subject
        
        if body:
            message += f"\n\n{body}"
        
        if footer or breaking:
            message += "\n\n"
            if breaking:
                message += "BREAKING CHANGE: "
            if footer:
                message += footer
        
        return message
    
    def validate(self, message: str) -> tuple[bool, str]:
        """
        Validate a commit message.
        
        Args:
            message: Commit message to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not message:
            return False, "Commit message cannot be empty"
        
        lines = message.split('\n')
        subject = lines[0]
        
        # Check length
        if len(subject) > self.max_length:
            return False, f"Subject line too long ({len(subject)} > {self.max_length})"
        
        # Check format (basic validation)
        if ':' not in subject:
            return False, "Subject must contain ':' separator"
        
        # Extract type
        type_part = subject.split(':')[0]
        if self.use_emoji:
            type_part = type_part.split(' ', 1)[-1] if ' ' in type_part else type_part
        
        type_part = type_part.split('(')[0]
        
        valid_types = ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 
                       'test', 'build', 'ci', 'chore', 'revert']
        
        if type_part not in valid_types:
            return False, f"Unknown type: {type_part}"
        
        return True, ""
