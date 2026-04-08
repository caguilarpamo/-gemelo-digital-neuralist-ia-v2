"""
Helper de alto nivel usado por DespliegueAgent para desplegar a Vercel
el sitio estático generado por el agente frontend (output/stitch/*.html).
"""
import asyncio
from pathlib import Path
from typing import Dict, List

import nest_asyncio

from config.settings import Settings
from tools.vercel_client import VercelMCPClient

nest_asyncio.apply()

STITCH_DIR = Path("output/stitch")


def _build_index(screen_files: List[Path]) -> str:
    """Genera un index.html con navegación a cada pantalla generada por Stitch."""
    links = "\n".join(
        f'    <li><a href="{p.name}">{p.stem}</a></li>' for p in screen_files
    )
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gemelo Digital Financiero</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 720px; margin: 3rem auto; padding: 0 1rem; color: #1a1a1a; }}
    h1 {{ font-size: 1.8rem; }}
    ul {{ line-height: 2; }}
    a {{ color: #0070f3; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    footer {{ margin-top: 3rem; font-size: 0.85rem; color: #666; }}
  </style>
</head>
<body>
  <h1>🚀 Aplicación desplegada</h1>
  <p>Generada automáticamente por el Gemelo Digital Financiero IA.</p>
  <h2>Pantallas disponibles</h2>
  <ul>
{links}
  </ul>
  <footer>Deploy automatizado vía Vercel MCP.</footer>
</body>
</html>"""


def _run(coro):
    """Ejecuta una corrutina desde código sync (BaseAgent es sync)."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return loop.run_until_complete(coro)
    except RuntimeError:
        pass
    return asyncio.run(coro)


def deploy_to_vercel(project_name: str = None) -> Dict:
    """
    Empaqueta los HTML generados por Stitch y los despliega a Vercel.

    Returns:
        dict con url, files, stub, error (opcional).
    """
    project_name = project_name or Settings.VERCEL_PROJECT_NAME

    if not STITCH_DIR.exists():
        return {
            "url": None,
            "files": [],
            "error": f"Directorio {STITCH_DIR} no existe. Ejecuta el paso de frontend primero.",
            "stub": True,
        }

    html_files = sorted(STITCH_DIR.glob("*.html"))
    if not html_files:
        return {
            "url": None,
            "files": [],
            "error": f"No hay archivos .html en {STITCH_DIR}.",
            "stub": True,
        }

    # Construir payload para Vercel
    files_payload: List[Dict[str, str]] = []
    for f in html_files:
        files_payload.append({"file": f.name, "data": f.read_text(encoding="utf-8")})

    # Agregar index.html de navegación si no existe
    if not any(f["file"].lower() == "index.html" for f in files_payload):
        files_payload.append({"file": "index.html", "data": _build_index(html_files)})

    client = VercelMCPClient()
    print(f"   📤 Subiendo {len(files_payload)} archivos a Vercel ({project_name})...")
    result = _run(client.deploy_static(project_name, files_payload))
    result["files"] = [f["file"] for f in files_payload]
    return result
