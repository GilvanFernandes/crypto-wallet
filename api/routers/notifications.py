from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import NotificationCreate, NotificationResponse, NotificationLogResponse
from crud import create_notification, get_notifications, get_notification, toggle_notification, delete_notification, get_notification_logs
from dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
def create_notification_route(notification: NotificationCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Criar nova notificação de preço"""
    return create_notification(db, notification, user.id)

@router.get("/", response_model=list[NotificationResponse])
def list_notifications_route(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Listar notificações do usuário"""
    return get_notifications(db, user.id)

@router.put("/{notification_id}/toggle")
def toggle_notification_route(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Ativar/desativar notificação"""
    notification = get_notification(db, notification_id, user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    toggle_notification(db, notification)
    return {"message": f"Notificação {'ativada' if notification.is_active else 'desativada'} com sucesso"}

@router.delete("/{notification_id}")
def delete_notification_route(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Deletar notificação"""
    notification = get_notification(db, notification_id, user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    delete_notification(db, notification)
    return {"message": "Notificação deletada com sucesso"}

@router.get("/logs", response_model=list[NotificationLogResponse])
def get_notification_logs_route(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Listar logs de notificações do usuário"""
    return get_notification_logs(db, user.id)