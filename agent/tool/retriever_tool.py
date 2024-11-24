from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool


def create_retriever_tools_from_urls(urls):
    """
    This function processes a list of URLs to create a retriever tool for searching and returning information.

    :param urls: A list of string URLs to be loaded and processed.
    :return: A retriever tool configured to search through documents obtained from the URLs.
    """

    # Load and flatten documents
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Add splits to a vector database
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(),
    )
    
    # Create a retriever from the vector store
    retriever = vectorstore.as_retriever()

    # Create and return the retriever tool
    retriever_tool = create_retriever_tool(
        retriever,
        name="retrieve_JonnySins_Facts",
        description="Search and return information about JonnySins",
    )

    return retriever_tool

