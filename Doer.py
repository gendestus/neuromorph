from Ada import Ada
from .Actions import Say

# The part of the brain that takes recent thoughts and decides if and what it should do with them
# Right now, all it can do is output text
# To make the neuromorph interesting, I'll have to add new actions and figure out some way to switch them
# Probably another model call....
class Doer:
    def __init__(self, ada: Ada):
        self.ada = ada
        self.say = Say.Say(ada)
    
    def do(self):
        # For now, the only action we have is Say
        # Eventually, this class will take the current state and make a decision about what to do next
        return self.say.execute()