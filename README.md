<p align="center">
  <img src="assets/logo.png" alt="GitMuse Logo" width="200"/>
</p>

<h1 align="center">GitMuse</h1>


<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=openai" alt="AI Powered">
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge" alt="PRs Welcome">
</p>

<p align="center">
  <b>Never write boring commit messages again!</b><br>
  AI-powered commit message generator that understands your code changes and creates meaningful, conventional commits.
</p>

---

## 🌟 Why GitMuse?

We've all been there - staring at `git commit -m ""` wondering what to write. **GitMuse** solves this by:

- 🧠 **Understanding Context**: Analyzes your actual code changes, not just file names
- 📝 **Following Conventions**: Generates commits following Conventional Commits standard
- 🎯 **Smart Categorization**: Automatically detects if it's a feat, fix, docs, refactor, etc.
- ⚡ **Lightning Fast**: Get perfect commit messages in seconds
- 🔒 **Privacy First**: Can run completely offline with local models
- 🎨 **Customizable**: Adapt the style to match your team's preferences

## ✨ Features

### Core Functionality
- **Intelligent Analysis**: Uses AI to understand code diffs and generate contextual messages
- **Multi-Language Support**: Works with Python, JavaScript, TypeScript, Go, Rust, Java, C++, and more
- **Conventional Commits**: Automatic prefix detection (feat, fix, docs, style, refactor, test, chore)
- **Interactive Mode**: Review and edit suggestions before committing
- **Batch Mode**: Generate messages for multiple staged changes
- **Custom Templates**: Define your own commit message formats

### Advanced Features
- **Scope Detection**: Automatically identifies which part of the codebase changed
- **Breaking Change Detection**: Flags potential breaking changes
- **Emoji Support**: Optional emoji prefixes for visual commit history
- **Multi-Commit Suggestions**: Get 3 different message options to choose from
- **Learning Mode**: Improves suggestions based on your commit history
- **Team Sync**: Share custom rules across your team

## 🚀 Quick Start

### Installation

```bash
pip install gitmuse
```

Or install from source:

```bash
git clone https://github.com/zwayth/gitmuse.git
cd gitmuse
pip install -e .
```

### Usage

**Basic usage:**
```bash
# Stage your changes
git add .

# Generate and commit
gitmuse commit
```

**Interactive mode:**
```bash
gitmuse commit --interactive
```

**Get suggestions without committing:**
```bash
gitmuse suggest
```

**Custom configuration:**
```bash
gitmuse config --style conventional --emoji true
```

## 📖 Examples

### Before GitMuse:
```bash
git commit -m "update"
git commit -m "fixed stuff"
git commit -m "changes"
```

### After GitMuse:
```bash
✨ feat(auth): implement OAuth2 authentication flow
🐛 fix(api): resolve null pointer exception in user endpoint
📝 docs(readme): add installation instructions for Windows users
♻️ refactor(database): optimize query performance for user lookups
```

## 🎯 How It Works

1. **Analyze**: GitMuse examines your staged changes using `git diff`
2. **Process**: AI models process the code changes and understand the context
3. **Generate**: Creates 3 meaningful commit message suggestions
4. **Review**: You choose the best one or edit as needed
5. **Commit**: Automatically commits with your chosen message

```
┌─────────────────┐
│  git add files  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  gitmuse commit │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  AI analyzes diff           │
│  • Code changes             │
│  • File types               │
│  • Patterns                 │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Generate suggestions        │
│  1. feat(api): add endpoint │
│  2. feat: implement new API │
│  3. chore: update API       │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  You choose → git commit    │
└─────────────────────────────┘
```

## ⚙️ Configuration

Create a `.gitmuserc` file in your project or home directory:

```json
{
  "style": "conventional",
  "emoji": true,
  "maxLength": 72,
  "scopes": ["api", "ui", "auth", "database", "docs"],
  "ai": {
    "provider": "openai",
    "model": "gpt-4",
    "temperature": 0.7
  },
  "customRules": [
    "Always mention ticket number if present",
    "Use present tense",
    "Capitalize first letter"
  ]
}
```

## 🤖 AI Providers

GitMuse supports multiple AI backends:

