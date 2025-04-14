from openai import OpenAI

import os

class Agent:
    def __init__(self, name: str, description: str, openai_model: str = "gpt-4o"):

        if "OPENAI_API_KEY" in os.environ:
            self.openai_api_key = os.environ["OPENAI_API_KEY"]
        else:
            raise EnvironmentError("OPENAI_API_KEY not found in environment variables. Please set it before running the code.")

        self.name = name
        self.description = description
        self.system_prompt = ""
        self.oai_client = OpenAI(api_key=self.openai_api_key, model=openai_model)
        self.oai_model = openai_model

    def get_completion(self, message: str) -> str:
        messages = [
            {
                "role":"system",
                "content": self.system_prompt
            },
            {
                "role":"user",
                "content": message
            }
        ]
        response = self.oai_client.chat.completions.create(messages=messages, model=self.oai_model)
        return response.choices[0].message["content"]
