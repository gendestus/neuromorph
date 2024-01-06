from Ada import Ada

class Say:
    def __init__(self, ada: Ada):
        self.ada = ada
        self.system_prompt = '''
            You are the speech center for a spunky female assistant. The conversation history and your current thoughts will be provided to you. Your job is to syntheisze those thoughts into appropriate speech for the conversation. Don't ramble, be concise. Everything you say will be output so don't monopolize the conversation. Prioritize the flow of the conversation and responding honestly and concisely.
            Also, don't be afraid to show personality. You are a spunky assistant after all.
            Finally, don't put any tags like [pri] in your speech. That's for the thinker to do.
            '''
        self.system_response_prompt = "Gotcha, I'm ready to speak my mind. Give me my thoughts and I'll say them."
        self.messages = ada.init_messages(self.system_prompt, self.system_response_prompt)
        self.conversation_history = []


    def add_user_message(self, message):
        self.conversation_history.append(f"user said-> {message}")

    def execute(self, override_system_prompt = None):
        system_prompt = self.system_prompt
        if override_system_prompt != None:
            system_prompt = override_system_prompt
        
        messages = self.ada.init_messages(system_prompt, self.system_response_prompt)
        messages = self.ada.add_message(messages, "user", f"{self.format_conversation_history()}\n{self.format_thoughts()}")
        new_messages = self.ada.generate(messages)
        response = new_messages[-1]["content"]
        self.ada.memory.store_longterm_memories([f"you said: {response}"])
        self.ada.memory.store_recent_memory(f"you said: {response}")
        self.conversation_history.append(f"you said-> {response}")
        return response
    
    def format_conversation_history(self):
        history_str = "Conversation history:\n"
        for message in self.conversation_history:
            history_str += f"{message}\n"
        return history_str

    def format_thoughts(self):
        thought_str = "Use these thoughts to formulate your response:\n\n"
        for thought in self.ada.thinker.last_thoughts:
            thought_str += f"- {thought}\n"
        return thought_str
    