import json

class VectorStore:
    def __init__(self, creds_file: str = None):
        self.creds = self.get_creds(creds_file)

    def get_creds(self, creds_file: str = None):
        if not creds_file:
            raise ValueError("Credentials file path must be provided.")
            
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