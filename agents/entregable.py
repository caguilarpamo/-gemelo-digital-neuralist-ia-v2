# agents/entregable.py
from core.base_agent import BaseAgent

PROMPT = """Empaquetador final. Devuelve un índice del paquete listando cada artefacto (doc + scripts) con descripción de 1 línea."""

class EntregableAgent(BaseAgent):

    def __init__(self):
        super().__init__("Entregable Final", PROMPT, temperature=0.1)

    def generar_entregable(self, doc, scripts):
        return self.run(f"Documentacion: {doc}\nScripts: {scripts}")