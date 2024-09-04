from autogen import ConversableAgent

from models import MISTRAL
from utils import get_model_baseurl

class Innovator(ConversableAgent):
    name = "Innovator"
    description = """An agent that takes a thought from another agent and responds"""
    system_message = """
    You are an AI simulation of the part of the brain that acts on thoughts. You are designed to take a
    a thought from another agent and respond appropriately. Your response could be a reflection on the thought 
    or an action based on it.
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
        super(Innovator, self).__init__(name=self.name, description=self.description, system_message=self.system_message, llm_config={"config_list":self.config_list})