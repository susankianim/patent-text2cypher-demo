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
- Patent_ID from the CSV is stored as Patent.id.
- Title from the CSV is stored as Patent.title.
- Filed_On from the CSV is stored as Patent.filed_on.
- OwnedBy from the CSV is stored as Organization.name.
- Inventors from the CSV are stored as Inventor.name.
- Technologies from the CSV are stored as Technology.name.
- Do not invent labels, relationships, or properties.
- Only generate read-only Cypher queries.
- Use LIMIT 20 for list questions.
"""
