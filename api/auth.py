from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from api.models import UserInDbModel
from constants import CONF
from db.driver import DbDriver
from utils import now

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='token')


class Password:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def verify(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_hash(cls, password):
        return cls.pwd_context.hash(password)


async def get_user(email: str):
    user = await DbDriver.UserData.get(email=email)
    return None if user is None else UserInDbModel(**user)


async def get_current_user(token: str = Depends(OAUTH2_SCHEME)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials.',
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, CONF['jwt']['secret_key'], [CONF['jwt']['algorithm']])
    except JWTError:
        raise credentials_exception

    email: str = payload.get('sub')
    if email is None:
        raise credentials_exception

    user = await get_user(email=email)
    if user is None:
        raise credentials_exception

    await DbDriver.UserData.update_last_request_at(id_=user.id)

    return user


async def authenticate_user(email: str, password: str):
    user = await get_user(email=email)
    if (
            user is None
            or
            not Password.verify(plain_password=password, hashed_password=user.password_hash)
    ):
        result = False
    else:
        await DbDriver.UserData.update_last_login_at(id_=user.id)
        result = user
    return result


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode['exp'] = now() + expires_delta
    encoded_jwt = jwt.encode(to_encode, CONF['jwt']['secret_key'], CONF['jwt']['algorithm'])
    return encoded_jwt
