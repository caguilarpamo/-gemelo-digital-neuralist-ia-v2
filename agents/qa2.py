# from core.base_agent import BaseAgent
# from tools.test_tools import run_tests

# PROMPT_QA2 = """
# Ejecuta pruebas reales.

# Valida:
# - consistencia
# - transacciones
# - errores
# """

# class QA2Agent(BaseAgent):
#     pass

# agents/qa2.py
from core.base_agent import BaseAgent
from tools.test_tools import run_tests

PROMPT_QA2 = """
Ejecuta pruebas reales.

Valida:
- consistencia
- transacciones
- errores
"""

class QA2Agent(BaseAgent):
    
    def __init__(self):
        super().__init__("QA2", PROMPT_QA2, temperature=0.1)

    def probar(self, codigo):
        return run_tests(codigo)