from aiopg.sa import create_engine


async def init_db_engine(conf, loop=None):
    return await create_engine(loop=loop, **conf)


def get_connection_string(conf):
    return f'postgres://{conf["user"]}:{conf["password"]}@{conf["host"]}:{conf["port"]}/{conf["database"]}'
