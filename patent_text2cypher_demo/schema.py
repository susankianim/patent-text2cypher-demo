def get_graph_schema_for_llm() -> str:
    """
    This schema is given to the LLM.

    The LLM must know the exact labels, relationships, and properties.
    Otherwise, it may hallucinate wrong Cypher queries.
    """
    return """
Graph schema:

Node labels and properties:
- Patent(id: STRING, title: STRING, filed_on: STRING)
- Organization(name: STRING)
- Inventor(name: STRING)
- Technology(name: STRING)

Relationships:
- (:Patent)-[:OWNED_BY]->(:Organization)
- (:Patent)-[:HAS_INVENTOR]->(:Inventor)
- (:Patent)-[:USES_TECHNOLOGY]->(:Technology)

Important rules:
- Do not invent labels, relationships, or properties.
- Only generate read-only Cypher queries.
- Use LIMIT 20 for list questions.
"""
