from typing import List, Tuple, Dict, Any, Union, Annotated

from db import create_conversation, add_message

def output(message: str) -> str:
    return message