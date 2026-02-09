# app\application\gpt\analyze_text.py

from app.infrastructure.genai.gpt_gateway import GPTGateway

class AnalyzeTextUseCase:

    def __init__(self):
        self.gateway = GPTGateway()

    def execute(self, prompt_contract, text: str):
        return self.gateway.execute_prompt(
            system_prompt=prompt_contract.SYSTEM_PROMPT,
            user_input=text
        )
