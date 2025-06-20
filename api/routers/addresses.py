from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Address
from schemas import AddressCreate, AddressResponse, TransactionCreate, TransactionResponse, BalanceResponse
from crud import create_address, get_addresses, get_address, create_transaction, get_transactions, get_latest_price
from dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=AddressResponse)
def create_address_route(address: AddressCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Criar novo endereço para o usuário"""
    return create_address(db, address, user.id)

@router.get("/", response_model=list[AddressResponse])
def list_addresses_route(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Listar endereços do usuário"""
    return get_addresses(db, user.id)

@router.post("/transactions", response_model=TransactionResponse)
def create_transaction_route(transaction: TransactionCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Criar nova transação"""
    address = get_address(db, transaction.address_id, user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return create_transaction(db, transaction)

@router.get("/{address_id}/transactions", response_model=list[TransactionResponse])
def get_transactions_route(address_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Listar transações de um endereço"""
    address = get_address(db, address_id, user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return get_transactions(db, address_id)

@router.get("/{address_id}/balance", response_model=BalanceResponse)
def get_balance_route(address_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Obter saldo de um endereço"""
    address = get_address(db, address_id, user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    price = get_latest_price(db, address.type)
    if not price:
        raise HTTPException(status_code=404, detail="Dados de preço não disponíveis")
    balance_usd = address.balance * price.price_usd
    balance_brl = address.balance * price.price_brl
    return {
        "address": address.address,
        "balance_usd": balance_usd,
        "balance_brl": balance_brl,
        "balance_crypto": address.balance,
        "crypto_type": address.type.value
    }