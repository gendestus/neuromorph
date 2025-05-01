from neuromorph.agents.llm_backends.llm_backend import LLMBackend

import os
from openai import OpenAI

class OpenAIBackend(LLMBackend):
    API_KEY_ENV_VAR = "OPENAI_API_KEY"

    def __init__(self, default_model: str = "gpt-4o"):
        if OpenAIBackend.API_KEY_ENV_VAR not in os.environ:
            raise ValueError(f"Environment variable {OpenAIBackend.API_KEY_ENV_VAR} not set.")
        
        self.api_key = os.environ[OpenAIBackend.API_KEY_ENV_VAR]
        self.default_model = default_model

    def get_completion(self, prompt: str, system_prompt: str|None = None) -> str:
        """
        Get the completion from the OpenAI API for a given prompt.
        """
        openai = OpenAI(api_key=self.api_key)
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = openai.chat.completions.create(messages=messages, model=self.default_model)
        return response.choices[0].message.content.strip()