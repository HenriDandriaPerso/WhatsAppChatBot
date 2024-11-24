from langchain.tools.retriever import create_retriever_tool
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import tools_condition
from BasicToolNode import BasicToolNode
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from tool.retriever_tool import create_retriever_tools_from_urls
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver





class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

urls = [
    "https://en.wikipedia.org/wiki/Johnny_Sins",
    "https://starsunfolded.com/johnny-sins/",
    "https://en.wikipedia.org/wiki/Steven_J._Wolfe",
]

def chatbot(state:State):
    llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)
    return {"messages": [llm.invoke(state["messages"])]}

retriever_tool = create_retriever_tools_from_urls(urls)
tool_node = BasicToolNode(tools=[retriever_tool])
graph_builder = StateGraph(State)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", chatbot)  

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {"tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

