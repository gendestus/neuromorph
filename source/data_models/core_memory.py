from pydantic import BaseModel, Field

class CoreMemory(BaseModel):
    """
    CoreMemory is a class that represents the core memory of an AI agent.
    It is responsible for storing and managing the agent's knowledge and experiences.

    core_memory_id (str): UUID of the core memory
    memory (str): The core memory content
    created (datetime): The date and time when the core memory was created
    author [optional] (str): The author of the core memory
    """

    core_memory_id: str = Field(..., description="UUID of the core memory")
    memory: str = Field(..., description="The core memory content")
    created: str = Field(..., description="The date and time when the core memory was created")
    author: str = Field(None, description="The author of the core memory")