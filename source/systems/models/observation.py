from pydantic import BaseModel, Field
from datetime import datetime

class Observation(BaseModel):
    description: str
    timestamp: datetime = Field(default_factory=datetime.now)
    source: str

    def __str__(self):
        return f"{self.timestamp} - from: {self.source} - {self.description}"