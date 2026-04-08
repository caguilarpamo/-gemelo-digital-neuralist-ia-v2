# agents/requerimientos.py
from core.base_agent import BaseAgent

PROMPT = """Experto en requerimientos financieros. Devuelve Markdown con `## Historias` (3-6 en formato "Como X, quiero Y, para Z") y `## Reglas` (reglas de negocio). Sin código."""

class RequerimientosAgent(BaseAgent):

    def __init__(self):
        super().__init__("Requerimientos", PROMPT, temperature=0.1)

    def generar_historias(self, requerimiento):
        return self.run(requerimiento)