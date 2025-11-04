from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.config.database import init_database
from app.utils.logger import log_info, log_error

# Crear instancia de FastAPI
app = FastAPI(
    title="Auth API",
    description="API de autenticación con registro y login",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router)

@app.on_event("startup")
async def startup_event():
    """Inicializa la base de datos al arrancar la aplicación"""
    try:
        log_info("Iniciando aplicación Auth API")
        init_database()
        log_info("Base de datos inicializada correctamente")
        log_info("Aplicación lista para recibir requests")
    except Exception as e:
        log_error("Error inicializando aplicación", error=e)
        raise

@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {
        "success": True,
        "message": "Auth API funcionando correctamente",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    log_info("Iniciando servidor en http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)