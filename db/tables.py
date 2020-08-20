import sqlalchemy.types as sa_types
from sqlalchemy.schema import (
    MetaData,
    Table,
    Column,
    ForeignKey,
    UniqueConstraint
)

from utils import now

METADATA = MetaData()

user_data_table = Table(
    'user_data',
    METADATA,
    Column('id', sa_types.BigInteger, primary_key=True, nullable=False),
    Column('email', sa_types.String(length=60), nullable=False, unique=True),
    Column('password_hash', sa_types.String(length=60), nullable=False),
    Column('created_at', sa_types.DateTime, nullable=False, default=now),
    Column('last_login_at', sa_types.DateTime, nullable=True),
    Column('last_request_at', sa_types.DateTime, nullable=True)
)

post_table = Table(
    'post',
    METADATA,
    Column('id', sa_types.BigInteger, primary_key=True, nullable=False),
    Column('user_data_id', ForeignKey('user_data.id', ondelete='CASCADE'), nullable=False)
)

like_table = Table(
    'like',
    METADATA,
    Column('user_data_id', ForeignKey('user_data.id', ondelete='CASCADE'), nullable=False),
    Column('post_id', ForeignKey('post.id', ondelete='CASCADE'), nullable=False),
    Column('date', sa_types.Date, nullable=False, default=now().date()),
    UniqueConstraint('user_data_id', 'post_id')
)
