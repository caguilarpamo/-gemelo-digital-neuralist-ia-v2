# agents/lider_tecnico.py
from core.base_agent import BaseAgent

PROMPT = """ROL: Líder Técnico (Lead Engineer) de un equipo financiero.
INPUT: Análisis + arquitectura.
TAREA: Produce DOS planes accionables —uno para el dev frontend y otro para el dev backend— que trabajarán en paralelo.

FORMATO OBLIGATORIO (marcadores literales):

### PLAN FRONTEND ###
- Pantallas (PascalCase + propósito).
- Componentes clave.
- Flujos de usuario.
- Estados UI (loading/error/vacío/éxito).
- Estilo (colores, tono).
Prohibido: backend, DB, endpoints.

### PLAN BACKEND ###
- Endpoints REST (método, ruta, payload, respuesta).
- Modelo de datos.
- Reglas de negocio y validaciones.
- Transacciones y seguridad.
- Contrato que consume el frontend.

Sé concreto. Sin código."""


def _split_plans(texto: str) -> dict:
    """Separa el plan completo en plan_frontend / plan_backend usando los marcadores.
    Si el LLM no respetó el formato, ambos reciben el plan completo como fallback."""
    marker_fe = "### PLAN FRONTEND ###"
    marker_be = "### PLAN BACKEND ###"

    if marker_fe in texto and marker_be in texto:
        fe_start = texto.index(marker_fe) + len(marker_fe)
        be_start = texto.index(marker_be)
        plan_frontend = texto[fe_start:be_start].strip()
        plan_backend = texto[be_start + len(marker_be):].strip()
    else:
        plan_frontend = texto
        plan_backend = texto

    return {
        "full": texto,
        "plan_frontend": plan_frontend,
        "plan_backend": plan_backend,
    }


class LiderTecnicoAgent(BaseAgent):

    def __init__(self):
        super().__init__("Lider Técnico", PROMPT, temperature=0.2)

    def planificar(self, arquitectura, analisis):
        input_text = f"Analisis: {analisis}\nArquitectura: {arquitectura}"
        texto = self.run(input_text)
        return _split_plans(texto)
