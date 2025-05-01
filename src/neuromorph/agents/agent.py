from neuromorph.agents.llm_backends.llm_backend import LLMBackend

class Agent:
    
    def __init__(self, backend: LLMBackend, name: str = "Agent"):
        self.backend = backend
        self.name = name