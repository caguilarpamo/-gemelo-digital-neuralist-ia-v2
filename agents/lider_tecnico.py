# agents/lider_tecnico.py
from core.base_agent import BaseAgent

PROMPT = """
Eres un líder técnico financiero.

Tu tarea es:
- Revisar arquitectura y análisis
- Definir estándares de desarrollo
- Planificar la implementación del sistema

Entrega un plan técnico claro para el desarrollo.
"""

class LiderTecnicoAgent(BaseAgent):

    def __init__(self):
        super().__init__("Lider Técnico", PROMPT, temperature=0.2)

    def planificar(self, arquitectura, analisis):
        input_text = f"Analisis: {analisis}\nArquitectura: {arquitectura}"
        return self.run(input_text)