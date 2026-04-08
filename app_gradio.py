# # app_gradio.py
# import gradio as gr
# from dotenv import load_dotenv
# from graph.workflow import ejecutar_flujo

# load_dotenv()

# def procesar(req):
#     try:
#         resultado = ejecutar_flujo(req)
#         return resultado["analisis"], resultado["arquitectura"], resultado["codigo"]
#     except Exception as e:
#         return str(e), "", ""

# # Definimos la interfaz
# iface = gr.Interface(
#     fn=procesar,
#     inputs=gr.Textbox(label="Describe el sistema financiero", lines=5, placeholder="Ej: Sistema de créditos..."),
#     outputs=[
#         gr.Textbox(label="📌 ANALISIS"),
#         gr.Textbox(label="🏗️ ARQUITECTURA"),
#         gr.Code(label="💻 CODIGO", language="python")
#     ],
#     title="💰 GEMELO DIGITAL FINANCIERO IA",
#     description="Ingresa la descripción del sistema financiero y analiza el flujo completo."
# )

# # Lanzamos la app
# iface.launch(share=True)  # share=True genera un link público tipo ngrok automáticamente


########### separacion

# # app_gradio.py
# import gradio as gr
# from graph.workflow import ejecutar_flujo

# def procesar_requerimiento(texto):
#     return ejecutar_flujo(texto)

# app = gr.Interface(
#     fn=procesar_requerimiento,
#     inputs=gr.Textbox(label="Describe tu requerimiento financiero"),
#     outputs=[
#         gr.Textbox(label="📜 Historias de Usuario"),
#         gr.Textbox(label="📌 Análisis"),
#         gr.Textbox(label="🏗️ Arquitectura"),
#         gr.Textbox(label="📝 Plan Técnico (Líder Técnico)"),
#         gr.Code(label="💻 Código", language="python"),
#         # gr.Code(label="💻 Código")  # Sin lenguaje, Gradio muestra como texto plano
#         gr.Textbox(label="🧪 QA1 - Validación de requerimientos"),
#         gr.Textbox(label="🧪 QA2 - Pruebas reales"),
#         gr.Textbox(label="📚 Documentación"),
#         gr.Textbox(label="🚀 Despliegue"),
#         gr.Textbox(label="🎁 Entregable final")
#     ],
#     title="💰 GEMELO DIGITAL FINANCIERO IA",
#     description="Ingresa un requerimiento y genera todo el flujo financiero automatizado.",
#     # allow_flagging="never"  # Aquí quitamos el flag
# )

# if __name__ == "__main__":
#     app.launch(share=True)

import gradio as gr
from graph.workflow import ejecutar_flujo

def procesar_requerimiento(texto):
    resultado = ejecutar_flujo(texto)
    return (
        resultado["historias"],
        resultado["analisis"],
        resultado["arquitectura"],
        resultado["plan_tecnico"],
        resultado["codigo"],
        resultado["qa1"],
        resultado["qa2"],
        resultado["documentacion"],
        resultado["despliegue"],
        resultado["entregable"]
    )

app = gr.Interface(
    fn=procesar_requerimiento,
    inputs=gr.Textbox(label="Describe tu requerimiento financiero"),
    outputs=[
        gr.Textbox(label="📜 Historias de Usuario"),
        gr.Textbox(label="📌 Análisis"),
        gr.Textbox(label="🏗️ Arquitectura"),
        gr.Textbox(label="📝 Plan Técnico (Líder Técnico)"),
        gr.Code(label="💻 Código", language="python"),
        gr.Textbox(label="🧪 QA1 - Validación de requerimientos"),
        gr.Textbox(label="🧪 QA2 - Pruebas reales"),
        gr.Textbox(label="📚 Documentación"),
        gr.Textbox(label="🚀 Despliegue"),
        gr.Textbox(label="🎁 Entregable final")
    ],
    title="💰 GEMELO DIGITAL FINANCIERO IA",
    description="Ingresa un requerimiento y genera todo el flujo financiero automatizado.",
)

if __name__ == "__main__":
    app.launch(share=True)