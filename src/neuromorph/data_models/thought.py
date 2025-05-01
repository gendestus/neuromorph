from pydantic import BaseModel, Field

class Thought(BaseModel):
    """
    A class to represent a thought.

    Attributes:
        timestamp (str): When the thought was made
        thought_id (str): UUID for the thought
        thought (str): the content of the thought
        content_chain (list): a list of observation, thought, and action ids that led to the thought
        metadata (dict): Additional metadata about the thought
    """

    timestamp: str = Field(..., description="When the thought was made")
    thought_id: str = Field(..., description="UUID for the thought")
    thought: str = Field(..., description="The content of the thought")
    content_chain: list = Field([], description="A list of observation, thought, and action ids that led to the thought")
    metadata: dict = Field({}, description="Additional metadata about the thought")