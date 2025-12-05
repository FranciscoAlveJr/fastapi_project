from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project.database import get_session
from fastapi_project.models import User
from fastapi_project.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_project.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: T_Session):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='User already exists', status_code=HTTPStatus.CONFLICT
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList, status_code=HTTPStatus.OK)
async def read_users(
    session: T_Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):
    users = await session.scalars(
        select(User).limit(filter_users.limit).offset(filter_users.offset)
    )
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
async def read_user(
    user_id: int,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    if not current_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return current_user


@router.put('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        # session.add(db_user)
        await session.commit()
        await session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
async def delete_user(
    user_id: int,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    if not current_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    await session.delete(current_user)
    await session.commit()

    return Message(message='User deleted')
