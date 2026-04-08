from core.base_agent import BaseAgent

PROMPT = """Clasifica si el sistema es financiero (banca/pagos/fintech/contabilidad/créditos). Responde SOLO con una palabra: APROBADO o RECHAZADO."""

class ValidadorAgent(BaseAgent):

    def __init__(self):
        super().__init__("Validador", PROMPT, temperature=0.0)

    def validar(self, text):
        result = self.run(text)

        if "RECHAZADO" in result:
            raise Exception("❌ Requerimiento no financiero")

        return result