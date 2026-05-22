import time
import traceback
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from patent_text2cypher_demo.config import (
    NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE,
    DEBUG, check_environment_variables
)
from patent_text2cypher_demo.retriever_factory import create_text2cypher_retriever
from patent_text2cypher_demo.demo_questions import DEMO_QUESTIONS
from patent_text2cypher_demo.display import (
    DemoResult, console, print_title, print_graph_summary,
    display_demo_result, print_error
)

PRESENTATION_MODE = True
ENABLE_INTERACTIVE_MODE_AFTER_PRESENTATION = True


def get_graph_summary(driver) -> list:
    """Helper to query the graph size/summary."""
    records, _, _ = driver.execute_query(
        """
        MATCH (p:Patent)
        OPTIONAL MATCH (p)-[:OWNED_BY]->(o:Organization)
        OPTIONAL MATCH (p)-[:HAS_INVENTOR]->(i:Inventor)
        OPTIONAL MATCH (p)-[:USES_TECHNOLOGY]->(t:Technology)
        RETURN
            count(DISTINCT p) AS patents,
            count(DISTINCT o) AS organizations,
            count(DISTINCT i) AS inventors,
            count(DISTINCT t) AS technologies
        """,
        database_=NEO4J_DATABASE,
    )
    return [records[0].data()] if records else []


def run_question(retriever, question: str) -> DemoResult:
    """Runs a single question securely and returns DemoResult encapsulating output state."""
    try:
        result = retriever.get_search_results(query_text=question)
        cypher = result.metadata.get("cypher", "")
        rows = [record.data() for record in result.records]
        return DemoResult(question=question, cypher=cypher, rows=rows)
    except Exception as error:
        error_msg = traceback.format_exc() if DEBUG else f"{type(error).__name__}: {str(error)}"
        return DemoResult(question=question, cypher="", rows=[], error=error_msg)


def run_presentation_demo(retriever) -> None:
    """Linearly loop over DEMO_QUESTIONS for academic presentation playback."""
    console.print("\n[bold green]Starting Presentation Mode...[/bold green]\n")
    for q_data in DEMO_QUESTIONS:
        console.rule(f"[cyan]{q_data['title']}[/cyan]")
        result = run_question(retriever, q_data["question"])
        display_demo_result(result, title=q_data["title"])
        time.sleep(1.5)  # Small pause to distinguish presentation steps


def run_interactive_mode(retriever) -> None:
    """Continual prompt-loop allowing dynamic queries after presentation mode."""
    console.print("\n[bold green]🎤 Interactive Mode[/bold green]")
    console.print("Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            user_question = console.input("[bold cyan]Ask a question:[/bold cyan] ").strip()
            if user_question.lower() in {"exit", "quit"}:
                break
            if user_question:
                console.rule()
                result = run_question(retriever, user_question)
                display_demo_result(result)
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\n[bold magenta]Exiting interactively.[/bold magenta]")
            break
        except Exception as error:
            error_msg = traceback.format_exc() if DEBUG else f"{type(error).__name__}: {str(error)}"
            print_error(error_msg)


def main() -> None:
    """
    Main orchestrator logic orchestrating Graph connection,
    summaries, retrieving LLM chain, then invoking modes.
    """
    print_title()
    
    try:
        check_environment_variables()
    except RuntimeError as e:
        print_error(str(e))
        return

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
    )

    try:
        # Check connection.
        driver.verify_connectivity()
        console.print("[bold green]✅ Connected to local Neo4j database.[/bold green]")

        # Show that the existing graph is available.
        summary = get_graph_summary(driver)
        print_graph_summary(summary)

        # Create Text-to-Cypher tool wrapper.
        retriever = create_text2cypher_retriever(driver)

        if PRESENTATION_MODE:
            run_presentation_demo(retriever)

        if ENABLE_INTERACTIVE_MODE_AFTER_PRESENTATION:
            run_interactive_mode(retriever)

    except Neo4jError as error:
        print_error(f"Neo4j connection or query error:\n{error}")
    except Exception as error:
        error_msg = traceback.format_exc() if DEBUG else f"Unexpected error: {error}"
        print_error(error_msg)
    finally:
        driver.close()
        console.print("\n[bold green]✅ Demo finished.[/bold green]")


if __name__ == "__main__":
    main()
