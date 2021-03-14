import uuid

import pytest

from tests.billing.utils import create_account, refill_deposit


def test_create_account(client):
    response = create_account(client)
    assert response.status_code == 201
    assert 'account_id' in response.json()


def test_create_duplicate_account(client):
    user_id = str(uuid.uuid4())
    create_account(client, user_id)
    response = create_account(client, user_id)
    assert response.status_code == 201
    assert 'account_id' in response.json()


def test_put_money(client):
    response = create_account(client)
    account_id = response.json()['account_id']

    response = refill_deposit(client, account_id, 250)
    assert response.status_code == 200
    assert response.json()['amount'] == 250


def test_put_money_bad_request(client):
    response = refill_deposit(client, '', 250)
    assert response.status_code == 422


def test_put_money_to_non_exist_account(client):
    response = refill_deposit(client, str(uuid.uuid4()), 250)
    assert response.status_code == 400


def test_put_negative_money(client):
    response = create_account(client)
    account_id = response.json()['account_id']

    response = refill_deposit(client, account_id, -250)
    assert response.status_code == 422


@pytest.mark.parametrize('amount', [200, 400])
def test_transfer_money(client, amount):
    response = create_account(client)
    account_id = response.json()['account_id']

    response = create_account(client)
    account_to = response.json()['account_id']

    refill_deposit(client, account_id, 400)

    response = client.patch(
        "/billing/transfer_money",
        json={
            'source': account_id,
            'destination': account_to,
            'amount': amount
        }
    )

    assert response.status_code == 200
    assert response.json()['amount'] == 400 - amount


def test_transfer_money_neg(client):
    response = create_account(client)
    account_id = response.json()['account_id']

    response = create_account(client)
    account_to = response.json()['account_id']

    refill_deposit(client, account_id, 250)

    response = client.patch(
        "/billing/transfer_money",
        json={
            'source': account_id,
            'destination': account_to,
            'amount': 300
        }
    )

    assert response.status_code == 400


def test_transfer_money_neg_no_add_money(client):
    response = create_account(client)
    account_id = response.json()['account_id']

    response = create_account(client)
    account_to = response.json()['account_id']

    refill_deposit(client, account_id, 250)

    client.patch(
        "/billing/transfer_money",
        json={
            'source': account_id,
            'destination': account_to,
            'amount': 300
        }
    )

    response = refill_deposit(client, account_to, 200)
    assert response.status_code == 200
    assert response.json()['amount'] == 200
