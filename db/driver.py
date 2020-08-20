from sqlalchemy import create_engine, select, and_

from constants import CONF
from db.tables import user_data_table, post_table, like_table
from db.utils import get_connection_string, init_db_engine
from utils import now


class DbDriver:
    engine = create_engine(get_connection_string(conf=CONF['database']))
    aioengine = None

    @classmethod
    async def get_aioengine(cls):
        if not cls.aioengine:
            cls.aioengine = await init_db_engine(conf=CONF['database'])
        return cls.aioengine

    class Like:
        @staticmethod
        async def insert(user_data_id, post_id):
            statement = (
                like_table
                    .insert()
                    .values(user_data_id=user_data_id, post_id=post_id)
                    .returning(like_table.c.user_data_id, like_table.c.post_id)
            )
            async with (await DbDriver.get_aioengine()).acquire() as conn:
                result_proxy = await conn.execute(statement)
                result = await result_proxy.fetchone()
            return dict(result)

        @staticmethod
        async def delete(user_data_id, post_id):
            statement = (
                like_table
                    .delete()
                    .where(
                    and_(
                        user_data_id == user_data_id,
                        post_id == post_id
                    )
                )
            )
            async with (await DbDriver.get_aioengine()).acquire() as conn:
                await conn.execute(statement)

        @staticmethod
        async def analytics(date_from, date_to):
            query = f"""
                    SELECT COUNT(*) n_likes
                    FROM \"like\"
                    WHERE \"date\" BETWEEN {str(date_from)!r} AND {str(date_to)!r};
                    """
            async with (await DbDriver.get_aioengine()).acquire() as conn:
                result_proxy = await conn.execute(query)
                result = await result_proxy.scalar()
            return result

    class Post:
        @staticmethod
        async def insert(user_data_id):
            statement = (
                post_table
                    .insert()
                    .values(user_data_id=user_data_id)
                    .returning(post_table.c.id)
            )
            async with (await DbDriver.get_aioengine()).acquire() as conn:
                result_proxy = await conn.execute(statement)
                result = await result_proxy.fetchone()
            return dict(result)

    class UserData:
        @staticmethod
        async def get(email, fields=(user_data_table,)):
            statement = select(fields).where(user_data_table.c.email == email)
            async with (await DbDriver.get_aioengine()).acquire() as conn:
                result_proxy = await conn.execute(statement)
                result = await result_proxy.fetchone()
            result = dict(result)
            return result

        @staticmethod
        async def get_by_id(id_, fields=(user_data_table,)):
            statement = select(fields).where(user_data_table.c.id == id_)
            async with (await DbDriver.get_aioengine()).acquire() as conn:
                result_proxy = await conn.execute(statement)
                result = await result_proxy.fetchone()
            result = dict(result)
            return result

        @staticmethod
        async def insert(email, password_hash):
            statement = (
                user_data_table
                    .insert()
                    .values(email=email, password_hash=password_hash)
                    .returning(user_data_table.c.id)
            )
            async with (await DbDriver.get_aioengine()).acquire() as conn:
                result_proxy = await conn.execute(statement)
                result = await result_proxy.fetchone()
            return dict(result)

        @staticmethod
        async def update(id_, **values):
            statement = (
                user_data_table
                    .update()
                    .where(user_data_table.c.id == id_)
                    .values(**values)
            )
            async with (await DbDriver.get_aioengine()).acquire() as conn:
                await conn.execute(statement)

        @classmethod
        async def update_last_login_at(cls, id_, last_login_at=None):
            last_login_at = last_login_at or now()
            result = await cls.update(id_=id_, last_login_at=last_login_at)
            return result

        @classmethod
        async def update_last_request_at(cls, id_, last_request_at=None):
            last_request_at = last_request_at or now()
            result = await cls.update(id_=id_, last_request_at=last_request_at)
            return result
