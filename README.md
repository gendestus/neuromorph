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

## Supported Models
- Mistral7B
- Dolphin

## Future Plans
- ollama backend
- curated models for specific tasks
- Introspection loop
- Reinforcement learning