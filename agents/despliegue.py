# agents/despliegue.py
from core.base_agent import BaseAgent
from tools.vercel_tools import deploy_to_vercel

# Prompt reservado por si algún día queremos delegar el reporte al LLM.
# En el happy path el agente NO usa LLM (ahorro de tokens): construye el reporte
# determinísticamente a partir del resultado del deploy.
PROMPT = """DevOps. Describe el deploy realizado destacando la URL pública."""


class DespliegueAgent(BaseAgent):
    """
    Agente de despliegue automatizado. Reemplaza la antigua generación de scripts
    manuales por un deploy real a Vercel vía tools/vercel_tools.deploy_to_vercel().

    El agente lee los archivos que el DesarrolladorFrontEndAgent dejó en
    output/stitch/ y los publica como sitio estático en Vercel, devolviendo una
    URL pública lista para compartir con el usuario.
    """

    def __init__(self):
        super().__init__("Despliegue", PROMPT, temperature=0.0)

    def desplegar(self, frontend_output: str = "", codigo: str = "") -> str:
        """Ejecuta el deploy completo (frontend + backend) y devuelve un reporte
        Markdown con la URL pública."""
        print("   🚀 Iniciando deploy automático a Vercel (frontend + backend)...")
        result = deploy_to_vercel(codigo=codigo)

        url = result.get("url")
        files = result.get("files", [])
        error = result.get("error")
        stub = result.get("stub", False)

        # Error fatal: ningún URL
        if not url:
            return (
                "## ❌ Despliegue fallido\n\n"
                f"**Error:** {error or 'desconocido'}\n\n"
                "Verifica que el paso de frontend haya generado archivos en `output/stitch/` "
                "y que `VERCEL_TOKEN` esté presente en el `.env`."
            )

        # Reporte de éxito (o stub con URL)
        badge = "⚠️ STUB" if stub else "✅ LIVE"
        lines = [
            f"## 🚀 Despliegue a Vercel — {badge}",
            "",
            f"### 🔗 URL pública: {url}",
            "",
            f"**Archivos desplegados ({len(files)}):**",
            *[f"- `{f}`" for f in files],
        ]
        if stub and error:
            lines += ["", f"> _Nota: {error}_"]
        elif stub:
            lines += [
                "",
                "> _Modo stub: agrega `VERCEL_TOKEN` al `.env` para habilitar el deploy real._",
            ]
        return "\n".join(lines)

    # Alias de compatibilidad por si algún otro punto del código llama al nombre viejo.
    def generar_scripts(self, codigo="", frontend_output=""):
        return self.desplegar(frontend_output, codigo)
