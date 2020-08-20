from datetime import timedelta, date

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from psycopg2 import Error

from api.auth import create_access_token, Password, authenticate_user, get_current_user
from api.models import (
    TokenModel,
    UserCreateModel,
    PostCreateModel,
    UserInDbModel,
    UserActivityModel,
    UserCreatedModel,
    PostCreatedModel,
    LikeCreateDeleteModel
)
from constants import CONF
from db.driver import DbDriver

ROUTER = APIRouter()


@ROUTER.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserCreatedModel)
async def signup(user: UserCreateModel):
    # todo: add email validation
    password_hash = Password.get_hash(password=user.password)
    user_data = await DbDriver.UserData.insert(email=user.email, password_hash=password_hash)
    return UserCreatedModel(id=user_data['id'])


@ROUTER.get('/users/{user_id}/activity', dependencies=[Depends(get_current_user)], response_model=UserActivityModel)
async def get_user_activity(user_id):
    user = await DbDriver.UserData.get_by_id(id_=user_id)
    return UserActivityModel(**user)


@ROUTER.post('/token', response_model=TokenModel)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(
        data={'sub': user.email},  # 'sub' should be unique across the app
        expires_delta=timedelta(minutes=CONF['jwt']['access_token_expire_minutes'])
    )
    return {'access_token': access_token, 'token_type': 'bearer'}  # mandatory return, don't change


@ROUTER.post('/posts', status_code=status.HTTP_201_CREATED, response_model=PostCreatedModel)
async def create_post(post: PostCreateModel, user: UserInDbModel = Depends(get_current_user)):
    new_post = await DbDriver.Post.insert(user_data_id=user.id, **post.dict())
    return PostCreatedModel(id=new_post['id'])


@ROUTER.post(
    '/likes',
    status_code=status.HTTP_201_CREATED,
    response_model=LikeCreateDeleteModel,
    dependencies=[Depends(get_current_user)]
)
async def like_post(like: LikeCreateDeleteModel):
    try:
        new_like = await DbDriver.Like.insert(user_data_id=like.user_id, post_id=like.post_id)
        return LikeCreateDeleteModel(user_id=new_like['user_data_id'], post_id=new_like['post_id'])
    except Error as e:
        if e.pgcode == '23505':  # unique_violation
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder({'detail': 'You\'ve already liked the post.'}),
            )
        else:
            raise


@ROUTER.delete('/likes', status_code=status.HTTP_200_OK)
async def dislike_post(like: LikeCreateDeleteModel, user: UserInDbModel = Depends(get_current_user)):
    await DbDriver.Like.delete(user_data_id=user.id, post_id=like.post_id)


@ROUTER.get('/analytics/likes', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def analytics_likes(date_from: date, date_to: date):
    n_likes = await DbDriver.Like.analytics(date_from=date_from, date_to=date_to)
    return {'n_likes': n_likes}
