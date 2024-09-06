from pydantic import BaseModel

from agents.proxy import Proxy
from agents.thinker import Thinker

class Observation(BaseModel):
    observation: str
    source: str
    timestamp: str
    observation_type: str

    def __str__(self):
        return f"[{self.observation_type.upper()}] from: {self.source} - {self.observation}"



def observe(observation: Observation):
    thinker = Thinker()
    proxy = Proxy()
    thought = proxy.initiate_chat(thinker, message=str(observation), max_turns=1)
    return thought.summary.strip()