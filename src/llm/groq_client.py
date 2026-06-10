from groq import Groq 
from src.config.config import EnvVars


class GroqClient:
    """
    Generic Groq Client

    Responsibility:
    - Connect to Groq
    - Send prompts
    - Return text response

    It does NOT contain:
    - Loan logic
    - Drift logic
    - Business rules
    """

    def __init__(self):
        self.client = Groq(
            api_key=EnvVars.GROQ_API_KEY
        )

        self.model_name = EnvVars.GROQ_MODEL

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 100
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()