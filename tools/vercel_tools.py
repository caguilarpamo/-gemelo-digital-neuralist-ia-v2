"""
Helper de alto nivel usado por DespliegueAgent para desplegar a Vercel
una aplicación completa: frontend (React + Tailwind CDN) + backend
(Python serverless function en api/index.py).
"""
import asyncio
import concurrent.futures
import re
from pathlib import Path
from typing import Dict, List

from config.settings import Settings
from tools.vercel_client import VercelMCPClient

STITCH_DIR = Path("output/stitch")
REACT_DIR = Path("output/react/src/components")
BACKEND_DIR = Path("output/backend")


# ============================================================================
# Helpers de transformación de código (frontend)
# ============================================================================

def _strip_code_fences(text: str) -> str:
    """Quita los ``` ... ``` que el LLM a veces incluye."""
    text = text.strip()
    if text.startswith("```"):
        first_nl = text.find("\n")
        if first_nl != -1:
            text = text[first_nl + 1:]
    if text.endswith("```"):
        text = text[:-3].rstrip()
    return text.strip()


def _strip_module_syntax(jsx: str) -> str:
    """Convierte código JSX con imports/exports en código que Babel standalone
    puede ejecutar en browser (sin módulos ES)."""
    jsx = _strip_code_fences(jsx)

    out = []
    in_multiline_import = False
    for line in jsx.split("\n"):
        stripped = line.strip()
        if in_multiline_import:
            if ";" in stripped or "from " in stripped:
                in_multiline_import = False
            continue
        if stripped.startswith("import "):
            if ";" not in stripped:
                in_multiline_import = True
            continue
        if stripped.startswith("export default function"):
            line = line.replace("export default function", "function", 1)
        elif stripped.startswith("export default "):
            # "export default ComponentName;" → eliminar (la función ya existe)
            continue
        elif stripped.startswith("export function"):
            line = line.replace("export function", "function", 1)
        elif stripped.startswith("export const") or stripped.startswith("export let"):
            line = line.replace("export ", "", 1)
        out.append(line)
    return "\n".join(out).strip()


def _extract_component_name(jsx: str, fallback: str) -> str:
    """Detecta el nombre del componente React en el JSX."""
    m = re.search(r"function\s+([A-Z]\w*)\s*\(", jsx)
    if m:
        return m.group(1)
    m = re.search(r"const\s+([A-Z]\w*)\s*=", jsx)
    if m:
        return m.group(1)
    return fallback


def _build_react_page(screen_name: str, component_name: str, jsx_body: str) -> str:
    """Construye una página HTML self-contained con Tailwind + React + el JSX inline."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{screen_name}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gray-50 min-h-screen">
  <div id="root"></div>
  <script type="text/babel" data-presets="react">
    const {{ useState, useEffect, useRef, useCallback, useMemo, Fragment }} = React;

{jsx_body}

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<{component_name} />);
  </script>
</body>
</html>"""


def _build_index(screen_names: List[str], has_backend: bool) -> str:
    """Index con navegación a cada pantalla y enlace al endpoint backend."""
    links = "\n".join(
        f'      <li><a class="text-blue-600 hover:underline" href="{n}.html">📱 {n}</a></li>'
        for n in screen_names
    )
    backend_section = ""
    if has_backend:
        backend_section = """
      <h2 class="text-xl font-semibold mt-8 mb-3">Backend</h2>
      <ul class="space-y-2">
        <li><a class="text-blue-600 hover:underline" href="/api/index">🔌 GET /api/index</a> — código backend generado</li>
        <li><a class="text-blue-600 hover:underline" href="backend.py">📄 backend.py</a> — descarga el código FastAPI</li>
      </ul>"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gemelo Digital Financiero — App desplegada</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
  <main class="max-w-2xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold mb-2">🚀 Aplicación desplegada</h1>
    <p class="text-gray-600 mb-6">Generada automáticamente por el Gemelo Digital Financiero IA.</p>

    <h2 class="text-xl font-semibold mt-6 mb-3">Pantallas (React + Tailwind)</h2>
    <ul class="space-y-2">
{links}
    </ul>
    {backend_section}

    <footer class="mt-12 pt-6 border-t text-sm text-gray-500">
      Pipeline: Líder Técnico → Frontend (Stitch) → Backend (FastAPI) → Deploy (Vercel).
    </footer>
  </main>
</body>
</html>"""


