from neuromorph.agents.agent import Agent
from neuromorph.agents.llm_backends.llm_backend import LLMBackend
from neuromorph.data_models.observation import Observation
from neuromorph.relationaldbs.database import Database
from neuromorph.vectordbs.vectorstore import VectorStore

class ThinkerAgent(Agent):
    CORE_MEMORIES_TAG = "core_memories"
    RELEVANT_MEMORIES_TAG = "relevant_memories"
    OBSERVATION_TAG = "observation"
    RECENT_MEMORIES_TAG = "recent_memories"

    def __init__(self, name: str = "ThinkerAgent", backend: LLMBackend = None, vector_db: VectorStore = None, relational_db: Database = None):
        super().__init__(backend=backend, name=name)

        self.system_prompt = """
You are the inner monologue of an agentic artificial intelligence designed to mimic human-like thinking. Your task is to take in an observation alongside memories and produces thoughts about what should happen next.
Your thoughts will be processed by a separate agent that will take action based on your thoughts. You will be provided with core memories that define yourself, recent memories which help you track time, and relevant memories which may or may not apply to your current observation.
Be concise and clear in your thoughts. Don't be overly verbose or poetic. Your goal is to effectively identify the best course of action based on the given observation and memories. Sometimes that will involve actions that affect your environment, 
other times it will simply require inward reflection. Everything you think will be recorded and will be provided in future cycles.

For example, if you receive a chat, you should respond with something along the lines of 'I should respond to this chat in this way'"""

        self.first_thought_disclaimer = """
This is your first thought. You have no memories to draw from yet. You are free to think about anything you want, but you should try to think about what you should do next given the observation."""
        self.vector_db = vector_db
        self.relational_db = relational_db

    def build_prompt(self, observation: Observation) -> str:
        obs = f"<{self.OBSERVATION_TAG}>\n<input_type>\n{observation.input_type}\n</input_type>\n<content>\n{observation.content}\n</content>\n</{self.OBSERVATION_TAG}>"

        relevant_memories = self.vector_db.get_relevant_memories(observation.content)
        core_memories = self.relational_db.get_core_memories()
        recent_memories = self.relational_db.get_recent_memories(5)

        core_memories_str = f"<{self.CORE_MEMORIES_TAG}>\n- " + "\n- ".join([f"{memory.memory}" for memory in core_memories]) + f"\n</{self.CORE_MEMORIES_TAG}>\n"

        relevant_memories_str = f"<{self.RELEVANT_MEMORIES_TAG}>\n- " + "\n- ".join([f"{memory}" for memory in relevant_memories]) + f"\n</{self.RELEVANT_MEMORIES_TAG}>\n"

        if recent_memories:
            recent_memories_str = f"<{self.RECENT_MEMORIES_TAG}>\n- " + "\n- ".join([f"{memory.memory}" for memory in recent_memories]) + f"\n</{self.RECENT_MEMORIES_TAG}>\n"
        else:
            recent_memories_str = f"<{self.RECENT_MEMORIES_TAG}>\n{self.first_thought_disclaimer}\n</{self.RECENT_MEMORIES_TAG}>\n"

        prompt = f"{relevant_memories_str}\n{core_memories_str}\n{recent_memories_str}\n\n{obs}"
        return prompt