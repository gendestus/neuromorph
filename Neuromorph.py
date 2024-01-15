import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .Memory import Memory
from .Thinker import Thinker
from .Doer import Doer

# Main Entrypoint for the neuromorphic agent
class Neuromorph:
    # The currently supported model backends
    #TODO: add support for ollama
    MISTRAL7B = "mistralai/Mistral-7B-Instruct-v0.2"
    DOLPHIN = "cognitivecomputations/dolphin-2.6-mistral-7b"

    # Upon creation, the main class will load the desired model into memory and initialize the component parts of the brain
    # torch type will default to half precision because that's what works with mistral on consumer grade gpus for now
    # display_thoughts defaults to off because text output gets real messy with it on
    def __init__(self, model_name, agent_name = "Ada", torch_type = torch.float16, display_thoughts = False):
        if not agent_name.isalpha():
            raise Exception("agent_name must be alphabetic")
        self.agent_name = agent_name.capitalize()
        self.model_name = model_name
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch_type)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # AFAIK Dolphin's ChatML format is not automatic with torch's tokenizers
        if model_name == Neuromorph.DOLPHIN:
            self.tokenizer.chat_template = "{% for message in messages %}{{'<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n'}}{% endfor %}{{'<|im_start|> assistant\n'}}"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cpu":
            #TODO: make this a warning or something
            print("watch out! torch device set to cpu which is not fully implemented. Stuff will break.")

        # Config copied from the LLM arena thing
        # URL: 
        self.model_config = {
            "epsilon_cutoff": 1.49,
            "eta_cutoff": 10.42,
            "repetition_penalty": 1.17,
            "temperature": 1.31,
            "top_k": 49,
            "top_p": 0.14,
            "pad_token_id": self.tokenizer.eos_token_id
        }

        self.display_thoughts = display_thoughts

        # Init parts of the brain!!!!
        self.memory = Memory(self)
        self.thinker = Thinker(self)
        self.doer = Doer(self)
        
        # These are tags that get slapped on all messages to the thinker
        # eventually will capture all sorts of sensor input
        self.SYSTEM_MESSAGE = "system_message"
        self.USER_MESSAGE = "user_message"
    
    # Pure function that takes a message list and returns a new one with a new message added
    def add_message(self, messages, role, content):
        new_messages = messages.copy()  
        new_messages.append({"role":role, "content":content})
        return new_messages

    # Pure function that returns a new blank message list with a system prompt and an optional system response prompt
    def init_messages(self, system_prompt, system_response_prompt = None):
        messages = [
            {
                "role":"user",
                "content":system_prompt
            }
        ]
        if system_response_prompt is not None:
            messages = self.add_message(messages, "assistant", system_response_prompt)
        return messages

    # Method for interacting with the neuromorph
    # Will pass the input, whatever it is, to the thinker and kick off the response pipeline
    def interface(self, action, message):
        if action == self.USER_MESSAGE:
            self.doer.say.add_user_message(message)
        self.thinker.observe(action, message)
        if self.display_thoughts:
            for thought in self.thinker.last_thoughts:
                print(thought)
        response = self.doer.do()
        r = {
            "response":response,
            "thoughts":self.thinker.last_thoughts
        }
        return r

    # Method for interacting with the model
    # Handles passing in the messages in the correct format and returning the results
    def generate(self, messages):
        encodings = self.tokenizer.apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodings.to(self.device)
        self.model.to(self.device)
        generated_ids = self.model.generate(model_inputs, max_new_tokens=1000, do_sample=True, **self.model_config)
        decoded = self.tokenizer.batch_decode(generated_ids)
        if self.model_name == Neuromorph.DOLPHIN:
            response = self.get_chatml_response(decoded[0])
        else:
            response = self.get_mistral_response(decoded[0])
        new_messages = messages.copy()
        new_messages.append({"role":"assistant", "content":response})
        return new_messages
    
    # Extracts the last assistant response from decoded tokens in the ChatML format
    def get_chatml_response(self, decoded_tokens):
        r_count = decoded_tokens.count("<|im_end|>")
        response = decoded_tokens.split("<|im_end|>")[r_count-1].strip()[25:]
        return response
    
    # Extracts the last assistant response from decoded tokens in the Mistral format
    def get_mistral_response(self, decoded_tokens):
        r_count = decoded_tokens.count("[/INST]")
        response = decoded_tokens.split("[/INST]")[r_count][0:-4].strip()
        return response
        
    

    