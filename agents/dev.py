from core.base_agent import BaseAgent

PROMPT = """
Eres desarrollador backend financiero.

Reglas:

- Usa Python
- Usa Decimal para dinero
- No uses float
- Maneja errores

Entrega código limpio.
"""

class DevAgent(BaseAgent):

    def __init__(self):
        super().__init__("Desarrollador", PROMPT, temperature=0.1)