# agents/requerimientos.py
from core.base_agent import BaseAgent

PROMPT = """
Eres un experto en requerimientos funcionales financieros.

Genera:
1. Historias de usuario
2. Reglas de negocio financieras

Recuerda entregar solo textos claros y estructurados.
"""

class RequerimientosAgent(BaseAgent):

    def __init__(self):
        super().__init__("Requerimientos", PROMPT, temperature=0.1)

    def generar_historias(self, requerimiento):
        return self.run(requerimiento)