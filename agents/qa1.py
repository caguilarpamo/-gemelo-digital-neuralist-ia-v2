# from core.base_agent import BaseAgent

# PROMPT_QA1 = """
# Valida que el código cumpla requerimientos.

# No ejecutes código.
# Solo análisis.
# """

# class QA1Agent(BaseAgent):
#     pass

# agents/qa1.py
from core.base_agent import BaseAgent

PROMPT_QA1 = """QA estático. Verifica si el código cubre los casos de uso y reglas del análisis. Devuelve lista ✓/✗ con justificación 1 línea. No reescribas código."""

class QA1Agent(BaseAgent):
    
    def __init__(self):
        super().__init__("QA1", PROMPT_QA1, temperature=0.1)

    # Método de validación placeholder
    def validar(self, codigo, analisis):
        return "✅ QA1 - Validación de requerimientos simulada"