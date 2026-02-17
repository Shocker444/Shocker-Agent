from typing import TypedDict, Annotated
from loguru import logger
from langchain.chat_models import init_chat_model
from langgraph.graph import add_messages
from langchain.messages import (
    SystemMessage,
)
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from settings import settings
from prompts import SYSTEM_PROMPT, TEXT_TO_SPEECH_PROMPT


model = init_chat_model(model=settings.LLM_MODEL_NAME, model_provider="openai", temperature=0, api_key=settings.OPENAI_API_KEY)
    

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    job_description: str


async def call_llm(state: AgentState):
    """Call the LLM with the given messages."""

    response = await model.ainvoke(
        [
            SystemMessage(
                content=SYSTEM_PROMPT.format(JOB_DESCRIPTION=state["job_description"],
                                             RESUME_DATA="N/A",
                                             tts_prompt=TEXT_TO_SPEECH_PROMPT)
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