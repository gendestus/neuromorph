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
            cursor.execute(command)
            result = None
            if should_return:
                result = cursor.fetchall()
            conn.commit()
            return result

def add_message(conversation_id: str, message: str, sender: str):        
    execute_stored_procedure("AddMessage", False, conversation_id=conversation_id, message=message, sender=sender)
    
def create_conversation(note: str|None=None):
    id = execute_stored_procedure("CreateConversation", True, note=note)
    return str(id[0][0])
