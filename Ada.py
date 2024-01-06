import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .Memory import Memory
from .Thinker import Thinker
from .Doer import Doer

class Ada:
    MISTRAL7B = "mistralai/Mistral-7B-Instruct-v0.2"
    DOLPHIN = "cognitivecomputations/dolphin-2.6-mistral-7b"

    def __init__(self, model_name, torch_type, display_thoughts = False):
        self.model_name = model_name
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch_type)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if model_name == Ada.DOLPHIN:
            self.tokenizer.chat_template = "{% for message in messages %}{{'<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n'}}{% endfor %}{{'<|im_start|> assistant\n'}}"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
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
        

        self.SYSTEM_MESSAGE = "system_message"
        self.USER_MESSAGE = "user_message"
    
    def add_message(self, messages, role, content):
        new_messages = messages.copy()  
        new_messages.append({"role":role, "content":content})
        return new_messages


    def init_messages(self, system_prompt, system_response_prompt):
        messages = [
            {
                "role":"user",
                "content":system_prompt
            },
            {
                "role":"assistant",
                "content":system_response_prompt
            }
        ]
        return messages

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

    def generate(self, messages):
        encodings = self.tokenizer.apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodings.to(self.device)
        self.model.to(self.device)
        generated_ids = self.model.generate(model_inputs, max_new_tokens=1000, do_sample=True, **self.model_config)
        decoded = self.tokenizer.batch_decode(generated_ids)
        if self.model_name == Ada.DOLPHIN:
            response = self.get_chatml_response(decoded[0])
        else:
            response = self.get_mistral_response(decoded[0])
        new_messages = messages.copy()
        new_messages.append({"role":"assistant", "content":response})
        return new_messages
    
    def get_chatml_response(self, decoded_tokens):
        r_count = decoded_tokens.count("<|im_end|>")
        response = decoded_tokens.split("<|im_end|>")[r_count-1].strip()[25:]
        return response
    def get_mistral_response(self, decoded_tokens):
        r_count = decoded_tokens.count("[/INST]")
        response = decoded_tokens.split("[/INST]")[r_count][0:-4].strip()
        return response
        
    

    