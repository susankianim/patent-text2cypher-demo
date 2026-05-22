from dataclasses import dataclass
from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

# Global rich console instance for this module
console = Console()

@dataclass
class DemoResult:
    """Structure to hold the retrieved execution outputs cleanly."""
    question: str
    cypher: str
    rows: List[Dict]
    error: Optional[str] = None


def print_title() -> None:
    """Display the presentation title."""
    console.print(Panel.fit("[bold blue]🚀 Patent Text-to-Cypher Demo[/bold blue]", border_style="blue"))


def print_graph_summary(summary: List[Dict]) -> None:
    """Display a quick summary of the graph content to prove connection."""
    console.print("\n[bold green]📊 Existing graph summary:[/bold green]")
    table = Table(show_header=True, header_style="bold magenta")
    
    if summary:
        keys = list(summary[0].keys())
        for key in keys:
            table.add_column(key)
        for row in summary:
            table.add_row(*[str(row.get(k, "")) for k in keys])
        console.print(table)
    else:
        console.print("No summary available.")


def print_question(question: str, title: Optional[str] = None) -> None:
    """Display the natural language question formatted nicely."""
    title_text = f"🧑 Natural language question: {title}" if title else "🧑 Natural language question"
    console.print(Panel(question, title=title_text, border_style="cyan"))


def print_cypher(cypher: str) -> None:
    """Display the generated cypher string with highlighting."""
    syntax = Syntax(cypher.strip(), "cypher", theme="monokai", line_numbers=False)
    console.print(Panel(syntax, title="🤖 Generated Cypher", border_style="green"))


def print_rows(rows: List[Dict]) -> None:
    """Display the retrieved rows from Neo4j."""
    console.print("\n[bold yellow]📦 Neo4j result:[/bold yellow]")
    if not rows:
        console.print(Panel("No records found.", border_style="yellow"))
        return

    table = Table(show_header=True, header_style="bold magenta")
    
    # Collect all available keys to render as columns across all rows
    keys = list({k for row in rows for k in row.keys()})
    for key in keys:
        table.add_column(key)

    for row in rows:
        table.add_row(*[str(row.get(k, "")) for k in keys])

    console.print(table)


def print_error(error: str) -> None:
    """Display an error cleanly in bold red panel."""
    console.print(Panel(f"[bold red]❌ Error:[/bold red]\n{error}", border_style="red"))


def display_demo_result(result: DemoResult, title: Optional[str] = None) -> None:
    """Main generic runner handling the displaying mechanics for any DemoResult."""
    print_question(result.question, title)
    
    if result.error:
        print_error(result.error)
    else:
        print_cypher(result.cypher)
        print_rows(result.rows)
    console.print()
