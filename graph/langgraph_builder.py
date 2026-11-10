from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, List
from langchain_core.documents import Document
from agents.document_agent import load_documents, create_vector_store, retrieve_documents
from agents.portfolio_agent import portfolio_chart
from agents.temperature_agent import TemperatureRetryAgent
from dotenv import load_dotenv
from utils.db_manager import init_db
import os

init_db()
load_dotenv()  # .env dosyasını yükle

if not os.environ.get("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY .env dosyasında tanımlanmalı.")


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    route: str  # Router'ın belirlediği yolu saklamak için


documents = load_documents()
vector_store = create_vector_store(documents)
temp_agent = TemperatureRetryAgent()



def retrieve(state: State):
    docs = retrieve_documents(vector_store, state["question"])
    return {"context": docs}

def generate(state: State):
    question = state["question"]
    context = state["context"]
    answer = temp_agent.run(question, context)
    return {"answer": answer}

def router(state: State):
    question = state["question"].lower()
    portfolio_keywords = ["portföy", "portfolio", "pasta grafiği", "müşteri id"]

    if any(keyword in question for keyword in portfolio_keywords):
        return {"route": "portfolio_chart"}
    else:
        return {"route": "retrieve"}

def build_graph():
    builder = StateGraph(State)
    builder.add_node("router", router)
    builder.add_node("retrieve", retrieve)
    builder.add_node("generate", generate)
    builder.add_node("portfolio_chart", portfolio_chart)
    builder.set_entry_point("router")
    builder.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "retrieve": "retrieve",
            "portfolio_chart": "portfolio_chart"
        }
    )
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)
    builder.add_edge("portfolio_chart", END)
    return builder.compile()