import aiohttp
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlalchemy.orm import Session
from models import Price, CryptoType
from config import COINGECKO_API_URL
from services.notification_service import check_notifications
import structlog

logger = structlog.get_logger()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_prices():
    """Fazer requisição assíncrona para a API da CoinGecko"""
    async with aiohttp.ClientSession() as session:
        async with session.get(COINGECKO_API_URL, timeout=10) as response:
            return await response.json()

def save_prices_to_db(data, db: Session):
    """Salvar preços no banco de dados"""
    logger.info("💾 Salvando preços no banco de dados...")
    try:
        db.add(Price(
            crypto=CryptoType.BTC, 
            price_usd=data["bitcoin"]["usd"],
            price_brl=data["bitcoin"]["brl"]
        ))
        db.add(Price(
            crypto=CryptoType.ETH, 
            price_usd=data["ethereum"]["usd"],
            price_brl=data["ethereum"]["brl"]
        ))
        db.commit()
        logger.info("✅ Preços salvos no banco de dados com sucesso")
        check_notifications(db, data)
    except Exception as e:
        logger.error(f"❌ Erro ao salvar preços no banco: {e}")
        db.rollback()

async def update_prices():
    """Tarefa em background para atualizar preços"""
    logger.info("🔄 Iniciando tarefa de atualização de preços em background...")
    await asyncio.sleep(10)  # Aguardar inicialização
    from main import SessionLocal  # Importação tardia para evitar dependência circular
    while True:
        try:
            data = await fetch_prices()
            logger.info(f"💰 Preços obtidos: BTC=${data['bitcoin']['usd']}/R${data['bitcoin']['brl']}, ETH=${data['ethereum']['usd']}/R${data['ethereum']['brl']}")
            db = SessionLocal()
            try:
                await asyncio.to_thread(save_prices_to_db, data, db)
            finally:
                db.close()
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar preços: {e}")
        await asyncio.sleep(300)  # Aguardar 5 minutos