from autogen import ConversableAgent

class InnovatorProxy(ConversableAgent):
    name = "Innovator Proxy"
    description = """An agent that executes actions based on thoughts from another agent."""
    def __init__(self):
        super(InnovatorProxy, self).__init__(name=self.name, description=self.description, system_message=self.system_message, llm_config=None, human_input_mode="NEVER")

        