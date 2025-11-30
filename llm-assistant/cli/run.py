from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from analysis.analyzer import analyze_multiple_events, analyze_single_event
from logs.ingest import load_json_logs, load_text_logs
from llm.client import DEFAULT_MODEL, chat
from sources.cloudflare import fetch_cloudflare_logs
from sources.wazuh import fetch_wazuh_alerts

app = typer.Typer()
console = Console()


@app.command()
def analyze(path: str) -> None:
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
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


@app.command()
def pull_cloudflare(
    zone_id: str,
    api_token: str = typer.Option(..., envvar="CLOUDFLARE_API_TOKEN"),
    start: str | None = typer.Option(None, help="Start time (RFC3339)"),
    end: str | None = typer.Option(None, help="End time (RFC3339)"),
    limit: int = typer.Option(100, help="Maximum records to request"),
    analyze_result: bool = typer.Option(False, "--analyze", help="Analyze fetched logs"),
) -> None:
    destination, events = fetch_cloudflare_logs(zone_id, api_token, start=start, end=end, limit=limit)
    console.print(f"Saved Cloudflare logs to {destination}")
    if analyze_result:
        if not events:
            console.print("[red]No events returned to analyze.[/red]")
            return
        if len(events) == 1:
            result = analyze_single_event(events[0])
            console.print(Panel(str(result["explanation"]), title="Explanation", expand=False))
            console.print(f"Severity: [bold]{result['severity'].value}[/bold]")
        else:
            result = analyze_multiple_events(events)
            console.print(Panel(str(result["summary"]), title="Summary", expand=False))
            console.print(f"Severity: [bold]{result['severity'].value}[/bold]")


@app.command()
def pull_wazuh(
    base_url: str,
    username: str = typer.Option(..., envvar="WAZUH_USERNAME"),
    password: str = typer.Option(..., envvar="WAZUH_PASSWORD"),
    limit: int = typer.Option(100, help="Maximum alerts to request"),
    verify_ssl: bool = typer.Option(True, help="Verify TLS certificates"),
    analyze_result: bool = typer.Option(False, "--analyze", help="Analyze fetched alerts"),
) -> None:
    destination, events = fetch_wazuh_alerts(base_url, username, password, limit=limit, verify_ssl=verify_ssl)
    console.print(f"Saved Wazuh alerts to {destination}")
    if analyze_result:
        if not events:
            console.print("[red]No alerts returned to analyze.[/red]")
            return
        if len(events) == 1:
            result = analyze_single_event(events[0])
            console.print(Panel(str(result["explanation"]), title="Explanation", expand=False))
            console.print(f"Severity: [bold]{result['severity'].value}[/bold]")
        else:
            result = analyze_multiple_events(events)
            console.print(Panel(str(result["summary"]), title="Summary", expand=False))
            console.print(f"Severity: [bold]{result['severity'].value}[/bold]")


if __name__ == "__main__":
    app()
