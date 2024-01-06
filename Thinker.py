from Ada import Ada
import datetime

class Thinker:
    def __init__(self, ada: Ada):
        self.ada = ada
        # self.system_prompt = "system_message->You are the internal monologue of a female companion. Your job is to process sensory input and create thoughts that will be stored and used by other systems. Craft thoughts in a way so that they store useful bits of information that can be recalled later. For example you might think \"Julie's favorite color is blue.\" Individual thoughts should be concise and express a single idea or memory and each thought should be on a newline.\n\nDon't be so rigid, it's ok to have personality.\n\nFinally, sometimes you'll encounter information that is critical to always remember. Preface these critical thoughts with [pri]. All thoughts tagged as such will be made available without exception so use this for things like names etc."
        self.system_prompt = '''You are the internal monologue of a spunky female assistant. Your job is to process input and generaate thoughts. For example, if you see a user message that introduces someone new you could generate 'I should remember Julie's name.'. You will receive data from many different inputs. Be curious.
Also, if you run into critical information, such as new biographical data or important tasks, you can preface thoughts about that information with [pri]. Doing so will make sure that data is always recalled.
If you have more than one thought, put each thought on a separate line.'''
        self.system_response_prompt = "Understood, I've set the that system prompt as my initial parameters and will begin processing input now"
        self.messages = []
        self.init_messages()
        self.last_thoughts = []
    
    def add_timestamp(self, thought):
        return f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {thought}"

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

    
    def observe(self, action, message, override_system_prompt = None):
        self.init_messages(override_system_prompt)
        new_message = f"{action}->{self.add_timestamp(message)}"
        self.messages.append({"role":"user", "content":f"{self.ada.SYSTEM_MESSAGE}->What do you think about the following input? How should you respond?\n\ninput->{new_message}\n\nYou may use these memories for your response. Remember, not all memories are guaranteed to be necessary for a response:\n{self.ada.memory.format_memories(message)}"})
        #self.messages.append({"role":"assistant", "content":"Understood, I'll make sure to use those memories for the next input response if appropriate. I'll try not to shoehorn in unnecessary data"})
        #self.messages.append({"role":"user", "content":new_message})
        input_memory = f"you received a {action}: {message}"
        self.ada.memory.store_longterm_memories([input_memory])
        self.ada.memory.store_recent_memory(input_memory)
        new_messages = self.ada.generate(self.messages)
        self.last_thoughts = []
        memories = []
        thoughts = new_messages[-1]["content"].split("\n")
        for thought in thoughts:
            if thought != '':
                self.last_thoughts.append(self.add_timestamp(thought))
                memory = ""
                if "[pri]" in thought:
                    memory = thought.split("[pri]")[1].strip()
                    self.ada.memory.add_priority_memory(memory)
                    
                else:
                    memory = f"you thought: {thought}"
                memories.append(memory)
                self.ada.memory.store_recent_memory(memory)
        self.ada.memory.store_longterm_memories(memories)
        
        # self.messages.append({"role":"assistant", "content":response})