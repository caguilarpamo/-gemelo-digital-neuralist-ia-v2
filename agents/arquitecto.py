from core.base_agent import BaseAgent

PROMPT = """Arquitecto financiero. Markdown con: capas (API/dominio/datos), esquema DB (tablas clave), seguridad (auth/cifrado/auditoría), transacciones ACID. Sin código."""

class ArquitectoAgent(BaseAgent):

    def __init__(self):
        super().__init__("Arquitecto", PROMPT, temperature=0.2)