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

PROMPT = """
Eres analista funcional financiero.

Genera:

1. Análisis financiero basado en requerimientos e historias de usuario
2. Casos de uso
3. Reglas financieras

PROHIBIDO:
- Código
- Arquitectura
"""

class AnalistaAgent(BaseAgent):

    def __init__(self):
        super().__init__("Analista", PROMPT, temperature=0.1)

    def run(self, requerimiento, historias):
        # Combina requerimiento + historias
        texto = f"{requerimiento}\nHistorias de usuario:\n{historias}"
        return super().run(texto)