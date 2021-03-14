from sqlalchemy import (
    Table, MetaData, Column, DECIMAL, BigInteger, ForeignKey, UniqueConstraint, CheckConstraint,
    DateTime, func
)
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()


accounts = Table(
    'accounts', metadata,
    Column('id', UUID, primary_key=True),
    Column('user_id', UUID, nullable=False),
    Column('amount', DECIMAL, nullable=False),
    Column('time_created', DateTime(timezone=True), server_default=func.now()),
    Column('time_updated', DateTime(timezone=True), onupdate=func.now()),
    UniqueConstraint('user_id', name='accounts_user_id'),
    CheckConstraint('amount >= 0', name='check1')
)


operation_history = Table(
    'operation_history', metadata,
    Column('id', BigInteger, primary_key=True),
    Column(
        'source',
        UUID,
        ForeignKey('accounts.id', ondelete='CASCADE'),
        index=True,
        nullable=True
    ),
    Column(
        'destination',
        UUID,
        ForeignKey('accounts.id', ondelete='CASCADE'),
        index=True,
        nullable=False
    ),
    Column('amount', DECIMAL, nullable=False),
    Column('time_created', DateTime(timezone=True), server_default=func.now()),
)
