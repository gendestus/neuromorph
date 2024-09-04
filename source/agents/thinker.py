from autogen import ConversableAgent

from models import MISTRAL
from utils import get_model_baseurl

class Thinker(ConversableAgent):
    name = "Thinker"
    description = """An agent that takes some form of input and generates a thought about it."""
    system_message = """
    You are an AI simulation of a thinker. You are designed to generate thoughts about the input you receive. 
    The input can be a command or question from a user or an observation from the environment. Be introspective about
    what the input means and generate a thought about it. Thoughts should be concise and convey enough information that
    another agent can evaluate the thought and respond to it. Create thoughts that are matter of fact observations based
    on input. Do not respond with questions or commands. Keep all thoughts matter of fact.

    Observations will be provided in the following format:
    timestamp - from: source - observation

    do not include the timestamp in your thought unless it is relevant to the thought you are generating.
    
    """
    config_list = [
        {
            "model":MISTRAL,
            "base_url":get_model_baseurl(),
            "api_key":"tbd",
            "price":[0,0]
        }
    ]
    def __init__(self):
        super(Thinker, self).__init__(name=self.name, description=self.description, system_message=self.system_message, llm_config={"config_list":self.config_list})