from decimal import Decimal
from uuid import UUID

from pydantic import validator
from pydantic.main import BaseModel

__all__ = ('User', 'DepositRefill', 'MoneyTransfer',)


class User(BaseModel):
    user_id: UUID


class DepositRefill(BaseModel):
    destination: UUID
    amount: Decimal

    @validator('amount')
    def amount_must_be_greater_than_zero(cls, v):
        if v <= 0:
            raise ValueError('must be greater than zero')
        return v


class MoneyTransfer(DepositRefill):
    source: UUID
