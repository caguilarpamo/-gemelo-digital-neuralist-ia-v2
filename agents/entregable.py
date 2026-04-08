# agents/entregable.py
from core.base_agent import BaseAgent

PROMPT = """
Eres responsable de generar el entregable final financiero.

Tu tarea es:
- Unir documentación y scripts de despliegue
- Generar un paquete completo listo para entrega
"""

class EntregableAgent(BaseAgent):

    def __init__(self):
        super().__init__("Entregable Final", PROMPT, temperature=0.1)

    def generar_entregable(self, doc, scripts):
        return self.run(f"Documentacion: {doc}\nScripts: {scripts}")