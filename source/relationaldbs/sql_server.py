import pyodbc
import json
from .database import Database
from source.data_models.core_memory import CoreMemory
from source.data_models.memory import Memory

class SQLServer(Database):
    def __init__(self, use_local=True):
        super().__init__(use_local)
        self.creds = self.get_creds()
        self.conn_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};Encrypt=no;SERVER={self.creds['host']};DATABASE={self.creds['database']};UID={self.creds['user']};PWD={self.creds['password']}"

    def get_core_memories(self) -> list:
        if self.creds is None:
            print("No credentials available.")
            return None
        
        core_memories = []
        rows = self.run_stored_procedure("GetCoreMemories", should_return=True)
        for row in rows:
            core_memories.append(CoreMemory(
                core_memory_id=row[0],
                memory=row[1],
                created=str(row[2]),
                author=row[3]
            ))
        return core_memories
    
    def get_recent_memories(self, num_memories: int) -> list:
        if self.creds is None:
            print("No credentials available.")
            return None
        
        recent_memories = []
        rows = self.run_stored_procedure("GetRecentMemories", should_return=True, num_memories=num_memories)
        for row in rows:
            recent_memories.append(Memory(
                memory_id=row[0],
                memory=row[1],
                created=str(row[2]),
                related_observation_ids=json.loads(row[3]),
                metadata=json.loads(row[4])
            ))
        return recent_memories


    def run_stored_procedure(self, name: str, should_return = False, **kwargs):
        if self.creds is None:
            print("No credentials available.")
            return None
        
        try:
            with pyodbc.connect(self.conn_string) as conn:
                cursor = conn.cursor()
                params = []
                for key, value in kwargs.items():
                    if isinstance(value, str):
                        params.append(f"@{key}='{value}'")
                    else:
                        params.append(f"@{key}={value}")
                param_str = ", ".join(params)
                query = f"EXEC {name} {param_str}"
                cursor.execute(query)
                
                if should_return:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return None
        except pyodbc.Error as e:
            print(f"Error executing stored procedure {name}: {e}")
            return None
