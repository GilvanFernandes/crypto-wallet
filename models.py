from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Enum, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

Base = declarative_base()

class AddressType(enum.Enum):
    BTC = "BTC"
    ETH = "ETH"

class CryptoType(enum.Enum):
    BTC = "BTC"
    ETH = "ETH"

class NotificationType(enum.Enum):
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    GREATER = ">"
    LESS = "<"
    EQUAL = "=="

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    addresses = relationship("Address", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String(100), nullable=False)
    type = Column(Enum(AddressType), nullable=False)
    balance = Column(Float, default=0.0)  # Saldo pré-calculado
    user = relationship("User", back_populates="addresses")
    transactions = relationship("Transaction", back_populates="address")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    tx_hash = Column(String(100), unique=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    address = relationship("Address", back_populates="transactions")

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    crypto = Column(Enum(CryptoType), nullable=False)
    price_usd = Column(Float, nullable=False)
    price_brl = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        Index('idx_price_crypto_last_updated', 'crypto', 'last_updated'),
    )

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    crypto_type = Column(Enum(CryptoType), nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    threshold_value = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="notifications")

class NotificationLog(Base):
    __tablename__ = "notification_logs"
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("notifications.id"))
    crypto_type = Column(Enum(CryptoType), nullable=False)
    current_price_usd = Column(Float, nullable=False)
    current_price_brl = Column(Float, nullable=False)
    threshold_value = Column(Float, nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    notification = relationship("Notification")