from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.retrievers import Text2CypherRetriever

from patent_text2cypher_demo.config import (
    OPENAI_MODEL, OPENAI_API_KEY, OPENAI_BASE_URL, NEO4J_DATABASE
)
from patent_text2cypher_demo.schema import get_graph_schema_for_llm
from patent_text2cypher_demo.examples import get_few_shot_examples

def create_text2cypher_retriever(driver) -> Text2CypherRetriever:
    """
    Create the Text2CypherRetriever using parameters defined in config.
    Connects to the OpenAI-compatible endpoint.
    """

    llm = OpenAILLM(
        model_name=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        model_params={
            "temperature": 0
        },
    )

    retriever = Text2CypherRetriever(
        driver=driver,
        llm=llm,
        neo4j_schema=get_graph_schema_for_llm(),
        examples=get_few_shot_examples(),
        neo4j_database=NEO4J_DATABASE,
    )

    return retriever
