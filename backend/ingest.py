from langchain_chroma import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model='gemini-embedding-001')

PERSIST_DIR = "./vectorstore"

if not PERSIST_DIR:
    os.mkdir('./vectorstore')


def ingest_documents():
    documents_dir = "./data/documents"
    files = os.listdir(documents_dir)
    
    all_docs = []
    
    # Loading documents
    for file in files:
        if file.endswith(".pdf"):
            print(f"Loading {file}...")
            loader = PyPDFLoader(os.path.join(documents_dir, file))
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
    print("Creating vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    
    
    
    
if __name__=="__main__":
    ingest_documents()