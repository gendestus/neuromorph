from neuromorph.data_models.observation import Observation
from neuromorph.data_models.thought import Thought
from neuromorph.data_models.memory import Memory

from neuromorph.agents.thinker_agent import ThinkerAgent

from neuromorph.agents.llm_backends.llm_backend import LLMBackend
from neuromorph.relationaldbs.database import Database
from neuromorph.vectordbs.vectorstore import VectorStore

import datetime

class Thinker:
    def __init__(self, llm_backend: LLMBackend = None, vector_db: VectorStore = None, relational_db: Database = None):
        self.agent = ThinkerAgent(backend=llm_backend, vector_db=vector_db, relational_db=relational_db)
        self.llm_backend = llm_backend
        self.vector_db = vector_db
        self.relational_db = relational_db

    def observe(self, observation: Observation) -> Thought:
        # store observation
        # think about observation
        # return thought
        observation_id = self.relational_db.log_observation(observation)
        thought_prompt = self.agent.build_prompt(observation)
        thought = self.llm_backend.get_completion(thought_prompt, system_prompt=self.agent.system_prompt)

        memory_content = f"In response to: '{observation.content}', I think: '{thought}'"
        memory = Memory(memory_id="-", memory=memory_content, created=str(datetime.datetime.now()), related_observation_ids=[observation_id], metadata={})
        memory_id = self.relational_db.log_memory(memory)
        memory.memory_id = memory_id
        memory_metadata = {
            "observation_id": observation_id,
            "thought": thought,
            "created": str(datetime.datetime.now())
        }
        self.vector_db.store_memory(memory.memory, memory_metadata)


        return thought