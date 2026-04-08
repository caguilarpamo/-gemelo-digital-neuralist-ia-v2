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

import re
from pathlib import Path

import gradio as gr
from graph.workflow import ejecutar_flujo

STITCH_DIR = Path("output/stitch")
IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def _collect_frontend_visuals():
    """Lee output/stitch/*.html y devuelve:
       - lista de URLs de imágenes (para gr.Gallery)
       - HTML combinado con cada pantalla en un iframe (para gr.HTML)
    """
    if not STITCH_DIR.exists():
        return [], "<p><em>Aún no hay pantallas generadas. Ejecuta el flujo primero.</em></p>"

    files = sorted(STITCH_DIR.glob("*.html"))
    if not files:
        return [], "<p><em>No se encontraron archivos HTML en output/stitch/.</em></p>"

    images = []
    sections = []
    for f in files:
        html = f.read_text(encoding="utf-8", errors="ignore")
        # 1. Extraer URLs absolutas o data URIs (las relativas no resuelven en Gradio)
        for src in IMG_RE.findall(html):
            if src.startswith(("http://", "https://", "data:")):
                images.append((src, f.stem))
        # 2. Render inline vía iframe srcdoc (escapamos comillas dobles)
        escaped = html.replace('"', "&quot;")
        sections.append(
            f'<h3 style="margin:1.5rem 0 0.5rem;font-family:system-ui">📱 {f.stem}</h3>'
            f'<iframe srcdoc="{escaped}" '
            f'style="width:100%;height:640px;border:1px solid #ddd;border-radius:8px;background:#fff"></iframe>'
        )

    return images, "\n".join(sections)


def procesar_requerimiento(texto):
    resultado = ejecutar_flujo(texto)
    images, screens_html = _collect_frontend_visuals()
    return (
        resultado["historias"],
        resultado["analisis"],
        resultado["arquitectura"],
        resultado["plan_tecnico"],
        resultado["frontend"],          # Markdown — texto del agente
        images,                          # Gallery — imágenes Stitch
        screens_html,                    # HTML — pantallas renderizadas inline
        resultado["codigo"],
        resultado["qa1"],
        resultado["qa2"],                # Markdown — Nielsen
        resultado["documentacion"],
        resultado["despliegue"],         # Markdown — URL Vercel clickeable
        resultado["entregable"],
    )


app = gr.Interface(
    fn=procesar_requerimiento,
    inputs=gr.Textbox(label="Describe tu requerimiento financiero", lines=4),
    outputs=[
        gr.Textbox(label="📜 Historias de Usuario"),
        gr.Textbox(label="📌 Análisis"),
        gr.Textbox(label="🏗️ Arquitectura"),
        gr.Textbox(label="📝 Plan Técnico (Líder Técnico — FE + BE)"),
        gr.Markdown(label="🎨 Frontend (Stitch → React) — reporte del agente"),
        gr.Gallery(label="🖼️ Mockups generados por Stitch", columns=2, height="auto"),
        gr.HTML(label="📱 Pantallas renderizadas (preview en vivo)"),
        gr.Code(label="💻 Código Backend", language="python"),
        gr.Textbox(label="🧪 QA1 — Validación de requerimientos"),
        gr.Markdown(label="🧪 QA2 — Funcional + 10 heurísticas de Nielsen"),
        gr.Textbox(label="📚 Documentación"),
        gr.Markdown(label="🚀 Despliegue (Vercel) — URL pública clickeable"),
        gr.Textbox(label="🎁 Entregable final"),
    ],
    title="💰 GEMELO DIGITAL FINANCIERO IA",
    description="Ingresa un requerimiento financiero y genera todo el flujo: análisis → arquitectura → frontend (Stitch) → backend → QA → deploy a Vercel.",
)

if __name__ == "__main__":
    app.launch(share=True)