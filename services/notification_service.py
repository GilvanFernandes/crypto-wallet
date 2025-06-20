from sqlalchemy.orm import Session
from models import Notification, NotificationLog, CryptoType, NotificationType
import structlog

logger = structlog.get_logger()

def check_notifications(db: Session, price_data: dict):
    """Verificar e processar notificações em lotes"""
    logger.info("🔍 Verificando notificações ativas...")
    try:
        for crypto_type in [CryptoType.BTC, CryptoType.ETH]:
            current_price = price_data["bitcoin" if crypto_type == CryptoType.BTC else "ethereum"]["usd"]
            current_price_brl = price_data["bitcoin" if crypto_type == CryptoType.BTC else "ethereum"]["brl"]
            
            notifications = db.query(Notification).filter(
                Notification.is_active == True,
                Notification.crypto_type == crypto_type
            ).yield_per(100).all()

            triggered_logs = []
            for notification in notifications:
                triggered = False
                if notification.notification_type == NotificationType.GREATER_EQUAL:
                    triggered = current_price >= notification.threshold_value
                elif notification.notification_type == NotificationType.LESS_EQUAL:
                    triggered = current_price <= notification.threshold_value
                elif notification.notification_type == NotificationType.GREATER:
                    triggered = current_price > notification.threshold_value
                elif notification.notification_type == NotificationType.LESS:
                    triggered = current_price < notification.threshold_value
                elif notification.notification_type == NotificationType.EQUAL:
                    triggered = abs(current_price - notification.threshold_value) < 0.01
                
                if triggered:
                    triggered_logs.append(NotificationLog(
                        notification_id=notification.id,
                        crypto_type=notification.crypto_type,
                        current_price_usd=current_price,
                        current_price_brl=current_price_brl,
                        threshold_value=notification.threshold_value
                    ))
            
            if triggered_logs:
                db.add_all(triggered_logs)
                logger.info(f"🚨 {len(triggered_logs)} notificação(ões) disparada(s) para {crypto_type.value}")
        
        if triggered_logs:
            db.commit()
            logger.info(f"✅ {len(triggered_logs)} notificação(ões) processada(s)")
        else:
            logger.info("✅ Nenhuma notificação foi atingida")
    
    except Exception as e:
        logger.error(f"❌ Erro ao verificar notificações: {e}")
        db.rollback()