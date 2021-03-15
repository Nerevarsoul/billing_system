import logging

from asyncpg import CheckViolationError, ForeignKeyViolationError
from fastapi import APIRouter, Response

from app.billing.entities import *
from app.billing.services import BillingService


logger = logging.getLogger(__name__)


account_router = APIRouter(
    prefix="/billing"
)


@account_router.post("/create_account", status_code=201)
async def create_account(user: User):
    service = BillingService()
    account_id = await service.create_account(user.user_id)

    return {"account_id": str(account_id)}


@account_router.patch("/refill_deposit")
async def refill_deposit(charge: DepositRefill, response: Response):
    service = BillingService()
    amount = await service.refill_deposit(charge)

    if amount is None:
        response.status_code = 400
        return {"error": f"Account with id={charge.destination} doesn't exist"}

    return {"amount": amount}


@account_router.patch("/transfer_money")
async def transfer_money(transfer: MoneyTransfer, response: Response):
    service = BillingService()

    try:
        amount = await service.transfer(transfer)
    except CheckViolationError:
        logging.error("Account %s doesn't have %s $", transfer.source, transfer.amount)
        response.status_code = 400
        return {
            "error": f"Account with id={transfer.source} doesn't have {transfer.amount}$"
        }
    except ForeignKeyViolationError:
        logging.error("Account with id=%s doesn't exist", transfer.destination)
        response.status_code = 400
        return {"error": f"Account with id={transfer.destination} doesn't exist"}

    return {"amount": amount}
