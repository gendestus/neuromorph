import chromadb
import uuid

class VectorDB:
    def __init__(self, collection_name="memories"):
        self.client = chromadb.HttpClient(host="localhost", port="8000")
        self.memory_collection = self.client.get_or_create_collection(collection_name)

    def add_memory(self, memory: str, metadata: dict = {}) -> str:
        memory_id = str(uuid.uuid4())
        self.memory_collection.add(
            documents=[memory],
            metadatas=[metadata],
            ids=[memory_id]
        )
        return memory_id
    
    def get_relevant_memories(self, thought: str) -> list:
        results =self.memory_collection.query(
            query_texts=[thought],
            n_results=10,
            include=["documents"]
        )
        relevant_memories = results["documents"][0]
        return relevant_memories
