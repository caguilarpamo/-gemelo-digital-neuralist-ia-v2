"""
Cliente HTTP al API de Vercel para deploys automáticos.

Usa el endpoint oficial POST /v13/deployments con Bearer token. Si VERCEL_TOKEN
no está configurado o la llamada falla, devuelve una URL stub marcada para que
el pipeline del hackathon no se rompa durante la demo.

Patrón paralelo a tools/stitch_client.py para coherencia del proyecto.
"""
import os
import uuid
import traceback
from typing import Dict, List, Optional

import httpx


class VercelMCPClient:
    """Cliente mínimo async al API REST de Vercel (deployments v13)."""

    def __init__(self, token: Optional[str] = None, timeout: float = 120.0):
        self.token = token or os.getenv("VERCEL_TOKEN")
        self.base_url = "https://api.vercel.com"
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def deploy_static(self, name: str, files: List[Dict[str, str]]) -> Dict:
        """
        Despliega un sitio estático a Vercel.

        Args:
            name: nombre del proyecto Vercel.
            files: lista de {"file": "ruta/en/proyecto.html", "data": "<contenido utf-8>"}.

        Returns:
            dict con: url (https://...), id, readyState, stub (bool), error (opcional).
        """
        if not self.token:
            stub_url = f"https://{name}-stub-{uuid.uuid4().hex[:6]}.vercel.app"
            print(f"   ⚠️ VERCEL_TOKEN ausente — URL stub: {stub_url}")
            return {"url": stub_url, "stub": True}

        payload = {
            "name": name,
            "files": files,
            "projectSettings": {
                "framework": None,
                "buildCommand": None,
                "outputDirectory": None,
                "installCommand": None,
            },
            "target": "production",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/v13/deployments",
                    headers=self._headers(),
                    json=payload,
                )
                if resp.status_code >= 400:
                    err = resp.text[:400]
                    print(f"   ⚠️ Vercel {resp.status_code}: {err}")
                    return {
                        "url": f"https://{name}-error-{uuid.uuid4().hex[:6]}.vercel.app",
                        "error": err,
                        "stub": True,
                    }
                data = resp.json()
                url = data.get("url", "")
                if url and not url.startswith("http"):
                    url = f"https://{url}"
                return {
                    "url": url,
                    "id": data.get("id"),
                    "readyState": data.get("readyState"),
                    "stub": False,
                }
        except Exception as e:
            traceback.print_exc()
            return {
                "url": f"https://{name}-exception-{uuid.uuid4().hex[:6]}.vercel.app",
                "error": str(e),
                "stub": True,
            }
