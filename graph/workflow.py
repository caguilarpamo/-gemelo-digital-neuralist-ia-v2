from agents.validador import ValidadorAgent
from agents.analista import AnalistaAgent
from agents.arquitecto import ArquitectoAgent
from agents.dev import DevAgent

validador = ValidadorAgent()
analista = AnalistaAgent()
arquitecto = ArquitectoAgent()
dev = DevAgent()


def ejecutar_flujo(requerimiento):

    print("\n🚀 INICIO DEL PROCESO\n")

    # 1. Validación
    validador.validar(requerimiento)
    print("✅ Validación OK")

    # 2. Análisis
    analisis = analista.run(requerimiento)
    print("✅ Análisis generado")

    # 3. Arquitectura
    arquitectura = arquitecto.run(analisis)
    print("✅ Arquitectura generada")

    # 4. Desarrollo
    codigo = dev.run(arquitectura)
    print("✅ Código generado")

    return {
        "analisis": analisis,
        "arquitectura": arquitectura,
        "codigo": codigo
    }