from .models.observation import Observation

class InnerMind:
    def __init__(self, num_thought_tracks: int = 1):
        '''
        InnerMind is a system that processes observations and memories.
        For on-prem local model deployments where you're really GPU limited, InnerMind will only use
        a single "thought track" at a time. I wanted to call it threads but I didn't want to overload and confuse
        that term. When using an API moderl service, you can have multiple thought tracks that will process thoughts
        in parallel.
        
        Observations is a queue that should take in data whenever
        '''
        self.observations = []
        self.num_thought_tracks = num_thought_tracks

    def observe(self, observation: Observation):
        self.observations.append(observation)
        return observation
    
    def introspect(self):
        '''
        This should be called in a loop to process observations and memories.
        The caller would be whatever is orchestrating the innermind. Like a notebook call or a script

        for now, we're going to assume num_thought_tracks is 1
        '''
        