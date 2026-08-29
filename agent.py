from strands import Agent

# Bare-bones orchestrator — no tools wired in yet
agent = Agent()

# Simple test prompt to confirm it's alive
response = agent("Hello! Can you confirm you're working?")
print(response)