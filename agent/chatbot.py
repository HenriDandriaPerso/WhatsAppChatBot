from typing import Annotated

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition
from typing_extensions import TypedDict

from agent.prompt.systemPrompt import SYSTEM_PROMPT
from agent.tool.BasicToolNode import BasicToolNode
from agent.tool.retriever_tool import create_retriever_tools_from_urls


class State(TypedDict):
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

def compile_chatbot_graph() -> StateGraph:
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
    return graph_builder

def get_answer_from_chat(graph: CompiledStateGraph, from_number: str, to_number_str: str, message: str) -> str:
    # config = {"configurable": {"thread_id": from_number + "_" + to_number_str}}
    config = {"configurable": {"thread_id": from_number + "_" + to_number_str}}
    previous_value = graph.get_state(config).values
    if previous_value == {}:  # if the thread is new, add the initial state
        graph.update_state(config, {"messages": [
            ("system", SYSTEM_PROMPT)
        ]})

    events = graph.stream(
        {"messages": [("user", message)]}, config, stream_mode="values"
    )
    for event in events:
        event["messages"][-1].pretty_print()

    return event["messages"][-1].content
    






