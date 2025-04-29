class LLMBackend:

    def get_completion(self, prompt: str, system_prompt: str|None = None) -> str:
        """
        Get the completion from the LLM for a given prompt.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")