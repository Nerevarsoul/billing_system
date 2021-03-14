import logging
import uuid
from decimal import Decimal
from uuid import UUID

from asyncpg import CheckViolationError, ForeignKeyViolationError
from sqlalchemy.dialects.postgresql import insert

from app.db import database
from app.db.models import accounts, operation_history
from app.billing.entities import *


logger = logging.getLogger(__name__)


class BillingService:

    async def create_account(self, user_id: UUID) -> UUID:
        query = insert(accounts).values(
            id=str(uuid.uuid4()),
            user_id=user_id,
            amount=0
        ).on_conflict_do_nothing(
            constraint='accounts_user_id'
        ).returning(accounts.c.id)

        return await database.fetch_val(query)

    async def refill_deposit(self, charge: DepositRefill):
        async with database.transaction():
            try:
                amount = await self._update_account(charge.destination, charge.amount)
                await self._update_history(charge.destination, charge.amount)
                return amount
            except ForeignKeyViolationError:
                logging.error("Account %s doesn't exist", charge.destination)

    async def _update_account(self, account_id: UUID, amount: Decimal) -> Decimal:
        query = accounts.update().values(
            amount=accounts.c.amount + amount
        ).where(
            accounts.c.id == account_id
        ).returning(accounts.c.amount)

        return await database.fetch_val(query)

    async def _update_history(self, destination, amount, source=None):
        query = insert(operation_history).values(
            source=source,
            destination=destination,
            amount=amount
        )
        await database.execute(query)

    async def transfer(self, transfer: MoneyTransfer):
        async with database.transaction():
            try:
                amount = await self._update_account(transfer.source, -transfer.amount)
                await self._update_account(transfer.destination, transfer.amount)
                await self._update_history(transfer.destination, transfer.amount, transfer.source)
                return amount
            except CheckViolationError:
                logging.error("Account %s doesn't have %s $", transfer.source, transfer.amount)
