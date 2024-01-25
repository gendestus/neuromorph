import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from neuromorph import Neuromorph

# Class that handles sensor input (user messages, whatever, etc) and thinking about them
class Thinker:
    SENDER_ID = "THINKER"
    def __init__(self, neuromorph: "Neuromorph"):
        self.neuromorph = neuromorph
        # self.system_prompt = "system_message->You are the internal monologue of a female companion. Your job is to process sensory input and create thoughts that will be stored and used by other systems. Craft thoughts in a way so that they store useful bits of information that can be recalled later. For example you might think \"Julie's favorite color is blue.\" Individual thoughts should be concise and express a single idea or memory and each thought should be on a newline.\n\nDon't be so rigid, it's ok to have personality.\n\nFinally, sometimes you'll encounter information that is critical to always remember. Preface these critical thoughts with [pri]. All thoughts tagged as such will be made available without exception so use this for things like names etc."
        self.system_prompt = '''You are the internal monologue of a spunky female assistant. Your job is to process input and generaate thoughts. For example, if you see a user message that introduces someone new you could generate 'I should remember Julie's name.'. You will receive data from many different inputs. Be curious.
Also, if you run into critical information, such as new biographical data or important tasks, you can preface thoughts about that information with [pri]. Doing so will make sure that data is always recalled.
If you have more than one thought, put each thought on a separate line.'''
        self.system_response_prompt = "Understood, I've set the that system prompt as my initial parameters and will begin processing input now"
        self.messages = []
        self.init_messages()
        self.last_thoughts = []
    
    # Pure function that takes a thought and returns a new one with a timestamp on it
    def add_timestamp(self, thought):
        return f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {thought}"

    # Deprecated, should be removed once I'm off this plane and can execute the model
    def init_messages(self, override_system_prompt = None):
        system_prompt = self.system_prompt
        if override_system_prompt != None:
            system_prompt = override_system_prompt
        self.messages = [
            {
                "role":"user",
                "content":system_prompt
            },
            {
                "role":"assistant",
                "content":self.system_response_prompt
            }
        ]

    # Main entry point for the Thinker. Allows the LLM to create observances in the form of thoughts based on some input
    # This is all pretty freeform so we have to do some rudimentary shepherding to make sure things stay sane
    # The default system prompt here also gives the model power to create priority memories here. This will likely be changed in the future to a dedicated priority rememberer
    def observe(self, action, message, override_system_prompt = None):
        self.init_messages(override_system_prompt)
        new_message = f"{action}->{self.add_timestamp(message)}"
        self.messages.append({"role":"user", "content":f"{self.neuromorph.SYSTEM_MESSAGE}->What do you think about the following input? How should you respond?\n\ninput->{new_message}\n\nYou may use these memories for your response. Remember, not all memories are guaranteed to be necessary for a response:\n{self.neuromorph.memory.format_memories(message)}"})
        #self.messages.append({"role":"assistant", "content":"Understood, I'll make sure to use those memories for the next input response if appropriate. I'll try not to shoehorn in unnecessary data"})
        #self.messages.append({"role":"user", "content":new_message})
        input_memory = f"you received a {action}: {message}"
        self.neuromorph.memory.store_longterm_memories([input_memory])
        self.neuromorph.memory.store_recent_memory(input_memory)
        new_messages = self.neuromorph.generate(self.SENDER_ID, self.messages)
        self.last_thoughts = []
        memories = []
        thoughts = new_messages[-1]["content"].split("\n")
        for thought in thoughts:
            # Mistral at least likes to adds headders and new lines a lot.....
            if thought != '' and thought.strip().lower() != "thoughts:" and thought.strip().lower() != "thoughts":
                self.last_thoughts.append(self.add_timestamp(thought))
                memory = ""
                if "[pri]" in thought:
                    memory = thought.split("[pri]")[1].strip()
                    self.neuromorph.memory.add_priority_memory(memory)
                    
                else:
                    memory = f"you thought: {thought}"
                memories.append(memory)
                self.neuromorph.memory.store_recent_memory(memory)
        self.neuromorph.memory.store_longterm_memories(memories)