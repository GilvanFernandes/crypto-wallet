from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from models import Price, CryptoType
from schemas import PriceResponse
from dependencies import get_db

router = APIRouter()

@router.get("/status")
def get_status(db: Session = Depends(get_db)):
    """Verificar status do sistema e últimos preços atualizados"""
    try:
        latest_btc = db.query(Price).filter(Price.crypto == CryptoType.BTC).order_by(Price.last_updated.desc()).first()
        latest_eth = db.query(Price).filter(Price.crypto == CryptoType.ETH).order_by(Price.last_updated.desc()).first()
        return {
            "status": "online",
            "database": "connected",
            "price_updates": {
                "btc": {
                    "price_usd": latest_btc.price_usd if latest_btc else None,
                    "price_brl": latest_btc.price_brl if latest_btc else None,
                    "last_updated": latest_btc.last_updated if latest_btc else None
                },
                "eth": {
                    "price_usd": latest_eth.price_usd if latest_eth else None,
                    "price_brl": latest_eth.price_brl if latest_eth else None,
                    "last_updated": latest_eth.last_updated if latest_eth else None
                }
            },
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Erro ao verificar status: {e}")
        return {"status": "error", "message": str(e)}