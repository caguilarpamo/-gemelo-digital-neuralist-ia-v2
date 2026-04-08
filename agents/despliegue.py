# agents/despliegue.py
from core.base_agent import BaseAgent

PROMPT = """
Eres un experto en despliegue de sistemas financieros.

Tu tarea es:
- Preparar scripts de despliegue
- Instrucciones de instalación y configuración
- Buenas prácticas de seguridad y manejo de transacciones
"""

class DespliegueAgent(BaseAgent):

    def __init__(self):
        super().__init__("Despliegue", PROMPT, temperature=0.1)

    def generar_scripts(self, codigo):
        return self.run(f"Codigo: {codigo}")