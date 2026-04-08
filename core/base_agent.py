from langchain_anthropic import ChatAnthropic
from config.settings import Settings

class BaseAgent:

    def __init__(self, name, prompt, temperature=0.1):
        self.name = name
        self.prompt = prompt

        self.llm = ChatAnthropic(
            model=Settings.MODEL,
            anthropic_api_key=Settings.ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=Settings.MAX_TOKENS
        )

    def run(self, input_text):

        print(f"\n🧠 [{self.name}] ejecutando...\n")

        full_prompt = f"{self.prompt}\n\nINPUT:\n{input_text}"

        response = self.llm.invoke(full_prompt)

        return response.content