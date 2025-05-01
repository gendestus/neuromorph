import pyodbc
import json
from neuromorph.relationaldbs.database import Database
from neuromorph.data_models.core_memory import CoreMemory
from neuromorph.data_models.memory import Memory
from neuromorph.data_models.observation import Observation

class SQLServer(Database):
    def __init__(self, creds_file: str = None):
        super().__init__(creds_file=creds_file)
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

    def log_memory(self, memory: Memory) -> str:
        if self.creds is None:
            print("No credentials available.")
            return None
        
        try:
            row = self.run_stored_procedure("LogMemory", memory=memory.memory, created=memory.created, related_observation_ids=json.dumps(memory.related_observation_ids), metadata=json.dumps(memory.metadata), should_return=True)
            if row:
                return row[0][0]
            else:
                print("No memory id row returned from stored procedure.")
                return None
        except pyodbc.Error as e:
            print(f"Error logging memory: {e}")
            return None
    
    def log_observation(self, observation: Observation) -> str:
        if self.creds is None:
            print("No credentials available.")
            return None
        
        try:
            row = self.run_stored_procedure("LogObservation", source=observation.source, timestamp=observation.timestamp, input_type=observation.input_type, observation_content=observation.content, content_type=observation.content_type, metadata=json.dumps(observation.metadata), should_return=True)
            if row:
                return row[0][0]
            else:
                print("No observation id row returned from stored procedure.")
                return None
        except pyodbc.Error as e:
            print(f"Error logging observation: {e}")
            return None


    def run_stored_procedure(self, name: str, should_return = False, **kwargs):
        if self.creds is None:
            print("No credentials available.")
            return None
        
        try:
            with pyodbc.connect(self.conn_string) as conn:
                cursor = conn.cursor()
                # Build a parameter placeholder list like "@param1 = ?"
                param_placeholders = [f"@{key} = ?" for key in kwargs.keys()]
                param_str = ", ".join(param_placeholders)

                # Build the parameter values in the same order
                param_values = list(kwargs.values())

                query = f"EXEC {name} {param_str}"
                print(f"Executing: {query} with params: {param_values}")

                cursor.execute(query, param_values)

                if should_return:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return None
        except pyodbc.Error as e:
            print(f"Error executing stored procedure {name}: {e}")
            return None
