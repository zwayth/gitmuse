#!/usr/bin/env python3
"""
GitMuse - AI-Powered Commit Message Generator
Main CLI interface
"""

import click
import subprocess
import sys
from typing import List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from .analyzer import GitAnalyzer
from .ai.factory import AIProviderFactory
from .generators.conventional import ConventionalGenerator
from .config import Config

console = Console()


class GitMuse:
    """Main GitMuse application class."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize GitMuse with configuration."""
        self.config = Config(config_path)
        self.analyzer = GitAnalyzer()
        self.ai_provider = AIProviderFactory.create(self.config)
        self.generator = ConventionalGenerator(self.config)
    
    def get_staged_changes(self) -> str:
        """Get the diff of staged changes."""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            console.print("[red]Error: Not a git repository or no staged changes[/red]")
            sys.exit(1)
    
    def analyze_changes(self, diff: str) -> dict:
        """Analyze the git diff and extract meaningful information."""
        return self.analyzer.analyze(diff)
    
    async def generate_suggestions(self, analysis: dict, count: int = 3) -> List[str]:
        """Generate commit message suggestions using AI."""
        suggestions = []
        
        with console.status("[cyan]Analyzing your changes with AI..."):
            for i in range(count):
                message = await self.ai_provider.generate_commit_message(
                    analysis,
                    temperature=0.7 + (i * 0.1)  # Vary temperature for diversity
                )
                suggestions.append(message)
        
        return suggestions
    
    def display_suggestions(self, suggestions: List[str]) -> None:
        """Display commit message suggestions in a nice format."""
        table = Table(title="💡 Suggested Commit Messages", show_header=True)
        table.add_column("#", style="cyan", width=3)
        table.add_column("Message", style="green")
        
        for i, suggestion in enumerate(suggestions, 1):
            table.add_row(str(i), suggestion)
        
        console.print(table)
    
    def commit_with_message(self, message: str) -> bool:
        """Execute git commit with the chosen message."""
        try:
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                capture_output=True,
                text=True,
                check=True
            )
            console.print(f"[green]✓ Committed successfully![/green]")
            console.print(f"[dim]{result.stdout}[/dim]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error committing: {e.stderr}[/red]")
            return False


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    🎨 GitMuse - AI-Powered Commit Message Generator
    
    Never write boring commit messages again!
    """
    pass


@cli.command()
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode with choices')
@click.option('--count', '-c', default=3, help='Number of suggestions to generate')
@click.option('--auto', '-a', is_flag=True, help='Auto-commit with first suggestion')
def commit(interactive: bool, count: int, auto: bool):
    """Generate AI-powered commit message and commit changes."""
    
    console.print(Panel.fit(
        "[bold cyan]🎨 GitMuse[/bold cyan]\n[dim]AI-Powered Commit Generator[/dim]",
        border_style="cyan"
    ))
    
    # Initialize GitMuse
    gitmuse = GitMuse()
    
    # Get staged changes
    diff = gitmuse.get_staged_changes()
    
    if not diff.strip():
        console.print("[yellow]⚠ No staged changes found. Stage your changes first with 'git add'[/yellow]")
        sys.exit(1)
    
    # Analyze changes
    with console.status("[cyan]Analyzing changes..."):
        analysis = gitmuse.analyze_changes(diff)
    
    # Show analysis summary
    console.print(f"\n[cyan]📊 Analysis:[/cyan]")
    console.print(f"  Files changed: [green]{analysis['files_changed']}[/green]")
    console.print(f"  Lines added: [green]+{analysis['lines_added']}[/green]")
    console.print(f"  Lines removed: [red]-{analysis['lines_removed']}[/red]")
    console.print(f"  Detected type: [yellow]{analysis['detected_type']}[/yellow]")
    if analysis.get('scope'):
        console.print(f"  Scope: [blue]{analysis['scope']}[/blue]")
    console.print()
    
    # Generate suggestions
    import asyncio
    suggestions = asyncio.run(gitmuse.generate_suggestions(analysis, count))
    
    if auto:
        # Auto-commit with first suggestion
        console.print(f"[cyan]Using: {suggestions[0]}[/cyan]")
        gitmuse.commit_with_message(suggestions[0])
        return
    
    # Display suggestions
    gitmuse.display_suggestions(suggestions)
    
    if interactive:
        # Interactive selection
        choice = Prompt.ask(
            "\n[cyan]Choose a message[/cyan]",
            choices=[str(i) for i in range(1, len(suggestions) + 1)] + ['c', 'e'],
            default="1"
        )
        
        if choice == 'c':
            console.print("[yellow]Cancelled[/yellow]")
            sys.exit(0)
        elif choice == 'e':
            # Allow editing
            selected = suggestions[0]
            edited = Prompt.ask(
                "[cyan]Edit message[/cyan]",
                default=selected
            )
            gitmuse.commit_with_message(edited)
        else:
            # Use selected message
            selected_msg = suggestions[int(choice) - 1]
            
            if Confirm.ask(f"[cyan]Commit with this message?[/cyan]"):
                gitmuse.commit_with_message(selected_msg)
            else:
                console.print("[yellow]Cancelled[/yellow]")
    else:
        # Non-interactive: just show suggestions
        console.print("\n[dim]Run with --interactive to choose and commit[/dim]")


@cli.command()
@click.option('--count', '-c', default=3, help='Number of suggestions')
def suggest(count: int):
    """Generate commit message suggestions without committing."""
    
    gitmuse = GitMuse()
    diff = gitmuse.get_staged_changes()
    
    if not diff.strip():
        console.print("[yellow]No staged changes found[/yellow]")
        sys.exit(1)
    
    analysis = gitmuse.analyze_changes(diff)
    
    import asyncio
    suggestions = asyncio.run(gitmuse.generate_suggestions(analysis, count))
    
    gitmuse.display_suggestions(suggestions)
    
    console.print("\n[dim]Copy one of these messages for your commit![/dim]")


@cli.command()
@click.option('--style', type=click.Choice(['conventional', 'simple', 'emoji']), 
              help='Commit message style')
@click.option('--provider', help='AI provider (openai, claude, local)')
@click.option('--model', help='AI model to use')
@click.option('--emoji/--no-emoji', default=None, help='Enable/disable emoji')
def config(style: Optional[str], provider: Optional[str], 
           model: Optional[str], emoji: Optional[bool]):
    """Configure GitMuse settings."""
    
    cfg = Config()
    
    if style:
        cfg.set('style', style)
        console.print(f"[green]✓ Style set to: {style}[/green]")
    
    if provider:
        cfg.set('ai.provider', provider)
        console.print(f"[green]✓ Provider set to: {provider}[/green]")
    
    if model:
        cfg.set('ai.model', model)
        console.print(f"[green]✓ Model set to: {model}[/green]")
    
    if emoji is not None:
        cfg.set('emoji', emoji)
        console.print(f"[green]✓ Emoji {'enabled' if emoji else 'disabled'}[/green]")
    
    if not any([style, provider, model, emoji is not None]):
        # Show current config
        console.print(Panel.fit(
            f"[bold]Current Configuration[/bold]\n\n"
            f"Style: [cyan]{cfg.get('style', 'conventional')}[/cyan]\n"
            f"Emoji: [cyan]{cfg.get('emoji', False)}[/cyan]\n"
            f"Provider: [cyan]{cfg.get('ai.provider', 'openai')}[/cyan]\n"
            f"Model: [cyan]{cfg.get('ai.model', 'gpt-4')}[/cyan]",
            border_style="cyan"
        ))


@cli.command()
@click.option('--days', '-d', default=30, help='Number of days to analyze')
def stats(days: int):
    """Show your commit statistics."""
    
    try:
        # Get commit history
        result = subprocess.run(
            ['git', 'log', f'--since={days} days ago', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )
        
        commits = result.stdout.strip().split('\n')
        
        if not commits or commits == ['']:
            console.print(f"[yellow]No commits found in the last {days} days[/yellow]")
            return
        
        # Analyze commits
        total = len(commits)
        types = {}
        
        for commit in commits:
            # Extract type from conventional commit
            if ':' in commit:
                commit_type = commit.split(':')[0].split('(')[0].strip()
                types[commit_type] = types.get(commit_type, 0) + 1
        
        # Display stats
        console.print(Panel.fit(
            f"[bold cyan]📈 Your Commit Statistics[/bold cyan]\n[dim]Last {days} days[/dim]",
            border_style="cyan"
        ))
        
        console.print(f"\n[cyan]Total commits:[/cyan] [bold]{total}[/bold]")
        
        if types:
            console.print(f"\n[cyan]Commit types:[/cyan]")
            for commit_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total) * 100
                console.print(f"  {commit_type}: {count} ([green]{percentage:.1f}%[/green])")
        
        avg_length = sum(len(c) for c in commits) / len(commits)
        console.print(f"\n[cyan]Average message length:[/cyan] {avg_length:.0f} characters")
        
    except subprocess.CalledProcessError:
        console.print("[red]Error: Not a git repository[/red]")
        sys.exit(1)


@cli.command()
def init():
    """Initialize GitMuse in current repository."""
    
    console.print("[cyan]🎨 Initializing GitMuse...[/cyan]\n")
    
    # Check if in git repo
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        console.print("[red]Error: Not a git repository[/red]")
        console.print("[dim]Run 'git init' first[/dim]")
        sys.exit(1)
    
    # Create config file
    config = Config()
    
    style = Prompt.ask(
        "[cyan]Choose commit style[/cyan]",
        choices=['conventional', 'simple', 'emoji'],
        default='conventional'
    )
    
    provider = Prompt.ask(
        "[cyan]Choose AI provider[/cyan]",
        choices=['openai', 'claude', 'local'],
        default='openai'
    )
    
    use_emoji = Confirm.ask("[cyan]Use emoji in commits?[/cyan]", default=False)
    
    config.set('style', style)
    config.set('ai.provider', provider)
    config.set('emoji', use_emoji)
    
    console.print("\n[green]✓ GitMuse initialized successfully![/green]")
    console.print("[dim]Configuration saved to .gitmuserc[/dim]")
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print("  1. Set up your AI provider API key")
    console.print("  2. Stage some changes: git add .")
    console.print("  3. Run: gitmuse commit --interactive")


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
