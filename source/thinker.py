from source.data_models.observation import Observation
from source.data_models.thought import Thought

from source.agents.thinker_agent import ThinkerAgent

class Thinker:
    def __init__(self):
        self.agent = ThinkerAgent()

    def observe(self, observation: Observation) -> Thought:
        # store observation
        # think about observation
        # return thought
        pass