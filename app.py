import os
from typing import List
from dotenv import load_dotenv
import gradio as gr

from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere 
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.llms import ChatMessage
from pinecone import Pinecone

load_dotenv()

INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "rag-project")
MODEL_NAME = "command-r-08-2024"


Settings.embed_model = CohereEmbedding(
    api_key=os.environ["COHERE_API_KEY"], 
    model_name="embed-english-v3.0"
)

Settings.llm = Cohere(
    api_key=os.environ["COHERE_API_KEY"], 
    model=MODEL_NAME
)

class RetrievalEvent(Event):
    query: str
    nodes: List


class NexusAgent(Workflow):
    def __init__(self, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index

    @step
    async def retrieve(self, ev: StartEvent) -> RetrievalEvent:
        query = ev.get("query", "").strip()
        retriever = self.index.as_retriever(similarity_top_k=5)
        nodes = retriever.retrieve(query)
        return RetrievalEvent(query=query, nodes=nodes)

    @step
    async def synthesize(self, ev: RetrievalEvent) -> StopEvent:
        if not ev.nodes:
            return StopEvent(result="לא נמצא מידע רלוונטי בתיעוד ב-Pinecone.")

        context = "\n\n".join([n.get_content() for n in ev.nodes])
        
        system_prompt = "You are a professional system analyzer. Answer in Hebrew based on the context provided."
        user_message = f"Context:\n{context}\n\nQuestion: {ev.query}"
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_message)
        ]

        try:
            response = await Settings.llm.achat(messages)
            return StopEvent(result=str(response))
        except Exception as e:
            return StopEvent(result=f"שגיאה ביצירת תשובה מה-LLM: {str(e)}")

def setup_agent():
    try:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        p_index = pc.Index(INDEX_NAME)
        vector_store = PineconeVectorStore(pinecone_index=p_index)
    
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        return NexusAgent(index=index, timeout=60)
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return None

nexus_agent = setup_agent()

async def chat_interface(message, history):
    if not nexus_agent:
        return "❌ שגיאת חיבור ל-Pinecone. וודא שה-API Key ושם האינדקס נכונים ב-env."
    
    try:
        result = await nexus_agent.run(query=message)
        return str(result)
    except Exception as e:
        print(f"DEBUG ERROR: {e}") 
        return f"❌ שגיאה בהרצת המערכת: {str(e)}"

demo = gr.ChatInterface(
    fn=chat_interface,
    title="Nexus Intelligence Agent",
    description="מערכת RAG לניתוח תיעוד טכני מבוססת LlamaIndex, Cohere ו-Pinecone"
)

if __name__ == "__main__":
    demo.launch(share=False)
