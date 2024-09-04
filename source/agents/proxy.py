from autogen import ConversableAgent

class Proxy(ConversableAgent):
    def __init__(self):
        super(Proxy, self).__init__(name="proxy", description="A proxy agent", human_input_mode="NEVER", llm_config=None)