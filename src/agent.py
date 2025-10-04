from dataclasses import dataclass
from llm import LLM
from prompts import agent_prompt

@dataclass
class Personality:
    openness: float # Imaginative, curious vs. Cautious, consistent
    conscientiousness: float # Organized, dependable vs. Easy-going, careless
    extraversion: float # Outgoing, energetic vs. Solitary, reserved
    agreeableness: float # Friendly, compassionate vs. Challenging, detached
    neuroticism: float # Sensitive, nervous vs. Secure, confident
    
    def __str__(self) -> str:
        """Return a detailed string representation of the personality traits."""
        
        def get_level(value: float) -> str:
            """Get the level description for a trait value."""
            if value < 0.2:
                return "very low"
            elif value < 0.4:
                return "low"
            elif value < 0.6:
                return "moderate"
            elif value < 0.8:
                return "high"
            else:
                return "very high"
        
        def describe_openness(value: float) -> str:
            level = get_level(value)
            if value < 0.3:
                return (f"With {level} openness ({value:.2f}), this person tends to be cautious and prefers "
                       f"routine and familiar experiences. They are practical and traditional in their approach, "
                       f"valuing consistency over novelty.")
            elif value < 0.7:
                return (f"With {level} openness ({value:.2f}), this person balances practicality with curiosity. "
                       f"They appreciate both routine and new experiences, showing moderate interest in abstract "
                       f"ideas and creative pursuits.")
            else:
                return (f"With {level} openness ({value:.2f}), this person is highly imaginative and intellectually "
                       f"curious. They eagerly embrace new experiences, enjoy abstract thinking, and are drawn to "
                       f"creative and artistic pursuits.")
        
        def describe_conscientiousness(value: float) -> str:
            level = get_level(value)
            if value < 0.3:
                return (f"With {level} conscientiousness ({value:.2f}), this person is spontaneous and easy-going, "
                       f"preferring flexibility over strict planning. They may struggle with organization and "
                       f"tend to be more casual about deadlines and responsibilities.")
            elif value < 0.7:
                return (f"With {level} conscientiousness ({value:.2f}), this person shows a balanced approach to "
                       f"organization and spontaneity. They can be responsible when needed but also know how to "
                       f"relax and be flexible.")
            else:
                return (f"With {level} conscientiousness ({value:.2f}), this person is highly organized, dependable, "
                       f"and disciplined. They plan ahead, pay attention to details, and take their obligations "
                       f"seriously, consistently meeting their goals.")
        
        def describe_extraversion(value: float) -> str:
            level = get_level(value)
            if value < 0.3:
                return (f"With {level} extraversion ({value:.2f}), this person is introverted and reserved, preferring "
                       f"solitude or small groups over large social gatherings. They recharge through quiet time alone "
                       f"and tend to be more reflective and reserved in social settings.")
            elif value < 0.7:
                return (f"With {level} extraversion ({value:.2f}), this person is an ambivert, comfortable in both "
                       f"social and solitary settings. They enjoy socializing but also value their alone time, "
                       f"adapting well to various social situations.")
            else:
                return (f"With {level} extraversion ({value:.2f}), this person is highly outgoing and energetic in "
                       f"social situations. They thrive on interaction with others, seek out social stimulation, "
                       f"and feel energized by being around people.")
        
        def describe_agreeableness(value: float) -> str:
            level = get_level(value)
            if value < 0.3:
                return (f"With {level} agreeableness ({value:.2f}), this person is direct and analytical, valuing "
                       f"truth over tact. They are willing to challenge others' ideas and may prioritize logic "
                       f"over harmony, sometimes appearing detached or competitive.")
            elif value < 0.7:
                return (f"With {level} agreeableness ({value:.2f}), this person balances compassion with assertiveness. "
                       f"They can be cooperative and friendly while also standing their ground when necessary, "
                       f"showing both empathy and healthy skepticism.")
            else:
                return (f"With {level} agreeableness ({value:.2f}), this person is warm, compassionate, and highly "
                       f"cooperative. They prioritize harmony in relationships, are quick to help others, and "
                       f"naturally empathize with people's feelings and perspectives.")
        
        def describe_neuroticism(value: float) -> str:
            level = get_level(value)
            if value < 0.3:
                return (f"With {level} neuroticism ({value:.2f}), this person is emotionally stable, calm, and resilient. "
                       f"They handle stress well, remain composed under pressure, and rarely experience intense "
                       f"negative emotions or anxiety.")
            elif value < 0.7:
                return (f"With {level} neuroticism ({value:.2f}), this person experiences a typical range of emotional "
                       f"responses. They can feel stressed or anxious at times but generally maintain emotional "
                       f"balance and recover reasonably well from setbacks.")
            else:
                return (f"With {level} neuroticism ({value:.2f}), this person is emotionally sensitive and prone to "
                       f"experiencing stress, anxiety, or worry. They feel emotions intensely and may be more "
                       f"vulnerable to negative moods and self-doubt.")
        
        # Build the personality description
        lines = [
            "=" * 80,
            "PERSONALITY PROFILE",
            "=" * 80,
            "",
            describe_openness(self.openness),
            "",
            describe_conscientiousness(self.conscientiousness),
            "",
            describe_extraversion(self.extraversion),
            "",
            describe_agreeableness(self.agreeableness),
            "",
            describe_neuroticism(self.neuroticism),
            "",
            "=" * 80
        ]
        
        return "\n".join(lines)

@dataclass
class AgentProfile:
    name: str
    backstory: str
    personality: Personality
    core_values: list
    goals: list

@dataclass
class Memory:
    timestamp: int # In ticks
    type: str
    content: str

@dataclass
class AgentState:
    mood: str
    location: str
    short_term_goals: list
    relationships: dict
    memories: list[Memory]

class Agent:
    def __init__(self, llm: LLM, profile: AgentProfile, starting_state: AgentState = None):
        self.profile = profile
        self.state = starting_state if starting_state else AgentState(
            mood="neutral",
            location="home",
            short_term_goals=[],
            relationships={},
            memories=[]
        )
        self.llm = llm
    
    def perceive(self, observation: str):
        new_memory = Memory(
            timestamp=len(self.state.memories),
            type="observation",
            content=observation
        )

        self.state.memories.append(new_memory)
    
    def generate_prompt(self, current_observation: str) -> str:
        prompt = agent_prompt.format(
            name=self.profile.name,
            backstory=self.profile.backstory,
            personality=str(self.profile.personality),
            core_values=", ".join(self.profile.core_values),
            long_term_goals=", ".join(self.profile.goals),
            current_mood=self.state.mood,
            short_term_goals=", ".join(self.state.short_term_goals),
            relationships=str(self.state.relationships),
            recent_memories="\n".join(
                f"[{m.timestamp}] ({m.type}) {m.content}" for m in self.state.memories
            ),
            current_location=self.state.location,
            current_observation=current_observation
        )
        return prompt