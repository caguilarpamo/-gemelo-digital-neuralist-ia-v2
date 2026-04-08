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


###funcional
# import gradio as gr
# from graph.workflow import ejecutar_flujo

# def procesar_requerimiento(texto):
#     resultado = ejecutar_flujo(texto)
#     return (
#         resultado["historias"],
#         resultado["analisis"],
#         resultado["arquitectura"],
#         resultado["plan_tecnico"],
#         resultado["codigo"],
#         resultado["qa1"],
#         resultado["qa2"],
#         resultado["documentacion"],
#         resultado["despliegue"],
#         resultado["entregable"]
#     )

# app = gr.Interface(
#     fn=procesar_requerimiento,
#     inputs=gr.Textbox(label="Describe tu requerimiento financiero"),
#     outputs=[
#         gr.Textbox(label="📜 Historias de Usuario"),
#         gr.Textbox(label="📌 Análisis"),
#         gr.Textbox(label="🏗️ Arquitectura"),
#         gr.Textbox(label="📝 Plan Técnico (Líder Técnico)"),
#         gr.Code(label="💻 Código", language="python"),
#         gr.Textbox(label="🧪 QA1 - Validación de requerimientos"),
#         gr.Textbox(label="🧪 QA2 - Pruebas reales"),
#         gr.Textbox(label="📚 Documentación"),
#         gr.Textbox(label="🚀 Despliegue"),
#         gr.Textbox(label="🎁 Entregable final")
#     ],
#     title="💰 GEMELO DIGITAL FINANCIERO IA",
#     description="Ingresa un requerimiento y genera todo el flujo financiero automatizado.",
# )

# if __name__ == "__main__":
#     app.launch(share=True)

# app_gradio.py
import gradio as gr
from dotenv import load_dotenv
from graph.workflow import ejecutar_flujo

load_dotenv()

# CSS personalizado (puedes ponerlo dentro de <style> o en un archivo externo)
css = """
    /* Fondo general con gradiente */
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }
    /* Tarjetas de entrada/salida */
    .card {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    /* Botón principal */
    .primary-btn {
        background: linear-gradient(95deg, #0b4f6c 0%, #1e7e6c 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 12px 24px;
        border-radius: 40px;
        transition: transform 0.2s;
    }
    .primary-btn:hover {
        transform: scale(1.02);
        background: linear-gradient(95deg, #0a3e55 0%, #186b5c 100%) !important;
    }
    /* Títulos */
    h1, h2, h3 {
        color: #fff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    /* Etiquetas de los outputs */
    label span {
        font-weight: 600;
        color: #1e2a3a;
    }
    /* Código */
    .prose pre {
        border-radius: 16px;
        background: #1e1e2f !important;
    }
"""

#def procesar_requerimiento(texto):
#    resultado = ejecutar_flujo(texto)
#    return (
#        resultado["historias"],
#        resultado["analisis"],
#        resultado["arquitectura"],
#        resultado["plan_tecnico"],
#        resultado["codigo"],
#        resultado["qa1"],
#        resultado["qa2"],
#        resultado["documentacion"],
#        resultado["despliegue"],
#        resultado["entregable"]
#    )

def procesar_requerimiento(texto):
    try:
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

    except Exception as e:
        mensaje = str(e)

        # Mensaje amigable para el usuario
        alerta = f"⚠️ {mensaje}\n\nEste sistema solo procesa requerimientos financieros."

        # Retornamos vacío + mensaje en el primer tab (o donde quieras)
        return (
            alerta, "", "", "", "", "", "", "", "", ""
        )

# Construimos la interfaz con gr.Blocks para mayor control
with gr.Blocks(css=css, title="Gemelo Digital Financiero IA") as app:
    gr.Markdown("""
    # 💰 GEMELO DIGITAL FINANCIERO IA
    ### Ingresa un requerimiento y genera todo el flujo financiero automatizado.
    """)
    
    with gr.Row():
        with gr.Column(scale=4):
            requerimiento = gr.Textbox(
                label="📝 Describe tu requerimiento financiero",
                placeholder="Ejemplo: 'Necesito una app bancaria para créditos hipotecarios con simulador de cuotas'",
                lines=4,
                elem_classes="card"
            )
        with gr.Column(scale=1):
            # Botón personalizado
            btn = gr.Button("🚀 Generar flujo completo", elem_classes="primary-btn")
    
    # Organizamos los 10 outputs en grupos visuales
    with gr.Tabs():
        with gr.TabItem("📋 Historias de Usuario"):
            historias_out = gr.Textbox(label="", lines=15, elem_classes="card")
        with gr.TabItem("📌 Análisis"):
            analisis_out = gr.Textbox(label="", lines=15, elem_classes="card")
        with gr.TabItem("🏗️ Arquitectura"):
            arquitectura_out = gr.Textbox(label="", lines=15, elem_classes="card")
        with gr.TabItem("📝 Plan Técnico"):
            plan_out = gr.Textbox(label="", lines=15, elem_classes="card")
        with gr.TabItem("💻 Código"):
            codigo_out = gr.Code(label="", language="python", elem_classes="card")
        with gr.TabItem("🧪 QA1 - Validación"):
            qa1_out = gr.Textbox(label="", lines=10, elem_classes="card")
        with gr.TabItem("🧪 QA2 - Pruebas"):
            qa2_out = gr.Textbox(label="", lines=10, elem_classes="card")
        with gr.TabItem("📚 Documentación"):
            doc_out = gr.Textbox(label="", lines=15, elem_classes="card")
        with gr.TabItem("🚀 Despliegue"):
            despliegue_out = gr.Textbox(label="", lines=10, elem_classes="card")
        with gr.TabItem("🎁 Entregable Final"):
            entregable_out = gr.Textbox(label="", lines=10, elem_classes="card")
    
    # Conectar botón con la función
    btn.click(
        fn=procesar_requerimiento,
        inputs=requerimiento,
        outputs=[
            historias_out, analisis_out, arquitectura_out, plan_out,
            codigo_out, qa1_out, qa2_out, doc_out, despliegue_out, entregable_out
        ]
    )

if __name__ == "__main__":
    app.launch(share=True)