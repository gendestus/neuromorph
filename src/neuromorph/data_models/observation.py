from pydantic import BaseModel, Field
from datetime import datetime

class Observation(BaseModel):
    """
    A class to represent an observation.

    Attributes:
        source (str): Where the observation came from
        timestamp (datetime): When the observation was made
        input_type (str): the type of observation (chat, hardware_sensor, file_upload, etc)
        content (str): The content of the observation
        content_type (str): The type of content (text, binary, etc)
        metadata (dict): Additional metadata about the observation
    """

    source: str = Field(..., description="Where the observation came from")
    timestamp: datetime = Field(..., description="When the observation was made")
    input_type: str = Field(..., description="The type of observation (chat, hardware_sensor, file_upload, etc)")
    content: str = Field(..., description="The content of the observation")
    content_type: str = Field(..., description="The type of content (text, binary, etc)")
    metadata: dict = Field({}, description="Additional metadata about the observation")
