from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.protected import router as protected_router
from app.routes.municipalities import router as municipalities_router
from app.routes.businesses import router as businesses_router
from app.routes.user import router as user_router
from app.routes.menu_simple import router as menu_router
from app.routes.rewards import router as rewards_router
from app.routes.business_portal import router as business_portal_router
from app.routes.loyalty import router as loyalty_router
from app.routes.admin import router as admin_router
from app.routes.notifications import router as notifications_router
from app.services.websocket_service import websocket_service
from app.config.database_sqlite import init_database
from app.utils.logger import log_info, log_error

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación"""
    try:
        log_info("Iniciando aplicación Auth API")
        init_database()
        log_info("Base de datos inicializada correctamente")
        log_info("Aplicación lista para recibir requests")
    except Exception as e:
        log_error("Error inicializando aplicación", error=e)
        raise
    
    yield
    
    # Cleanup al cerrar la aplicación
    log_info("Cerrando aplicación Auth API")

# Crear instancia de FastAPI
app = FastAPI(
    title="Auth API",
    description="API de autenticación con registro y login",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(municipalities_router)
app.include_router(businesses_router)
app.include_router(user_router)
app.include_router(menu_router)
app.include_router(rewards_router)
app.include_router(business_portal_router)
app.include_router(loyalty_router)
app.include_router(notifications_router)
app.include_router(admin_router)

# Montar WebSocket
app.mount("/ws", websocket_service.get_asgi_app())



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
    log_info("Iniciando servidor en http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)