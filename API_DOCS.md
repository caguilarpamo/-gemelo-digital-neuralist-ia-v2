# Documentación de API: Gemelo Digital Financiero IA

Esta documentación detalla los endpoints disponibles para interactuar con el backend del sistema "Gemelo Digital Financiero IA" desde un frontend como React.

## ⚙️ Configuración del Servidor

- **Host predeterminado:** `localhost` o `0.0.0.0`
- **Puerto:** `8000`
- **Base URL:** `http://localhost:8000`

---

## 🛠 Endpoints

### 1. Root / Health Check
Verifica si el servidor está activo.

- **URL:** `/`
- **Método:** `GET`
- **Respuesta Exitosa (200 OK):**
    ```json
    {
      "message": "Bienvenido a la API del Gemelo Digital Financiero IA..."
    }
    ```

### 2. Ejecutar Flujo de Agentes
Este es el endpoint principal que orquesta todo el proceso desde la validación hasta la generación del entregable final.

- **URL:** `/api/v1/ejecutar-flujo`
- **Método:** `POST`
- **Cuerpo de la Petición (JSON):**
    | Campo | Tipo | Descripción |
    | :--- | :--- | :--- |
    | `requerimiento` | `string` | Descripción detallada de la necesidad financiera (ej: "Sistema de préstamos"). |

    **Ejemplo de Request:**
    ```json
    {
      "requerimiento": "Necesito una plataforma para gestionar microcréditos para emprendedores rurales."
    }
    ```

- **Respuesta Exitosa (200 OK):**
    Retorna un objeto con los 10 campos generados por los agentes.
    ```json
    {
      "historias": "...",
      "analisis": "...",
      "arquitectura": "...",
      "plan_tecnico": "...",
      "codigo": "...",
      "qa1": "...",
      "qa2": "...",
      "documentacion": "...",
      "despliegue": "...",
      "entregable": "..."
    }
    ```

- **Errores Posibles:**
    - **400 Bad Request:** Ocurre cuando el `ValidadorAgent` determina que el requerimiento no es financiero.
      ```json
      {
        "detail": "Error de Validación: ❌ Requerimiento no financiero"
      }
      ```
    - **500 Internal Server Error:** Ocurre si hay un error inesperado durante la ejecución (error de red con Anthropic, etc.).

---

## 💻 Consumo desde React (Ejemplo)

```javascript
const generarFlujo = async (requerimiento) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/ejecutar-flujo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ requerimiento }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al procesar el requerimiento');
    }

    const data = await response.json();
    console.log("Resultado del flujo:", data);
    return data;
  } catch (err) {
    console.error("Error en la petición:", err.message);
  }
};
```

## 📝 Notas Importantes
1. **Tiempo de Espera:** Dado que el sistema utiliza múltiples LLMs en cadena, la respuesta puede tardar entre 20 y 60 segundos. Se recomienda manejar un "Loading Spinner" en el frontend.
2. **CORS:** El servidor ya tiene habilitado CORS para permitir peticiones desde cualquier origen (`*`). En entornos de producción reales, se debe restringir al dominio de la App React.
3. **Documentación Interactiva:** Una vez que el servidor esté corriendo, puedes acceder a `http://localhost:8000/docs` para probar los endpoints interactivamente con Swagger UI.
