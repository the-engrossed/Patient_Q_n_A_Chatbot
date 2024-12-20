import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from retrieval.loader import load_medquad, df_to_documents
from dotenv import load_dotenv
import time

load_dotenv()

def get_openai_embeddings():
    """Initialize the OpenAI Embeddings object."""
    # Assumes your OpenAI API key is set as an environment variable
    return OpenAIEmbeddings()

def create_vectordb(docs, persist_directory="db/chroma/"):
    """Create and persist a Chroma vector database from LangChain Documents."""
    embeddings = get_openai_embeddings()
    vectordb = Chroma.from_documents(
        docs, 
        embeddings,
        persist_directory=persist_directory
    )
    print(f"Vector DB created and persisted with {len(docs)} documents.")
    return vectordb

def load_vectordb(persist_directory="db/chroma/"):
    """Load an existing Chroma vector database."""
    embeddings = get_openai_embeddings()
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    print("Loaded vector DB from persisted directory.")
    return vectordb

if __name__ == "__main__":
    # Load and preprocess data
    df = load_medquad()
    docs = df_to_documents(df)
    MAX_BATCH_SIZE = 100  # Adjust lower/higher according to dataset and API limit

    embeddings = get_openai_embeddings()
    persist_directory = "db/chroma/"
    # Create empty vector DB
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    print("Vector DB created, starting batched addition…")

    # Add docs in batches to avoid OpenAI token limits
    for i in range(0, len(docs), MAX_BATCH_SIZE):
        batch = docs[i:i + MAX_BATCH_SIZE]
        print(f"Starting batch {i} to {i+len(batch)} (len={len(batch)})")
        try:
            vectordb.add_documents(batch)
            print(f"Finished batch {i} to {i+len(batch)}")
            time.sleep(1)  # Slight delay to avoid rate limits
        except Exception as e:
            print(f"Error adding docs {i} to {i+len(batch)}: {e}")
            break

    print(f"Finished. Vector DB now contains {len(docs)} documents.")
    # create_vectordb(docs)
