import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.cohere import CohereEmbedding
from pinecone import Pinecone

load_dotenv()

Settings.embed_model = CohereEmbedding(api_key=os.environ["COHERE_API_KEY"], model_name="embed-english-v3.0")
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)

def run_ingestion():
    print("🚀 Starting Ingestion...")
    if not os.path.exists("./data"):
        print("❌ Error: 'data' directory not found!")
        return

    reader = SimpleDirectoryReader("./data")
    documents = reader.load_data()
    
    for doc in documents:
        doc.metadata["file_name"] = os.path.basename(doc.metadata.get("file_path", "unknown"))

    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    pinecone_index = pc.Index("rag-project")
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex.from_documents(documents, storage_context=storage_context, show_progress=True)
    print("✅ Ingestion complete.")

if __name__ == "__main__":
    run_ingestion()