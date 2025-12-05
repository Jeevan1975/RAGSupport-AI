from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from ..models.prompts import chat_prompt
from ..models.llm import get_llm
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()

PERSIST_DIR = Path("../vectorstore")

PERSIST_DIR.mkdir(parents=True, exist_ok=True)


# Load vector store
embeddings = GoogleGenerativeAIEmbeddings(model='gemini-embedding-001')
vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR
)

retriever = vector_store.as_retriever(search_kwargs={"k":6})

prompt = chat_prompt

model = get_llm()

parser = StrOutputParser()

rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | parser
)

async def run_rag(query: str):
    return await rag_chain.ainvoke({"question": query})