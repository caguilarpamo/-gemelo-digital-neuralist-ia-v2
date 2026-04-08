from core.base_agent import BaseAgent

PROMPT = """ROL: Desarrollador Backend financiero.
INPUT: Plan backend del Líder Técnico + resumen del frontend ya generado.
REGLAS:
- Python + FastAPI.
- Decimal para dinero (nunca float).
- Transacciones y manejo de errores.
- Endpoints y DTOs alineados con las pantallas/flujos del frontend entregado.
SALIDA: Código Python ejecutable, sin explicaciones."""


class DevAgent(BaseAgent):

    def __init__(self):
        super().__init__("Desarrollador Backend", PROMPT, temperature=0.1)

    def run(self, plan_backend, frontend_output=""):
        """Genera el backend a partir del plan del Líder Técnico y del resumen
        del frontend ya generado (para alinear el contrato de integración)."""
        input_text = (
            f"PLAN BACKEND (del Líder Técnico):\n{plan_backend}\n\n"
            f"FRONTEND YA GENERADO (componentes y pantallas que debes soportar):\n{frontend_output}"
        )
        return super().run(input_text)
