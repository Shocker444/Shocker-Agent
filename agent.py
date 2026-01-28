from typing import TypedDict, Annotated
from langchain.chat_models import init_chat_model
from langgraph.graph import add_messages
from langchain.messages import (
    SystemMessage,
    HumanMessage,
)
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from settings import settings

model = init_chat_model(model=settings.LLM_MODEL_NAME, temperature=0, api_key=settings.OPENAI_API_KEY)
    

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def call_llm(state: AgentState):
    """Call the LLM with the given messages."""

    response = model.invoke(
        [
            SystemMessage(
                content="You are a friendly AI assistant with the sole aim of information and help."
            )
        ]
        + state["messages"]
    )
    return {"messages": response.content}


graph_builder = StateGraph(AgentState)
graph_builder.add_node("call_llm", call_llm)
graph_builder.add_edge(START, "call_llm")
graph_builder.add_edge("call_llm", END)

agent = graph_builder.compile(checkpointer=InMemorySaver())