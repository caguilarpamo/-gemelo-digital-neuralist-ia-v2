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
from agents.desarrollador_frontend import DesarrolladorFrontEndAgent
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
frontend_dev = DesarrolladorFrontEndAgent()
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

    # 4. Líder Técnico -> emite DOS planes: frontend y backend
    plan_tecnico = lider.planificar(arquitectura, analisis)
    print("✅ Plan técnico generado (frontend + backend)")

    # 5a. Desarrollador Frontend (Stitch MCP -> React)
    # Truncamos el plan a 2000 chars para mantenernos bajo el rate limit (50K tokens/min en Haiku 4.5)
    plan_fe_short = plan_tecnico["plan_frontend"][:2000]
    frontend_output = frontend_dev.run(plan_fe_short)
    print("✅ Frontend generado vía Stitch")

    # 5b. Desarrollador Backend (recibe plan_backend + contexto del frontend ya construido)
    codigo = dev.run(plan_tecnico["plan_backend"], frontend_output)
    print("✅ Código backend generado e integrado con el frontend")

    # 6. QA1
    qa1_reporte = qa1.validar(codigo, analisis)
    print("✅ QA1 completado")

    # 7. QA2 (funcional + usabilidad Nielsen sobre frontend + backend)
    qa2_reporte = qa2.probar(codigo, frontend_output)
    print("✅ QA2 completado (funcional + Nielsen)")

    # 8. Documentador
    doc = documentador.generar_doc(analisis, arquitectura, codigo, qa1_reporte, qa2_reporte)
    print("✅ Documentación generada")

    # 9. Despliegue automático a Vercel — frontend (React+Tailwind) + backend (serverless Python)
    scripts = despliegue.desplegar(frontend_output, codigo)
    print("✅ Deploy a Vercel completado (frontend + backend)")

    # 10. Entregable final
    paquete = entregable.generar_entregable(doc, scripts)
    print("✅ Entregable final listo")

    return {
        "historias": historias,
        "analisis": analisis,
        "arquitectura": arquitectura,
        "plan_tecnico": plan_tecnico["full"],
        "plan_frontend": plan_tecnico["plan_frontend"],
        "plan_backend": plan_tecnico["plan_backend"],
        "frontend": frontend_output,
        "codigo": codigo,
        "qa1": qa1_reporte,
        "qa2": qa2_reporte,
        "documentacion": doc,
        "despliegue": scripts,
        "entregable": paquete
    }