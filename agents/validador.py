from core.base_agent import BaseAgent

PROMPT = """
Eres un validador de software financiero.

SOLO aceptas:
- banca
- pagos
- fintech
- contabilidad
- créditos

Si NO es financiero responde EXACTAMENTE:
RECHAZADO

Si SÍ:
APROBADO
"""

class ValidadorAgent(BaseAgent):

    def __init__(self):
        super().__init__("Validador", PROMPT, temperature=0.0)

    def validar(self, text):
        result = self.run(text)

        if "RECHAZADO" in result:
            raise Exception("❌ Requerimiento no financiero")

        return result