from sqlalchemy.orm import Session
from models import User, Address, Transaction, Price, Notification, NotificationLog
from schemas import UserCreate, AddressCreate, TransactionCreate, NotificationCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user: User, user_update):
    user.name = user_update.name
    user.email = user_update.email
    db.commit()
    db.refresh(user)
    return user

def create_address(db: Session, address: AddressCreate, user_id: int):
    db_address = Address(**address.dict(), user_id=user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()

def get_address(db: Session, address_id: int, user_id: int):
    return db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    address = db.query(Address).filter(Address.id == transaction.address_id).first()
    address.balance += transaction.amount
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, address_id: int):
    return db.query(Transaction).filter(Transaction.address_id == address_id).all()

def get_latest_price(db: Session, crypto: str):
    return db.query(Price).filter(Price.crypto == crypto).order_by(Price.last_updated.desc()).first()

def create_notification(db: Session, notification: NotificationCreate, user_id: int):
    db_notification = Notification(**notification.dict(), user_id=user_id, is_active=True)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).all()

def get_notification(db: Session, notification_id: int, user_id: int):
    return db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()

def toggle_notification(db: Session, notification: Notification):
    notification.is_active = not notification.is_active
    db.commit()
    return notification

def delete_notification(db: Session, notification: Notification):
    db.delete(notification)
    db.commit()

def get_notification_logs(db: Session, user_id: int):
    return db.query(NotificationLog).join(Notification).filter(Notification.user_id == user_id).order_by(NotificationLog.triggered_at.desc()).all()