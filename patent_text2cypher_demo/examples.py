from typing import List

def get_few_shot_examples() -> List[str]:
    """
    Few-shot examples help the LLM generate more accurate Cypher.

    These examples match your actual graph structure.
    """
    return [
        """
User question: Which patents use sensor technology?
Cypher:
MATCH (p:Patent)-[:USES_TECHNOLOGY]->(t:Technology {name: "sensor"})
RETURN p.id AS patent_id, p.title AS title
LIMIT 20
""",
        """
User question: Who are the inventors of patent 10457113?
Cypher:
MATCH (p:Patent {id: "10457113"})-[:HAS_INVENTOR]->(i:Inventor)
RETURN i.name AS inventor
LIMIT 20
""",
        """
User question: Which organization owns patent 10457208?
Cypher:
MATCH (p:Patent {id: "10457208"})-[:OWNED_BY]->(o:Organization)
RETURN o.name AS organization
LIMIT 20
""",
        """
User question: Which patents are owned by MAGNA ELECTRONICS INC?
Cypher:
MATCH (p:Patent)-[:OWNED_BY]->(o:Organization {name: "MAGNA ELECTRONICS INC"})
RETURN p.id AS patent_id, p.title AS title
LIMIT 20
""",
        """
User question: How many patents use camera technology?
Cypher:
MATCH (p:Patent)-[:USES_TECHNOLOGY]->(t:Technology {name: "camera"})
RETURN count(DISTINCT p) AS number_of_patents
""",
        """
User question: Which inventors worked on patents related to sensor technology?
Cypher:
MATCH (i:Inventor)<-[:HAS_INVENTOR]-(p:Patent)-[:USES_TECHNOLOGY]->(t:Technology {name: "sensor"})
RETURN DISTINCT i.name AS inventor
LIMIT 20
""",
    ]
