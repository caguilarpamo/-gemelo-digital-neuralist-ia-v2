# from agents.validador import ValidadorAgent
# from agents.analista import AnalistaAgent
# from agents.arquitecto import ArquitectoAgent
# from agents.dev import DevAgent

# validador = ValidadorAgent()
# analista = AnalistaAgent()
# arquitecto = ArquitectoAgent()
# dev = DevAgent()


# def ejecutar_flujo(requerimiento):

#     print("\n🚀 INICIO DEL PROCESO\n")

#     # 1. Validación
#     validador.validar(requerimiento)
#     print("✅ Validación OK")

#     # 2. Análisis
#     analisis = analista.run(requerimiento)
#     print("✅ Análisis generado")

#     # 3. Arquitectura
#     arquitectura = arquitecto.run(analisis)
#     print("✅ Arquitectura generada")

#     # 4. Desarrollo
#     codigo = dev.run(arquitectura)
#     print("✅ Código generado")

#     return {
#         "analisis": analisis,
#         "arquitectura": arquitectura,
#         "codigo": codigo
#     }

# workflow.py
from agents.validador import ValidadorAgent
from agents.requerimientos import RequerimientosAgent
from agents.analista import AnalistaAgent
from agents.arquitecto import ArquitectoAgent
from agents.lider_tecnico import LiderTecnicoAgent
from agents.dev import DevAgent
from agents.qa1 import QA1Agent
from agents.qa2 import QA2Agent
from agents.documentador import DocumentadorAgent
from agents.despliegue import DespliegueAgent
from agents.entregable import EntregableAgent

# Instancias
validador = ValidadorAgent()
requerimientos = RequerimientosAgent()
analista = AnalistaAgent()
arquitecto = ArquitectoAgent()
lider = LiderTecnicoAgent()
dev = DevAgent()
qa1 = QA1Agent()
qa2 = QA2Agent()
documentador = DocumentadorAgent()
despliegue = DespliegueAgent()
entregable = EntregableAgent()


def ejecutar_flujo(requerimiento):
    print("\n🚀 INICIO DEL PROCESO\n")

    # 0. Validación
    validador.validar(requerimiento)
    print("✅ Requerimiento aprobado")

    # 1. Requerimientos
    historias = requerimientos.generar_historias(requerimiento)
    print("✅ Historias de usuario generadas")

    # 2. Analista
    analisis = analista.run(requerimiento, historias)
    print("✅ Análisis generado")

    # 3. Arquitecto
    arquitectura = arquitecto.run(analisis)
    print("✅ Arquitectura generada")

    # 4. Líder Técnico
    plan_tecnico = lider.planificar(arquitectura, analisis)
    print("✅ Plan técnico generado")

    # 5. Desarrollo
    codigo = dev.run(plan_tecnico)
    print("✅ Código generado")

    # 6. QA1
    qa1_reporte = qa1.validar(codigo, analisis)
    print("✅ QA1 completado")

    # 7. QA2
    qa2_reporte = qa2.probar(codigo)
    print("✅ QA2 completado")

    # 8. Documentador
    doc = documentador.generar_doc(analisis, arquitectura, codigo, qa1_reporte, qa2_reporte)
    print("✅ Documentación generada")

    # 9. Despliegue
    scripts = despliegue.generar_scripts(codigo)
    print("✅ Scripts de despliegue generados")

    # 10. Entregable final
    paquete = entregable.generar_entregable(doc, scripts)
    print("✅ Entregable final listo")

    return {
        "historias": historias,
        "analisis": analisis,
        "arquitectura": arquitectura,
        "plan_tecnico": plan_tecnico,
        "codigo": codigo,
        "qa1": qa1_reporte,
        "qa2": qa2_reporte,
        "documentacion": doc,
        "despliegue": scripts,
        "entregable": paquete
    }