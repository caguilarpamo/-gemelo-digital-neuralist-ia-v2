from core.base_agent import BaseAgent

PROMPT = """
Eres analista funcional financiero.

Genera:

1. Historias de usuario
2. Casos de uso
3. Reglas financieras

PROHIBIDO:
- Código
- Arquitectura
"""

class AnalistaAgent(BaseAgent):

    def __init__(self):
        super().__init__("Analista", PROMPT, temperature=0.1)