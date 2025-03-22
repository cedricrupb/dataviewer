"""Language model interface and implementations."""
from abc import ABC, abstractmethod

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class LLMInterface(ABC):
    @abstractmethod
    def generate_code(self, prompt: str, system_message: str) -> str:
        """Generate code based on prompt."""
        pass

class Claude(LLMInterface):
    def __init__(self, api_key: str):
        if Anthropic is None:
            raise ImportError("Anthropic is not installed. Please install it using 'pip install anthropic'.")
        self.client = Anthropic(api_key=api_key)
    
    def generate_code(self, prompt: str, system_message: str) -> str:
        response = self.client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1500,
            temperature=0,
            system=system_message,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class GPT4(LLMInterface):
    def __init__(self, api_key: str):
        if OpenAI is None:
            raise ImportError("OpenAI is not installed. Please install it using 'pip install openai'.")
        self.client = OpenAI(api_key=api_key)
    
    def generate_code(self, prompt: str, system_message: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content 