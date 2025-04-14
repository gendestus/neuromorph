from agent import Agent

class Thinker(Agent):
    def __init__(self):
        super().__init__(name="Thinker", description="A system that processes observations and memories.")
        self.system_prompt = """
        You are a system that processes observations and memories.
        You will be given observations and memories to process alongside potentially relevant information
        based on past performance. Memories can be normal memories or core memories.
        Core memories define who you are and how you should behave and persist over time. Normal memories may be
        the result of an observation or a thought based in introspection. All responses should be in first person,
        such as 'I think' or 'I feel'.
        Your job is to process these observations and memories and return a response that reflects your understanding
        
        The output of the thoughts will get stored in a vector store to be used for future reference
        """

    def think(self, memory: str, core_memories: list, relevant_info: list) -> str:
        formatted_core_memories = "\n".join([f"- {memory}" for memory in core_memories])
        formatted_relevant_info = "\n".join([f"- {info}" for info in relevant_info])
        
        message = f"""
        Core Memories:
        {formatted_core_memories}

        Potentially Relevant Information:
        {formatted_relevant_info}

        Memory:
        {memory}"""

        response = self.get_completion(message)
        return response    