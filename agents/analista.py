# from core.base_agent import BaseAgent

# PROMPT = """
# Eres analista funcional financiero.

# Genera:

# 1. Historias de usuario
# 2. Casos de uso
# 3. Reglas financieras

# PROHIBIDO:
# - Código
# - Arquitectura
# """

# class AnalistaAgent(BaseAgent):

#     def __init__(self):
#         super().__init__("Analista", PROMPT, temperature=0.1)

# agents/analista.py
from core.base_agent import BaseAgent

PROMPT = """Analista funcional financiero. Entrega Markdown con: casos de uso, reglas financieras (montos/tasas/validaciones), restricciones regulatorias. Sin código ni arquitectura."""

class AnalistaAgent(BaseAgent):

    def __init__(self):
        super().__init__("Analista", PROMPT, temperature=0.1)

    def run(self, requerimiento, historias):
        # Combina requerimiento + historias
        texto = f"{requerimiento}\nHistorias de usuario:\n{historias}"
        return super().run(texto)