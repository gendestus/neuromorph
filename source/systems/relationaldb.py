import json
import pyodbc
from enum import IntEnum
from typing import Optional, List

'''
This module interfaces with a relational database and provides queuing functionality for the memories
as they come in. The thinking here is that as observations are made by various sensors, they are stored FIFO
and get "processed" when there's downtime. Process in this case could mean reflection or introspection...
basically creating concepts that could lead to a core identity.

TODO
This needs a lot of cleanup. 
the functions return plain objects that should have container classes

Also, side note
the memory types are not a boolean because I anticipate additional types down the road
'''

class MemoryType(IntEnum):
    OPERATIONAL = 1
    PRIORITY = 2


class RelationalDB:
    def __init__(self, use_local: bool = True):
        self.use_local = use_local
        self.creds = self._get_creds()
        self.conn_str = self._build_connection_string()

    def _get_creds(self) -> dict:
        filename = "dbcreds.local.json" if self.use_local else "dbcreds.json"
        with open(filename, encoding="utf8") as f:
            return json.load(f)

    def _build_connection_string(self) -> str:
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.creds['host']};"
            f"DATABASE={self.creds['database']};"
            f"UID={self.creds['user']};"
            f"PWD={self.creds['password']}"
        )

    def _execute_stored_procedure(self, procedure_name: str, should_return: bool = False, **kwargs):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            params = ", ".join(
                [f"@{key} = ?" for key in kwargs]
            )
            command = f"EXEC {procedure_name} {params}"
            values = [None if v is None else v for v in kwargs.values()]
            print(f"Executing: {command} with {values}")
            cursor.execute(command, values)
            if should_return:
                return cursor.fetchall()
            else:
                conn.commit()

    def add_memory(self, memory: str, priority: bool = False):
        self._execute_stored_procedure("AddMemory", False, memory=memory, priority=priority)

    def count_unprocessed_memories(self) -> int:
        result = self._execute_stored_procedure("CountMemories", True)
        return result[0][0] if result else 0

    def get_core_memories(self) -> List[str]:
        result = self._execute_stored_procedure("GetCoreMemories", True)
        return [row[0] for row in result]

    def peek_memory(self, memory_type: MemoryType) -> Optional[object]:
        proc_name = self._get_procedure_for_type(memory_type)
        result = self._execute_stored_procedure(proc_name, True)
        return result

    def pop_memory(self, memory_type: MemoryType) -> Optional[object]:
        proc_name = self._get_procedure_for_type(memory_type)
        memory = self._execute_stored_procedure(proc_name, True)
        if memory:
            self._execute_stored_procedure("ProcessMemory", False, memory_id=memory[0][0])
        return memory

    def _get_procedure_for_type(self, memory_type: MemoryType) -> str:
        if memory_type == MemoryType.OPERATIONAL:
            return "GetOperationalMemory"
        elif memory_type == MemoryType.PRIORITY:
            return "GetPriorityMemory"
        else:
            raise ValueError("Invalid memory type.")

