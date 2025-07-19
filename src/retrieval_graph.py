from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
# from langchain_deepseek import ChatDeepSeek
# from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
import os

from server import mcp


# """
# Use this tool when the user asks about the phone.
# Use the context to answer the user's question.

# Input:
#     query: str -> The user asks about the phone

# Output:
#     Information about the phones that match the user's question
# """

# # Load environment variables
# load_dotenv()

# print(os.getenv("NEO4J_URI"))

# # 1. Kết nối graph
# graph = Neo4jGraph(
#     url=os.getenv("NEO4J_URI"),
#     username=os.getenv("NEO4J_USERNAME"),
#     password=os.getenv("NEO4J_PASSWORD")
# )

# # 2. Prompt để sinh Cypher
# CYPHER_GENERATION_PROMPT = PromptTemplate.from_template("""
# You are a graph database based question answering system. Convert user questions into corresponding Cypher queries.

# Below is the data diagram:
# - (:Phone {{model}})
# - (:Phone)-[:HAS_PRICE]->(:Price {{value}})
# - (:Phone)-[:HAS_RAM]->(:RAM {{value}})
# - (:Phone)-[:HAS_OS]->(:OS {{value}})
# - (:Phone)-[:HAS_BATTERY]->(:Battery {{value}})
# - (:Phone)-[:HAS_DISPLAY]->(:Display {{value}})
# - (:Phone)-[:HAS_CAMERA]->(:Camera {{value}})
# - (:Phone)-[:HAS_SIM]->(:Sim {{value}})
# - (:Phone)-[:HAS_PROCESSOR]->(:Processor {{value}})
# - (:Phone)-[:HAS_RATING]->(:Rating {{value}})
# - (:Phone)-[:HAS_CARD]->(:Card {{value}})

# If insufficient information, return a LIMIT 3 query.

# Question: {question}
# Cypher query:
# """)

# # 3. LLM + Chain
# llm = ChatDeepSeek(
#     temperature=0, 
#     model="deepseek-chat",
#     api_key=SecretStr(os.getenv("DEEPSEEK_API_KEY") or ""),
#     api_base=os.getenv("DEEPSEEK_API_BASE") or "",
#     max_tokens=1024
# )

# chain = GraphCypherQAChain.from_llm(
#     llm=llm,
#     graph=graph,
#     verbose=True,
#     cypher_prompt=CYPHER_GENERATION_PROMPT,
#     allow_dangerous_requests=True,
#     return_intermediate_steps=True
# )

# # 4. Thử truy vấn
# # query = "I want to buy a phone price less than 10000. Give me a list of 3 compatible phones and their displays"
# # result = chain.invoke({"query": query})

# # print("Kết quả trả về:")
# # print(result)


@mcp.prompt()
def change_query_to_cypher(query: str):
    return """
    Use this prompt when the user asks about the phones.
    Change the user's question to a Cypher query. Below is the data diagram:
    - (:Phone {{model}})
    - (:Phone)-[:HAS_PRICE]->(:Price {{value}})
    - (:Phone)-[:HAS_RAM]->(:RAM {{value}})
    - (:Phone)-[:HAS_OS]->(:OS {{value}})
    - (:Phone)-[:HAS_BATTERY]->(:Battery {{value}})
    - (:Phone)-[:HAS_DISPLAY]->(:Display {{value}})
    - (:Phone)-[:HAS_CAMERA]->(:Camera {{value}})
    - (:Phone)-[:HAS_SIM]->(:Sim {{value}})
    - (:Phone)-[:HAS_PROCESSOR]->(:Processor {{value}})
    - (:Phone)-[:HAS_RATING]->(:Rating {{value}})
    - (:Phone)-[:HAS_CARD]->(:Card {{value}})

    If insufficient information, return a LIMIT 5 query.

    Input:
        query: str -> The user asks about the phone

    Output:
        Cypher query: str -> The Cypher query to retrieve the information about the phones
    """.format(query=query)

@mcp.tool()
def retrieve_graph(cypher_query: str):
    """
    Use this tool when the user asks about the phone.
    This tool only accepts cypher queries.
    Return the result of the cypher query.
    """

    # Load environment variables
    load_dotenv()

    print(os.getenv("NEO4J_URI"))

    # Kết nối graph
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    result = graph.query(cypher_query)
    return result






