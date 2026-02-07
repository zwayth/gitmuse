"""
GitMuse - Git Diff Analyzer
Analyzes git diffs to extract meaningful information for commit message generation.
"""

import re
from typing import Dict, List, Set
from pathlib import Path


class GitAnalyzer:
    """Analyzes git diffs to understand code changes."""
    
    # Common file type categorizations
    CODE_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', 
                       '.go', '.rs', '.rb', '.php', '.swift', '.kt'}
    
    TEST_PATTERNS = ['test_', '_test.', 'spec.', '.test.', '.spec.']
    DOC_EXTENSIONS = {'.md', '.rst', '.txt', '.adoc'}
    CONFIG_FILES = {'package.json', 'requirements.txt', 'Cargo.toml', 'go.mod', 
                    'pom.xml', 'build.gradle', '.gitignore', 'Dockerfile'}
    
    # Commit type detection patterns
    TYPE_PATTERNS = {
        'feat': [
            r'add.*feature', r'implement', r'create.*new', r'introduce',
            r'class\s+\w+', r'function\s+\w+', r'def\s+\w+', r'const\s+\w+\s*='
        ],
        'fix': [
            r'fix', r'bug', r'issue', r'error', r'exception', r'resolve',
            r'patch', r'hotfix', r'correct'
        ],
        'docs': [
            r'document', r'readme', r'comment', r'javadoc', r'docstring',
            r'\.md', r'\.rst', r'changelog'
        ],
        'style': [
            r'format', r'whitespace', r'indent', r'lint', r'prettier',
            r'eslint', r'style', r'beautify'
        ],
        'refactor': [
            r'refactor', r'restructure', r'reorganize', r'cleanup',
            r'simplify', r'optimize', r'improve'
        ],
        'test': [
            r'test', r'spec', r'assertion', r'mock', r'stub',
            r'unittest', r'pytest', r'jest'
        ],
        'chore': [
            r'update.*dependenc', r'bump', r'version', r'package\.json',
            r'requirements\.txt', r'upgrade', r'maintain'
        ]
    }
    
    def __init__(self):
        """Initialize the analyzer."""
        self.compiled_patterns = {}
        for type_name, patterns in self.TYPE_PATTERNS.items():
            self.compiled_patterns[type_name] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    
    def analyze(self, diff: str) -> Dict:
        """
        Analyze a git diff and extract meaningful information.
        
        Args:
            diff: The git diff output as a string
            
        Returns:
            Dictionary containing analysis results
        """
        lines = diff.split('\n')
        
        # Extract basic statistics
        files_changed = self._extract_files(diff)
        lines_added, lines_removed = self._count_lines(lines)
        
        # Detect change type
        detected_type = self._detect_type(diff, files_changed)
        
        # Extract scope (affected component/module)
        scope = self._extract_scope(files_changed)
        
        # Detect breaking changes
        is_breaking = self._detect_breaking_changes(diff)
        
        # Extract code snippets for context
        snippets = self._extract_code_snippets(lines)
        
        # Categorize changes
        categories = self._categorize_changes(files_changed)
        
        return {
            'files_changed': len(files_changed),
            'files_list': list(files_changed),
            'lines_added': lines_added,
            'lines_removed': lines_removed,
            'detected_type': detected_type,
            'scope': scope,
            'is_breaking': is_breaking,
            'snippets': snippets,
            'categories': categories,
            'raw_diff': diff[:1000]  # First 1000 chars for AI context
        }
    
    def _extract_files(self, diff: str) -> Set[str]:
        """Extract list of changed files from diff."""
        files = set()
        for line in diff.split('\n'):
            if line.startswith('diff --git'):
                # Extract filename from "diff --git a/file b/file"
                parts = line.split()
                if len(parts) >= 4:
                    filename = parts[2][2:]  # Remove 'a/' prefix
                    files.add(filename)
        return files
    
    def _count_lines(self, lines: List[str]) -> tuple:
        """Count added and removed lines."""
        added = sum(1 for line in lines if line.startswith('+') and not line.startswith('+++'))
        removed = sum(1 for line in lines if line.startswith('-') and not line.startswith('---'))
        return added, removed
    
    def _detect_type(self, diff: str, files: Set[str]) -> str:
        """Detect the type of change (feat, fix, docs, etc.)."""
        
        # Check file extensions first
        if any(f.endswith(tuple(self.DOC_EXTENSIONS)) for f in files):
            return 'docs'
        
        if any(any(pattern in f for pattern in self.TEST_PATTERNS) for f in files):
            return 'test'
        
        if any(f in self.CONFIG_FILES for f in files):
            return 'chore'
        
        # Check diff content for patterns
        scores = {type_name: 0 for type_name in self.TYPE_PATTERNS.keys()}
        
        for type_name, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = len(pattern.findall(diff))
                scores[type_name] += matches
        
        # Return type with highest score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        # Default to chore if uncertain
        return 'chore'
    
    def _extract_scope(self, files: Set[str]) -> str:
        """Extract scope from file paths (e.g., 'api', 'ui', 'auth')."""
        if not files:
            return ''
        
        # Common scope patterns
        scopes = []
        
        for file in files:
            path = Path(file)
            parts = path.parts
            
            # Check for common scope indicators
            if 'src' in parts:
                idx = parts.index('src')
                if idx + 1 < len(parts):
                    scopes.append(parts[idx + 1])
            elif len(parts) > 1:
                scopes.append(parts[0])
        
        # Return most common scope
        if scopes:
            return max(set(scopes), key=scopes.count)
        
        return ''
    
    def _detect_breaking_changes(self, diff: str) -> bool:
        """Detect potential breaking changes."""
        breaking_indicators = [
            r'BREAKING CHANGE',
            r'remove.*function',
            r'delete.*class',
            r'deprecated',
            r'migration',
            r'API.*change'
        ]
        
        for pattern in breaking_indicators:
            if re.search(pattern, diff, re.IGNORECASE):
                return True
        
        return False
    
    def _extract_code_snippets(self, lines: List[str], max_snippets: int = 5) -> List[str]:
        """Extract meaningful code snippets from additions."""
        snippets = []
        current_snippet = []
        
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                # Clean the line
                clean_line = line[1:].strip()
                if clean_line and not clean_line.startswith('//') and not clean_line.startswith('#'):
                    current_snippet.append(clean_line)
            else:
                if current_snippet:
                    snippet = ' '.join(current_snippet)
                    if len(snippet) > 10:  # Only meaningful snippets
                        snippets.append(snippet[:100])  # Limit length
                    current_snippet = []
            
            if len(snippets) >= max_snippets:
                break
        
        return snippets
    
    def _categorize_changes(self, files: Set[str]) -> Dict[str, int]:
        """Categorize files by type."""
        categories = {
            'code': 0,
            'tests': 0,
            'docs': 0,
            'config': 0,
            'other': 0
        }
        
        for file in files:
            path = Path(file)
            
            if path.suffix in self.CODE_EXTENSIONS:
                if any(pattern in file for pattern in self.TEST_PATTERNS):
                    categories['tests'] += 1
                else:
                    categories['code'] += 1
            elif path.suffix in self.DOC_EXTENSIONS:
                categories['docs'] += 1
            elif path.name in self.CONFIG_FILES:
                categories['config'] += 1
            else:
                categories['other'] += 1
        
        return categories
    
    def generate_summary(self, analysis: Dict) -> str:
        """Generate a human-readable summary of the analysis."""
        summary_parts = []
        
        # File changes
        if analysis['files_changed'] == 1:
            summary_parts.append(f"Modified {analysis['files_list'][0]}")
        else:
            summary_parts.append(f"Modified {analysis['files_changed']} files")
        
        # Line changes
        if analysis['lines_added'] > 0 or analysis['lines_removed'] > 0:
            changes = []
            if analysis['lines_added'] > 0:
                changes.append(f"+{analysis['lines_added']}")
            if analysis['lines_removed'] > 0:
                changes.append(f"-{analysis['lines_removed']}")
            summary_parts.append(f"({', '.join(changes)} lines)")
        
        # Type and scope
        type_scope = analysis['detected_type']
        if analysis['scope']:
            type_scope += f"({analysis['scope']})"
        summary_parts.append(f"Type: {type_scope}")
        
        return " • ".join(summary_parts)
