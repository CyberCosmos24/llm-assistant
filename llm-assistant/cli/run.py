"""Command-line interface for the cybersecurity assistant."""
from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from analysis.analyzer import analyze_multiple_events, analyze_single_event
from logs.ingest import load_json_logs, load_text_logs
from llm.client import chat, DEFAULT_MODEL

app = typer.Typer(help="Local AI-powered cybersecurity assistant")
console = Console()


@app.command()
def analyze(path: str) -> None:
    """Analyze a log file (JSON or plain text)."""

    if path.endswith(".json"):
        events = load_json_logs(path)
    else:
        lines = load_text_logs(path)
        events = [{"message": line} for line in lines]

    if not events:
        console.print(f"[red]No log events could be loaded from {path}.[/red]")
        raise typer.Exit(code=1)

    if len(events) == 1:
        result = analyze_single_event(events[0])
        console.print(Panel(str(result["explanation"]), title="Explanation", expand=False))
        console.print(f"Severity: [bold]{result['severity'].value}[/bold]")
    else:
        result = analyze_multiple_events(events)
        console.print(Panel(str(result["summary"]), title="Summary", expand=False))
        table = Table(title="Top Events", show_header=True, header_style="bold magenta")
        table.add_column("Index", justify="right")
        table.add_column("Event")
        for idx, event in enumerate(result.get("top_events", []), start=1):
            table.add_row(str(idx), str(event))
        console.print(table)
        console.print(f"Severity: [bold]{result['severity'].value}[/bold]")


@app.command(name="chat")
def chat_command() -> None:
    """Start an interactive chat session with the local model."""

    console.print(f"Connecting to model [green]{DEFAULT_MODEL}[/green]. Type :q or quit to exit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {":q", "quit"}:
            console.print("Exiting chat.")
            break
        if not user_input:
            continue
        reply = chat(user_input)
        console.print(f"Assistant: {reply}")


if __name__ == "__main__":  # pragma: no cover
    app()