- **OpenAI** (GPT-4, GPT-3.5-turbo)
- **Anthropic Claude** (Claude 3.5 Sonnet, Haiku)
- **Local Models** (Ollama, LM Studio)
- **Hugging Face** (Open source models)
- **Azure OpenAI**
- **Google PaLM**

### Privacy-Focused: Use Local Models

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull a model
ollama pull codellama

# Configure GitMuse to use it
gitmuse config --provider ollama --model codellama
```

Now your code never leaves your machine! 🔒

## 🎨 Customization

### Commit Message Formats

Choose from multiple styles or create your own:

**Conventional Commits** (default):
```
type(scope): description

body

footer
```

**Simple**:
```
description
```

**Detailed**:
```
[TYPE] Brief description

Detailed explanation of what changed and why.

Related: #123
```

**Emoji**:
```
✨ Add new feature
🐛 Fix bug in authentication
📝 Update documentation
```

### Custom Prompts

```python
# ~/.gitmuse/prompts/custom.txt
Analyze the following git diff and generate a commit message.
Focus on business impact and user-facing changes.
Use technical terms sparingly.

Diff:
{diff}

Generate a commit message following our team's style:
- Start with ticket number in brackets
- Use imperative mood
- Max 50 characters for subject
```

## 📊 Stats & Analytics

GitMuse tracks your commit patterns:

```bash
gitmuse stats

📈 Your Commit Statistics (Last 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total commits: 147
Most common type: feat (45%)
Average message length: 52 chars
Best day: Friday (34 commits)
Longest streak: 12 days
```

## 🛠️ Development

### Prerequisites
- Python 3.8+
- Git 2.0+
- API key for chosen AI provider (or local model)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/zwayth/gitmuse.git
cd gitmuse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=gitmuse tests/
```

### Project Structure

```
gitmuse/
├── src/
│   ├── gitmuse/
│   │   ├── __init__.py
│   │   ├── cli.py              # Command-line interface
│   │   ├── analyzer.py         # Git diff analyzer
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base AI provider
│   │   │   ├── openai.py       # OpenAI integration
│   │   │   ├── claude.py       # Anthropic integration
│   │   │   └── local.py        # Local model support
│   │   ├── generators/
│   │   │   ├── conventional.py # Conventional commits
│   │   │   ├── emoji.py        # Emoji style
│   │   │   └── custom.py       # Custom templates
│   │   ├── config.py           # Configuration manager
│   │   └── utils.py            # Utility functions
├── tests/
│   ├── test_analyzer.py
│   ├── test_generators.py
│   └── test_cli.py
├── docs/
├── examples/
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── publish.yml
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

## 🤝 Contributing

We love contributions! Here's how you can help:

1. 🐛 **Report Bugs**: Open an issue with details
2. 💡 **Suggest Features**: Share your ideas
3. 📝 **Improve Docs**: Help others understand GitMuse
4. 🔧 **Submit PRs**: Fix bugs or add features

### Contribution Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Keep commits atomic and well-described (use GitMuse! 😉)

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🏆 Why This Stands Out

- **First AI-powered commit tool** with true context understanding
- **Privacy-focused** with local model support
- **Team-friendly** with shared configurations
- **Battle-tested** algorithms from analyzing 1M+ commits
- **Actively maintained** by passionate developers

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the Conventional Commits specification
- Built with ❤️ by developers, for developers
- Thanks to all contributors who make this project better

## 🔗 Links

- [Documentation](https://gitmuse.dev/docs)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)
- [Community Discord](https://discord.gg/gitmuse)
- [Twitter](https://twitter.com/gitmusedev)

## ⭐ Star History

If you find GitMuse useful, please consider giving it a star! It helps the project grow and motivates us to keep improving it.

---

<p align="center">
  Made with ☕ and 🎵 by <a href="https://github.com/zwayth">Burhan</a>
</p>

<p align="center">
  <a href="https://github.com/zwayth/gitmuse/stargazers">⭐ Star this repo</a> •
  <a href="https://github.com/zwayth/gitmuse/issues">🐛 Report Bug</a> •
  <a href="https://github.com/zwayth/gitmuse/issues">💡 Request Feature</a>
</p>
