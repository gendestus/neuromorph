# Introducing Ada, the world's first neuromorphic assistant

Neuro = Brain

Morph = Shape

Meet Ada. She's an AI assistant that has opinions, argues with passion, and is eager to learn about the world.

## Wait, what?
I wanted to see what happened when you take a normal large language model and structure it similarly to the human brain. 
There's an inner monologue, a speech center, and memory which work together to create identity. I was surprised to find that
the separation of responsibility alone was enough to create some emergent behavior including a distinct personality, increased 
creativity, and long term desires. I figured I would open source it to get more eyes on it.

## Structure
3 Core Components
- **Thinker**: This is the agent's inner monologue. The Thinker receives input (user messages, sensor readings, etc) and generates "thoughts" and creates memories
- **Doer**: This is the action taker that processes the Thinker's thoughts and executes actions based on them. Currently only supports outputting text
- **Memory**: This automatically handles the storage and retrieval of 3 different types of memories. It uses ChromaDB as a backend and is loosely based on the Simulacra paper memory structure here: https://arxiv.org/pdf/2304.03442.pdf

## Memory Types
- **Priority Memories**: These define the identity of the agent. All priority memories are supplied to the thinker for each generation. Think of them like RoboCop's Prime Directives.
- **Relevant Memories**: These are memories stored in a vector database and are retrieved based on the circumstances of the current generation task. 
- **Recent Memories**: These are memories stored in a First-In-First-Out list that allow the agent to keep track of the current situation.

## A Note About Context Windows
The memory system is doing a lot of heavy lifting for the agent's situational awareness. Conversations are not maintained in the context window like normal LLM interactions. In fact, every generation starts with a clean message stack. 

## Hardware Requirements
Until ollama is implemented, core functionality is really only possible with an RTX GPU with at least 16gb of vram, 24gb preferred. I'm getting 1-2 second inference times on a single RTX 4090 with 24gb with half-precision (on by default) but your mileage may vary.

## Supported Models
- Mistral7B
- Dolphin

## Future Plans
- ollama backend
- curated models for specific tasks
- Introspection loop
- Reinforcement learning