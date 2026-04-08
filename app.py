from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from graph.workflow import ejecutar_flujo

# Cargar variables de entorno
load_dotenv()

# Instancia de FastAPI
app = FastAPI(
    title="Gemelo Digital Financiero IA API",
    description="API para orquestar el flujo de agentes de inteligencia artificial para soluciones financieras.",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para el cuerpo de la petición
class RequerimientoRequest(BaseModel):
    requerimiento: str

# Endpoints
@app.get("/")
async def root():
    """
    Health check para verificar si el servidor está activo.
    """
    return {"message": "Bienvenido a la API del Gemelo Digital Financiero IA..."}

@app.post("/api/v1/ejecutar-flujo")
async def api_ejecutar_flujo(request: RequerimientoRequest):
    """
    Endpoint principal que orquesta todo el proceso desde la validación hasta la generación del entregable final.
    """
    if not request.requerimiento.strip():
        raise HTTPException(status_code=400, detail="El requerimiento no puede estar vacío.")

    try:
        # Llamar a la función que orquesta el flujo de agentes
        resultado = ejecutar_flujo(request.requerimiento)
        return resultado
    except Exception as e:
        # En caso de error de validación (por ejemplo, si el requerimiento no es financiero)
        # o cualquier otro error durante el flujo
        mensaje_error = str(e)
        if "Error de Validación" in mensaje_error or "❌" in mensaje_error:
            raise HTTPException(status_code=400, detail=f"Error de Validación: {mensaje_error}")
        
        # Otros errores internos
        raise HTTPException(status_code=500, detail=f"Error Interno del Servidor: {mensaje_error}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