# ============================================================================
# Helpers de backend (Vercel Python serverless)
# ============================================================================

def _build_api_handler(backend_code: str) -> str:
    """Construye un Vercel Python serverless function que sirve el código backend
    generado como text/plain. No intenta ejecutar el FastAPI directamente porque
    suele depender de DBs/configuración que no existen en serverless cold-start."""
    # Escapamos triples comillas para que quepa como string literal
    safe = backend_code.replace('"""', '\\"\\"\\"')
    return f'''from http.server import BaseHTTPRequestHandler

BACKEND_CODE = """{safe}"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(BACKEND_CODE.encode("utf-8"))
'''


def _build_vercel_json() -> str:
    return """{
  "version": 2,
  "builds": [
    {"src": "api/index.py", "use": "@vercel/python"},
    {"src": "*.html", "use": "@vercel/static"},
    {"src": "*.py", "use": "@vercel/static"}
  ]
}"""


def _build_requirements() -> str:
    return "fastapi\npydantic\n"


# ============================================================================
# Async runner (sin nest_asyncio, compatible con uvicorn/gradio)
# ============================================================================

def _run(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


# ============================================================================
# Entry point principal
# ============================================================================

def deploy_to_vercel(project_name: str = None, codigo: str = "") -> Dict:
    """Despliega la app completa a Vercel:
    - Frontend: páginas HTML con Tailwind+React montando los .jsx de output/react/.
      Si no hay JSX, fallback a los HTML crudos de output/stitch/.
    - Backend: si se pasa `codigo`, lo guarda en output/backend/main.py y lo incluye
      como api/index.py (serverless Python) + vercel.json + requirements.txt + backend.py.
    """
    project_name = project_name or Settings.VERCEL_PROJECT_NAME

    files_payload: List[Dict[str, str]] = []
    screen_names: List[str] = []

    # 1) Frontend desde JSX (preferido — Tailwind + React)
    if REACT_DIR.exists():
        for component_dir in sorted(REACT_DIR.iterdir()):
            if not component_dir.is_dir():
                continue
            jsx_files = list(component_dir.glob("*.jsx"))
            if not jsx_files:
                continue
            raw_jsx = jsx_files[0].read_text(encoding="utf-8", errors="ignore")
            cleaned = _strip_module_syntax(raw_jsx)
            comp_name = _extract_component_name(cleaned, component_dir.name)
            html = _build_react_page(component_dir.name, comp_name, cleaned)
            files_payload.append({"file": f"{component_dir.name}.html", "data": html})
            screen_names.append(component_dir.name)
            print(f"   🎨 React+Tailwind: {component_dir.name}.html ({comp_name})")

    # 2) Fallback: HTML crudo de Stitch si no hubo JSX
    if not files_payload and STITCH_DIR.exists():
        for f in sorted(STITCH_DIR.glob("*.html")):
            if f.name.lower() == "index.html":
                continue
            files_payload.append({"file": f.name, "data": f.read_text(encoding="utf-8")})
            screen_names.append(f.stem)
            print(f"   📄 Stitch HTML (fallback): {f.name}")

    if not files_payload:
        return {
            "url": None,
            "files": [],
            "error": "No hay frontend para desplegar (output/react/ y output/stitch/ vacíos).",
            "stub": True,
        }

    # 3) Backend (opcional)
    has_backend = bool(codigo and codigo.strip())
    if has_backend:
        backend_clean = _strip_code_fences(codigo)
        # Persistir en disco para inspección local
        BACKEND_DIR.mkdir(parents=True, exist_ok=True)
        (BACKEND_DIR / "main.py").write_text(backend_clean, encoding="utf-8")
        print(f"   💾 Backend guardado en {BACKEND_DIR / 'main.py'}")

        files_payload.append({"file": "api/index.py", "data": _build_api_handler(backend_clean)})
        files_payload.append({"file": "vercel.json", "data": _build_vercel_json()})
        files_payload.append({"file": "requirements.txt", "data": _build_requirements()})
        files_payload.append({"file": "backend.py", "data": backend_clean})

    # 4) Index de navegación
    files_payload.append({
        "file": "index.html",
        "data": _build_index(screen_names, has_backend),
    })

    client = VercelMCPClient()
    print(f"   📤 Subiendo {len(files_payload)} archivos a Vercel ({project_name})...")
    result = _run(client.deploy_static(project_name, files_payload))
    result["files"] = [f["file"] for f in files_payload]
    return result
