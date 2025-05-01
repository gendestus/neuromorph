import json

class Database:
    def __init__(self, creds_file: str = None):
        self.creds_file = creds_file

    def get_core_memories(self) -> list:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def get_creds(self):
        if not self.creds_file:
            raise ValueError("File path must be provided")
        
        try:
            with open(self.creds_file, "r") as f:
                creds = json.load(f)
            return creds
        except FileNotFoundError:
            print(f"Credentials file not found: {self.creds_file}")
            return None
    def get_recent_memories(self, num_memories: int) -> list:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def log_memory(self, memory: object) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def log_observation(self, observation: object) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
        
    def run_stored_procedure(self, name: str, should_return: bool = False, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")