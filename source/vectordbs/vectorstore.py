import json

class VectorStore:
    def __init__(self, use_local: bool = True):
        self.use_local = use_local

    def get_creds(self):
        if self.use_local:
            creds_file = "source/dbcreds.local.json"
        else:
            creds_file = "source/dbcreds.json"
        try:
            with open(creds_file, "r") as f:
                creds = json.load(f)
            return creds
        except FileNotFoundError:
            print(f"Credentials file not found: {creds_file}")
            return None

    def get_relevant_memories(self, query: str, num_results: int = 10) -> list:
        """
        Get relevant memories from the vector store based on the query.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")   
    
    def store_memory(self, memory: str, metadata: object):
        raise NotImplementedError("This method should be implemented by subclasses.")   