# agents/qa2.py
from core.base_agent import BaseAgent
from tools.test_tools import run_tests

PROMPT_QA2 = """QA integral (funcional + usabilidad). Recibes backend, frontend y pruebas básicas.

Devuelve Markdown con 3 secciones:

## Funcional
✓/✗ por ítem (consistencia, transacciones, errores, casos borde) — 1 línea c/u.

## Usabilidad (10 heurísticas de Nielsen sobre el frontend)
1. Visibilidad del estado
2. Mundo real
3. Control y libertad
4. Consistencia y estándares
5. Prevención de errores
6. Reconocer vs recordar
7. Flexibilidad y eficiencia
8. Estética minimalista
9. Recuperación de errores
10. Ayuda y documentación
Por cada una: ✓/✗ + observación de 1 línea.

## Veredicto
APROBADO o REQUIERE AJUSTES + razón breve."""


class QA2Agent(BaseAgent):

    def __init__(self):
        super().__init__("QA2", PROMPT_QA2, temperature=0.1)

    def probar(self, codigo, frontend_output=""):
        pruebas_basicas = run_tests(codigo)
        entrada = (
            f"CODIGO BACKEND:\n{codigo}\n\n"
            f"FRONTEND GENERADO:\n{frontend_output}\n\n"
            f"PRUEBAS BASICAS:\n{pruebas_basicas}"
        )
        return self.run(entrada)
