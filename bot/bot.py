import asyncio
from pathlib import Path
from random import randint
from random import sample
from uuid import uuid4

from api.client import Client
from api.models import UserCreateModel, PostCreateModel, LikeCreateDeleteModel
from config.utils import load_conf


def mock_users(n_users):
    users = []
    for _ in range(n_users):
        email = f'{str(uuid4())[:12]}@example.com'
        password = str(uuid4())
        users.append(UserCreateModel(email=email, password=password))
    return users


async def run(conf_path):
    conf = load_conf(filepath=conf_path)
    n_users = conf['number_of_users']
    max_posts_per_user = conf['max_posts_per_user']
    max_likes_per_user = conf['max_likes_per_user']

    users = mock_users(n_users=n_users)
    user_ids = [
        user['id']
        for user in await asyncio.gather(*[Client.signup(user=user) for user in users])
    ]

    tokens = await asyncio.gather(*[
        Client.get_token(username=user.email, password=user.password)
        for user in users
    ])

    clients = [Client(access_token=token) for token in tokens]
    post_ids = []
    for client in clients:
        new_post_ids = await asyncio.gather(*[
            client.create_post(post=PostCreateModel())
            for _ in range(randint(0, max_posts_per_user))
        ])
        post_ids.extend([new_post_id['id'] for new_post_id in new_post_ids])

    like_tasks = []
    for client, user_id in zip(clients, user_ids):
        n_likes = randint(0, min(len(post_ids), max_likes_per_user))
        posts_to_like = sample(post_ids, n_likes)
        like_tasks.append(
            asyncio.gather(*[
                client.like_post(like=LikeCreateDeleteModel(post_id=post_id, user_id=user_id))
                for post_id in posts_to_like
            ])
        )
    else:
        await asyncio.gather(*like_tasks)


if __name__ == '__main__':
    conf_path = Path.cwd() / 'bot' / 'config.yml'
    asyncio.get_event_loop().run_until_complete(run(conf_path=conf_path))
