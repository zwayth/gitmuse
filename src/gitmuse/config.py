"""
GitMuse - Configuration Manager
Handles loading and saving configuration from various sources.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional


class Config:
    """Configuration manager for GitMuse."""
    
    DEFAULT_CONFIG = {
        'style': 'conventional',
        'emoji': False,
        'maxLength': 72,
        'ai': {
            'provider': 'openai',
            'model': 'gpt-4',
            'temperature': 0.7
        },
        'scopes': [],
        'customRules': []
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Optional path to config file
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self.config_file = self._find_config_file(config_path)
        self._load()
    
    def _find_config_file(self, config_path: Optional[str] = None) -> Path:
        """Find configuration file in order of precedence."""
        if config_path:
            return Path(config_path)
        
        # Check current directory first
        local_config = Path('.gitmuserc')
        if local_config.exists():
            return local_config
        
        # Check home directory
        home_config = Path.home() / '.gitmuserc'
        if home_config.exists():
            return home_config
        
        # Return default location (may not exist yet)
        return local_config
    
    def _load(self) -> None:
        """Load configuration from file."""
        if not self.config_file.exists():
            return
        
        try:
            with open(self.config_file, 'r') as f:
                user_config = json.load(f)
                self._merge_config(user_config)
        except Exception as e:
            print(f"Warning: Could not load config from {self.config_file}: {e}")
    
    def _merge_config(self, user_config: dict) -> None:
        """Merge user configuration with defaults."""
        def merge_dict(base: dict, updates: dict) -> dict:
            """Recursively merge dictionaries."""
            result = base.copy()
            for key, value in updates.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dict(result[key], value)
                else:
                    result[key] = value
            return result
        
        self.config = merge_dict(self.config, user_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'ai.provider')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'ai.provider')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save()
    
    def _save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config to {self.config_file}: {e}")
    
    def get_all(self) -> dict:
        """Get all configuration as dictionary."""
        return self.config.copy()
