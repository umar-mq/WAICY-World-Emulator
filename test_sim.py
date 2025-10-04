# test_simulation.py

import os
from dotenv import load_dotenv
load_dotenv()
from src.agent import Agent, AgentProfile, Personality, AgentState
from src.llm import LLM

# --- 1. SETUP THE ENVIRONMENT ---
# Make sure to set your OPENAI_API_KEY as an environment variable
# For example, in your terminal: export OPENAI_API_KEY='your_key_here'
llm_client = LLM(
    model="gemini-2.5-flash",
    api_key=os.getenv("LLM_API_KEY"),
    temperature=0.7
)

# --- 2. DEFINE AN AGENT ---
alex_profile = AgentProfile(
    name="Alex",
    backstory="A driven data analyst who recently joined a competitive tech firm. Alex is eager to impress but suffers from impostor syndrome, making them cautious in social interactions.",
    personality=Personality(
        openness=0.7,          # Curious about new data, but not wildly creative
        conscientiousness=0.9, # Highly organized and dependable
        extraversion=0.2,      # Introverted, prefers focused work over socializing
        agreeableness=0.4,     # Can be skeptical and direct, values correctness
        neuroticism=0.8        # Prone to anxiety and stress about performance
    ),
    core_values=["Excellence", "Integrity", "Growth"],
    long_term_goals=[
        "Become a senior analyst within two years",
        "Gain the respect of my manager, Chloe",
        "Contribute to a major project"
    ]
)

alex_initial_state = AgentState(
    mood="Anxious",
    location="Office Cafe",
    short_term_goals=["Get coffee and start my daily report"]
)

# --- 3. CREATE THE AGENT INSTANCE ---
alex = Agent(
    llm=llm_client,
    profile=alex_profile,
    starting_state=alex_initial_state
)

# --- 4. DEFINE THE SCENARIO (THE OBSERVATION) ---
# This is the "input" to the agent's senses for this tick.
current_observation = (
    "The cafe is moderately busy. "
    "Your friendly but competitive colleague, Ben, is waving at you from a table. "
    "Your demanding boss, Chloe, is near the coffee machine, looking stressed."
)

# --- 5. RUN THE SIMULATION TICK ---
print("=" * 50)
print(f"AGENT: {alex.profile.name}")
print(f"LOCATION: {alex.state.location} | MOOD: {alex.state.mood}")
print("-" * 50)
print(f"OBSERVATION:\n{current_observation}")
print("=" * 50)
print("\n... Alex is thinking ...\n")

# The magic happens here! Alex perceives, thinks, and decides.
decision = alex.decide_action(current_observation)

# --- 6. DISPLAY THE RESULT ---
if decision:
    print("🧠 ALEX'S THOUGHT:")
    print(f"   \"{decision['thought']}\"")
    print("\n🎬 ALEX'S ACTION:")
    action = decision['action']
    print(f"   TYPE: {action['type']}")
    print(f"   DETAILS: {action['details']}")
    print("\n" + "=" * 50)
    print("\nAGENT STATE AFTER ACTION:")
    # Show the last two memories (the observation and the action)
    for mem in alex.state.memories[-2:]:
        print(f"  - [T-{mem.timestamp}] ({mem.type}) {mem.content}")
else:
    print("Alex failed to make a decision.")