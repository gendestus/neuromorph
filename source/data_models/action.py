from pydantic import BaseModel, Field

class Action(BaseModel):
    """
    A class to represent an action.

    Attributes:
        timestamp (str): When the action was made
        action_type (str): The type of action (API_call, hardware_control, etc)
        action_id (str): UUID for the action
        description (str): A description of the action
        result (str): The result of the action
        metadata (dict): Additional metadata about the action
    """

    timestamp: str = Field(..., description="When the action was made")
    action_type: str = Field(..., description="The type of action (API_call, hardware_control, etc)")
    action_id: str = Field(..., description="UUID for the action")
    description: str = Field(..., description="A description of the action")
    result: str = Field(..., description="The result of the action")
    metadata: dict = Field({}, description="Additional metadata about the action")