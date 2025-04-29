from pydantic import BaseModel, Field

class Memory(BaseModel):
    """
    
    """

    memory_id: str = Field(..., description="UUID of the core memory")
    memory: str = Field(..., description="The core memory content")
    created: str = Field(..., description="The date and time when the core memory was created")
    related_observation_ids: list = Field([], description="List of observation IDs related to this memory")
    metadata: dict = Field({}, description="Additional metadata about the memory")