from pydantic import BaseModel, validator
from typing_extensions import Annotated
from pydantic.types import StringConstraints
from datetime import datetime
from enum import Enum
from models import AddressType, CryptoType, NotificationType

class UserCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    email: Annotated[str, StringConstraints(min_length=5, max_length=100, pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')]
    password: Annotated[str, StringConstraints(min_length=8, max_length=100)]

class UserUpdate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    email: Annotated[str, StringConstraints(min_length=5, max_length=100, pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')]

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    class Config:
        from_attributes = True  # Substitui orm_mode no Pydantic V2

class Token(BaseModel):
    access_token: str
    token_type: str

class AddressCreate(BaseModel):
    address: Annotated[str, StringConstraints(min_length=26, max_length=100, pattern=r'^[a-zA-Z0-9]+$')]
    type: AddressType

    @validator('address')
    def validate_address(cls, v, values):
        if 'type' in values:
            if values['type'] == AddressType.BTC and not v.startswith(('1', '3', 'bc1')):
                raise ValueError('Endereço BTC inválido')
            if values['type'] == AddressType.ETH and not v.startswith('0x'):
                raise ValueError('Endereço ETH inválido')
        return v

class AddressResponse(BaseModel):
    id: int
    address: str
    type: AddressType
    balance: float
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    address_id: int
    tx_hash: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    amount: float

class TransactionResponse(BaseModel):
    id: int
    tx_hash: str
    amount: float
    timestamp: datetime
    class Config:
        from_attributes = True

class BalanceResponse(BaseModel):
    address: str
    balance_usd: float
    balance_brl: float
    balance_crypto: float
    crypto_type: str

class PriceResponse(BaseModel):
    crypto: str
    price_usd: float
    price_brl: float
    last_updated: datetime
    class Config:
        from_attributes = True

class NotificationCreate(BaseModel):
    crypto_type: CryptoType
    notification_type: NotificationType
    threshold_value: float

class NotificationResponse(BaseModel):
    id: int
    crypto_type: str
    notification_type: str
    threshold_value: float
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class NotificationLogResponse(BaseModel):
    id: int
    crypto_type: str
    current_price_usd: float
    current_price_brl: float
    threshold_value: float
    triggered_at: datetime
    class Config:
        from_attributes = True