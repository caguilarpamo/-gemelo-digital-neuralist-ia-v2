# agents/documentador.py
from core.base_agent import BaseAgent

PROMPT = """
Eres un documentador financiero.

Tu tarea es:
- Generar documentación completa del proyecto
- Incluir análisis, arquitectura, código y reportes QA
- Crear manuales y guías claras

Entrega un documento final organizado.
"""

class DocumentadorAgent(BaseAgent):

    def __init__(self):
        super().__init__("Documentador", PROMPT, temperature=0.1)

    def generar_doc(self, analisis, arquitectura, codigo, qa1, qa2):
        input_text = f"Analisis: {analisis}\nArquitectura: {arquitectura}\nCodigo: {codigo}\nQA1: {qa1}\nQA2: {qa2}"
        return self.run(input_text)