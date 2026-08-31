from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from app.agent.nodes.create_order import create_order
from app.agent.nodes.find_product import find_product
from app.agent.nodes.handle_result import handle_result
from app.agent.nodes.parse_intent import parse_intent
from app.agent.state import AgentState


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("parse_intent", parse_intent)
    graph.add_node("find_product", find_product)
    graph.add_node("create_order", create_order)
    graph.add_node("handle_result", handle_result)

    graph.add_edge(START, "parse_intent")
    graph.add_edge("parse_intent", "find_product")
    graph.add_edge("find_product", "create_order")
    graph.add_edge("create_order", "handle_result")
    graph.add_edge("handle_result", END)
    return graph.compile()


@lru_cache(maxsize=1)
def get_graph():
    return build_graph()
