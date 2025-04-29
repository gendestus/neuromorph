import json

class Database:
    def __init__(self, use_local: bool = True):
        self.use_local = use_local

    def get_core_memories(self) -> list:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def get_creds(self):
        creds_file = "source/dbcreds.json"
        if self.use_local:
            creds_file = "source/dbcreds.local.json"
        
        try:
            with open(creds_file, "r") as f:
                creds = json.load(f)
            return creds
        except FileNotFoundError:
            print(f"Credentials file not found: {creds_file}")
            return None
    def get_recent_memories(self, num_memories: int) -> list:
        raise NotImplementedError("This method should be implemented by subclasses.")
        
    def run_stored_procedure(self, name: str, should_return: bool = False, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")