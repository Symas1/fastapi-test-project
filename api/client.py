import aiohttp

from api.models import UserCreateModel, PostCreateModel, LikeCreateDeleteModel
from constants import CONF


class Client:
    base_url = CONF['client']['url']
    session = aiohttp.ClientSession()

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {'Authorization': self.access_token}

    @classmethod
    async def signup(cls, user: UserCreateModel):
        url = f'{cls.base_url}/users'
        result = await cls._post(url=url, json=user.dict())
        return result

    async def create_post(self, post: PostCreateModel):
        url = f'{self.base_url}/posts'
        result = await self._post(url=url, json=post.dict(), headers=self.headers)
        return result

    async def like_post(self, like: LikeCreateDeleteModel):
        url = f'{self.base_url}/likes'
        result = await self._post(url=url, json=like.dict(), headers=self.headers)
        return result

    @classmethod
    async def get_token(cls, username, password):
        url = f'{cls.base_url}/token'
        data = {'username': username, 'password': password}
        result = await cls._post(url=url, data=data)
        return f'{result["token_type"].capitalize()} {result["access_token"]}'

    @classmethod
    async def _request(cls, method, url, headers=None, params: dict = None, data: dict = None, json: dict = None):
        # params - query params
        # data - form-data params
        async with cls.session.request(
                method=method, url=url, headers=headers, params=params, data=data, json=json
        ) as response:
            response.raise_for_status()
            result = await response.json()
        return result

    @classmethod
    async def _get(cls, url, headers=None, params=None, data=None):
        result = await cls._request(method='GET', url=url, headers=headers, params=params, data=data)
        return result

    @classmethod
    async def _post(cls, url, headers=None, params=None, data=None, json=None):
        result = await cls._request(method='POST', url=url, headers=headers, params=params, data=data, json=json)
        return result
