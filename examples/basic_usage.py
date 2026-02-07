#!/usr/bin/env python3
"""
Example: Basic GitMuse Usage
This example demonstrates how to use GitMuse programmatically.
"""

import asyncio
from gitmuse.analyzer import GitAnalyzer
from gitmuse.ai.factory import AIProviderFactory
from gitmuse.config import Config


async def main():
    """Example of using GitMuse programmatically."""
    
    # Initialize components
    config = Config()
    analyzer = GitAnalyzer()
    
    # Example git diff
    sample_diff = """diff --git a/src/api.py b/src/api.py
index 1234567..8901234 100644
--- a/src/api.py
+++ b/src/api.py
@@ -10,6 +10,13 @@ from flask import Flask, jsonify
 
 app = Flask(__name__)
 
+@app.route('/api/users', methods=['GET'])
+def get_users():
+    \"\"\"Get all users from database.\"\"\"
+    users = User.query.all()
+    return jsonify([user.to_dict() for user in users])
+
+
 @app.route('/api/health', methods=['GET'])
 def health_check():
     return jsonify({'status': 'healthy'})
"""
    
    # Analyze the diff
    print("📊 Analyzing code changes...")
    analysis = analyzer.analyze(sample_diff)
    
    print(f"Files changed: {analysis['files_changed']}")
    print(f"Lines added: +{analysis['lines_added']}")
    print(f"Lines removed: -{analysis['lines_removed']}")
    print(f"Detected type: {analysis['detected_type']}")
    print(f"Scope: {analysis.get('scope', 'N/A')}")
    print()
    
    # Generate commit message (requires API key)
    try:
        print("🤖 Generating commit message with AI...")
        ai_provider = AIProviderFactory.create(config)
        message = await ai_provider.generate_commit_message(analysis)
        
        print(f"✨ Suggested commit message:")
        print(f"   {message}")
        
    except Exception as e:
        print(f"⚠️  Could not generate AI message: {e}")
        print("   Make sure you have configured an API key!")
        print()
        
        # Fallback: manual message construction
        print("📝 Manual message construction:")
        commit_type = analysis['detected_type']
        scope = analysis.get('scope', '')
        
        if scope:
            manual_message = f"{commit_type}({scope}): add user listing endpoint"
        else:
            manual_message = f"{commit_type}: add user listing endpoint"
        
        print(f"   {manual_message}")


if __name__ == '__main__':
    asyncio.run(main())
