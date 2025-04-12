import json

import pymssql

def get_creds():
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

def create_conversation(note: str|None=None) -> str:
    return execute_stored_procedure("CreateConversation", True, note=note)