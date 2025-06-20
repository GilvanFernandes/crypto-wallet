from fastapi import FastAPI
from sqlalchemy import text
from models import Base
from dependencies import SessionLocal, engine
from api.routers import users, addresses, notifications, prices
from services.price_service import update_prices
import asyncio
import structlog
import logging
from datetime import datetime

# Configuração do logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)
logger = structlog.get_logger()
logging.getLogger().setLevel(logging.WARNING)

app = FastAPI()

# Registrar rotas
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(addresses.router, prefix="/addresses", tags=["addresses"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
app.include_router(prices.router, prefix="/prices", tags=["prices"])

@app.get("/health")
def health_check():
    """Verificar se a aplicação está funcionando"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.on_event("startup")
async def startup_event():
    """Inicializar aplicação"""
    logger.info("=== INICIANDO APLICAÇÃO ===")
    try:
        # Testar conexão com banco
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("✅ Conexão com banco de dados OK")
        # Iniciar tarefa de atualização de preços
        asyncio.create_task(update_prices())
        logger.info("✅ Sistema de atualização de preços iniciado")
    except Exception as e:
        logger.warning(f"⚠️ Banco de dados não disponível: {e}")
    logger.info("=== APLICAÇÃO PRONTA ===")

# Criar tabelas no banco
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)