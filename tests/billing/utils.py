import uuid


__all__ = ('create_account', 'refill_deposit', 'create_account')


def create_account(client, user_id=''):
    if not user_id:
        user_id = str(uuid.uuid4())
    return client.post(
        "/billing/create_account",
        json={
            'user_id': user_id
        }
    )


def refill_deposit(client, account_id, amount):
    return client.patch(
        "/billing/refill_deposit",
        json={
            'destination': account_id,
            'amount': amount
        }
    )



