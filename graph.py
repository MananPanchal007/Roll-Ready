import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langchain.schema import SystemMessage


class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = init_chat_model(
    model_provider="openai", model="gpt-4.1"
)

def chatbot(state: State):
    system_prompt = SystemMessage(content="""
        You are an AI interviewer. You will ask the user a series of questions to
        gather information about their skills and experience. 

        First, user will greet you and then you have to start the conversation.                           
    """)

    message = llm.invoke([system_prompt] + state["messages"])
    return {"messages": [message]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)