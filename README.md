# Patent Text-to-Cypher Demo

A modular demonstration showing how to use an LLM to automatically translate natural language questions into Cypher queries and safely retrieve results from a Neo4j knowledge graph.

## 📦 Supported Graph Schema
- **Nodes**: `Patent`, `Organization`, `Inventor`, `Technology`
- **Relationships**: `(:Patent)-[:OWNED_BY]->(:Organization)`, `(:Patent)-[:HAS_INVENTOR]->(:Inventor)`, `(:Patent)-[:USES_TECHNOLOGY]->(:Technology)`

## 💻 Setup

1. **Environment Variables**: Create a `.env` file at the project root based on your credentials:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gemini-2.5-flash
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
```

2. **Install Dependencies**:
```bash
uvync  # or: pip install -r requirements.txt
```

## 🚀 How to Run
Run the application entry point:
```bash
uv run python -m patent_text2cypher_demo.app
```
*(Or use `python -m patent_text2cypher_demo.app` if your virtual environment is manually activated).*
