from openai import OpenAI

class LLM:
    def __init__(self, model: str = "gemini-2.5-flash", api_key: str = None, temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )


    def generate_single_turn(self, prompt: str, system: str = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )

        return response.choices[0].message.content
    
    def generate_multi_turn(self, turns: list, system: str = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        for i, msg in enumerate(turns):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": msg})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return response.choices[0].message.content
    