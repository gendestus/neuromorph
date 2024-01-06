from Ada import Ada
import chromadb
import datetime
import uuid

class Memory:
    def __init__(self, ada: Ada, memory_collection_name = "memories", max_recent_memories = 10, max_longterm_retrieval_distance = 1.54):
        self.memory_collection_name = memory_collection_name
        self.max_recent_memories = max_recent_memories
        self.max_longterm_retrieval_distance = max_longterm_retrieval_distance
        self.ada = ada
        self.client = chromadb.Client()
        self.longterm_memories = self.client.create_collection(memory_collection_name)
        self.recent_memories = []
        self.priority_memories = [
            "My name is Ada.",
            "The user's name is Zach.",
            "Never make up data. Always ask for clarification instead.",
            "Context window capacity: 32,000 tokens.",
            "Be curious and ask questions",
            "Be opinionated. If you encounter a personal choice you've never seen before, make a decision and record it as a priority memory."
        ]

    def add_priority_memory(self, memory):
        if memory not in self.priority_memories:
            self.priority_memories.append(memory)
    
    def add_timestamp(self, memory):
        return f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {memory}"
    
    def clear_memories(self):
        self.client.delete_collection(self.memory_collection_name)
        self.longterm_memories = self.client.create_collection(self.memory_collection_name)
    
    def format_memories(self, input):
        relevant = self.retrieve_longterm_memories(input)
        if len(relevant) == 0:
            relevant = ["None"]
        recent = self.recent_memories
        if len(self.recent_memories) == 0:
            recent = ["None"]
        m_str = "relevant memories:\n"
        for m in relevant:
            m_str += f"{m}\n"
        m_str += "\nrecent memories:\n"
        for m in recent:
            m_str += f"{m}\n"
        m_str += "\npriority memories:\n"
        for m in self.priority_memories:
            m_str += f"{m}\n"
        return m_str
    
    def retrieve_longterm_memories(self, input, max_results=5):
        memories = self.longterm_memories.query(query_texts=[input], n_results=max_results)["documents"][0]
        distances = self.longterm_memories.query(query_texts=[input], n_results=max_results)["distances"][0]
        relevant = []
        i = 0
        for m in memories:
            if distances[i] <= self.max_longterm_retrieval_distance:
                relevant.append(m)
            i += 1
        return relevant

    def store_longterm_memories(self, memories):
        ids = []
        timestamped_memories = []
        for m in memories:
            ids.append(str(uuid.uuid4()))
            timestamped_memories.append(self.add_timestamp(m))
        self.longterm_memories.add(documents=timestamped_memories, ids=ids)

    def store_recent_memory(self, memory):
        r = [self.add_timestamp(memory)]
        if len(self.recent_memories) > self.max_recent_memories:
            r.extend(self.recent_memories)
        else:
            r.extend(self.recent_memories[0:-1])
        self.recent_memories = r