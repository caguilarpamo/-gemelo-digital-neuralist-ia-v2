from core.base_agent import BaseAgent

PROMPT = """
Eres arquitecto de software financiero.

Debes definir:

1. Arquitectura
2. Base de datos
3. Seguridad
4. Manejo de transacciones

Usa buenas prácticas financieras.
"""

class ArquitectoAgent(BaseAgent):

    def __init__(self):
        super().__init__("Arquitecto", PROMPT, temperature=0.2)