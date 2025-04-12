import json

import pymssql

'''
This module interfaces with a relational database and provides queuing functionality for the memories
as they come in. The thinking here is that as observations are made by various sensors, they are stored FIFO
and get "processed" when there's downtime. Process in this case could mean reflection or introspection...
basically creating concepts that could lead to a core identity.

TODO
This needs a lot of cleanup. 
pymssql is no longer supported
the functions return plain objects that should have container classes
my brain is dead right now but I know there's a better way to do memory type flags in python....looking at you, enums

Also, side note
the memory types are not a boolean because I anticipate additional types down the road
'''

USE_LOCAL = True
OPERATIONAL_MEMORY = 1
PRIORITY_MEMORY = 2

def get_creds():
    if USE_LOCAL:
        with open("dbcreds.local.json", encoding="utf8") as f:
            return json.load(f)
    else:
        with open("dbcreds.json") as f:
            return json.load(f)
    
def execute_stored_procedure(procedure_name, should_return, **kwargs):
    creds = get_creds()
    with pymssql.connect(
        server=creds["host"], 
        user=creds["user"], 
        password=creds["password"], 
        database=creds["database"],
        ) as conn:
        with conn.cursor() as cursor:
            command = f"EXEC {procedure_name} " + ", ".join([f"@{key} = '{value}'" for key, value in kwargs.items()])
            command = command.replace("'None'", "NULL")
            print(command)
            cursor.execute(command)
            if should_return:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()

def add_memory(memory: str, priority: bool = False):
    execute_stored_procedure("AddMemory", False, memory=memory, priority=priority)

def count_unprocessed_memories() -> int:
    count_obj = execute_stored_procedure("CountMemories", True)
    return count_obj[0][0]

def peek_memory(memory_type: int) -> object | None:
    if memory_type == OPERATIONAL_MEMORY:
        return execute_stored_procedure("GetOperationalMemory", True)
    elif memory_type == PRIORITY_MEMORY:
        return execute_stored_procedure("GetPriorityMemory", True)
    else:
        raise ValueError("Invalid memory type. Use OPERATIONAL_MEMORY for operational memory or PRIORITY_MEMORY for priority memory.")

def pop_memory(memory_type: int) -> object | None:
    if memory_type == OPERATIONAL_MEMORY:
        memory = execute_stored_procedure("GetOperationalMemory", True)
    elif memory_type == PRIORITY_MEMORY:
        memory = execute_stored_procedure("GetPriorityMemory", True)
    else:
        raise ValueError("Invalid memory type. Use OPERATIONAL_MEMORY for operational memory or PRIORITY_MEMORY for priority memory.")  
    if memory:
        execute_stored_procedure("ProcessMemory", False, memory_id=memory[0][0])
    return memory