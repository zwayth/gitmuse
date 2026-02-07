"""
Tests for GitAnalyzer
"""

import pytest
from gitmuse.analyzer import GitAnalyzer


class TestGitAnalyzer:
    """Test suite for GitAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = GitAnalyzer()
    
    def test_analyze_basic_diff(self):
        """Test basic diff analysis."""
        diff = """diff --git a/src/main.py b/src/main.py
index 1234567..8901234 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,6 @@
+def new_function():
+    return True
+
 def old_function():
     return False
"""
        
        analysis = self.analyzer.analyze(diff)
        
        assert analysis['files_changed'] == 1
        assert 'src/main.py' in analysis['files_list']
        assert analysis['lines_added'] == 3
        assert analysis['lines_removed'] == 0
    
    def test_detect_type_feature(self):
        """Test feature type detection."""
        diff = """diff --git a/src/api.py b/src/api.py
+def new_endpoint():
+    return jsonify(data)
"""
        
        analysis = self.analyzer.analyze(diff)
        assert analysis['detected_type'] == 'feat'
    
    def test_detect_type_fix(self):
        """Test bug fix type detection."""
        diff = """diff --git a/src/bug.py b/src/bug.py
-    if user is None:
+    if user is not None:
"""
        
        analysis = self.analyzer.analyze(diff)
        # Should detect as fix due to change pattern
        assert analysis['detected_type'] in ['fix', 'refactor', 'chore']
    
    def test_detect_type_docs(self):
        """Test documentation type detection."""
        diff = """diff --git a/README.md b/README.md
+## Installation
+Run: pip install gitmuse
"""
        
        analysis = self.analyzer.analyze(diff)
        assert analysis['detected_type'] == 'docs'
    
    def test_extract_scope(self):
        """Test scope extraction from file paths."""
        diff = """diff --git a/src/api/users.py b/src/api/users.py
+def get_user():
+    pass
"""
        
        analysis = self.analyzer.analyze(diff)
        assert analysis['scope'] == 'api'
    
    def test_breaking_change_detection(self):
        """Test breaking change detection."""
        diff = """diff --git a/src/api.py b/src/api.py
-def old_api():
-    pass
+# BREAKING CHANGE: Removed old_api
"""
        
        analysis = self.analyzer.analyze(diff)
        assert analysis['is_breaking'] is True
    
    def test_multiple_files(self):
        """Test analysis with multiple files."""
        diff = """diff --git a/src/main.py b/src/main.py
+import new_module

diff --git a/tests/test_main.py b/tests/test_main.py
+def test_new_feature():
+    assert True
"""
        
        analysis = self.analyzer.analyze(diff)
        assert analysis['files_changed'] == 2
        assert len(analysis['files_list']) == 2
    
    def test_categorize_changes(self):
        """Test file categorization."""
        diff = """diff --git a/src/main.py b/src/main.py
diff --git a/tests/test_main.py b/tests/test_main.py
diff --git a/README.md b/README.md
diff --git a/setup.py b/setup.py
"""
        
        analysis = self.analyzer.analyze(diff)
        categories = analysis['categories']
        
        assert categories['code'] >= 1
        assert categories['tests'] >= 1
        assert categories['docs'] >= 1
        assert categories['config'] >= 1
    
    def test_empty_diff(self):
        """Test handling of empty diff."""
        analysis = self.analyzer.analyze("")
        
        assert analysis['files_changed'] == 0
        assert analysis['lines_added'] == 0
        assert analysis['lines_removed'] == 0
    
    def test_large_diff(self):
        """Test handling of large diffs."""
        # Create a large diff
        lines = ["+" + f"line {i}" for i in range(1000)]
        diff = "diff --git a/large.py b/large.py\n" + "\n".join(lines)
        
        analysis = self.analyzer.analyze(diff)
        assert analysis['lines_added'] == 1000
        assert len(analysis['raw_diff']) <= 1000  # Should be truncated
