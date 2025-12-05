from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4


load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model='gemini-embedding-001')

PERSIST_DIR = Path("../vectorstore")
DOCUMENTS_DIR = Path("../data/documents")

# Ensure whether directories exist or not
PERSIST_DIR.mkdir(parents=True, exist_ok=True)
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


def ingest_documents():
    files = list(DOCUMENTS_DIR.glob("*.pdf"))
    
    all_docs = []
    
    # Loading documents
    for file in files:
        print(f"Loading {file}...")
        loader = PyPDFLoader(str(file))
        docs = loader.load()
        all_docs.extend(docs)
    
    # Split documents
    print("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(all_docs)
    
    # Store in Chroma
    vector_store = Chroma(
        collection_name="laptop_manual",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR
    )
    uuids = [str(uuid4()) for _ in range(len(chunks))]
    vector_store.add_documents(documents=chunks, ids=uuids)
    print("Ingestion completed, vector store updated")
    
    
    
if __name__=="__main__":
    ingest_documents()