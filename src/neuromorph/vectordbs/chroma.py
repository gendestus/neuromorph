import chromadb
import uuid

import chromadb.errors

from neuromorph.vectordbs.vectorstore import VectorStore

class Chroma(VectorStore):

    LONG_TERM_MEMORY_COLLECTION_NAME = "long_term_memory"

    def __init__(self, creds_file: str = None):
        super().__init__(creds_file=creds_file)

        if self.creds is None:
            print("No credentials available.")
            return None
        host = self.creds["vector_db_host"]
        port = self.creds["vector_db_port"]

        self.chroma_client = chromadb.HttpClient(host, port)

        self.long_term_collection = self.chroma_client.get_or_create_collection(name=Chroma.LONG_TERM_MEMORY_COLLECTION_NAME)

    def get_relevant_memories(self, query: str, num_results: int = 10) -> list:
        """
        Get relevant memories from the vector store based on the query.
        """
        memories = []
        query_texts = [query]
        results = self.long_term_collection.query(query_texts=query_texts, n_results=num_results)
        for result in results['documents'][0]:
            memories.append(result)
        return memories


    def store_memory(self, memory: str, metadata: object) -> str:
        id = str(uuid.uuid4())
        self.long_term_collection.add(
            documents=[memory],
            metadatas=[metadata],
            ids=[id]
        )
        return id
        