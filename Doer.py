from Ada import Ada
from .Actions import Say

class Doer:
    def __init__(self, ada: Ada):
        self.ada = ada
        self.say = Say.Say(ada)
    
    def do(self):
        # For now, the only action we have is Say
        # Eventually, this class will take the current state and make a decision about what to do next
        return self.say.execute()