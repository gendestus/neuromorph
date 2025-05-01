from neuromorph.data_models.action import Action
from neuromorph.data_models.thought import Thought

class Doer:
    def __init__(self):
        pass

    def execute(self, thought: Thought) -> list[Action]:
        """
        Execute the given thought and return a list of actions.
        
        :param thought: The thought to be executed.
        :return: A list of actions resulting from the execution of the thought.
        """
        pass