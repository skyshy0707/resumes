from sqlalchemy import insert, delete, select, update, inspect, and_, or_
from sqlalchemy.exc import NoResultFound, SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.__init__ import ColumnProperty, DeclarativeMeta

from core import responses
from db.engine import connection
from db import models


from core.logger import setup_logger

logger = setup_logger(__name__)

get_fields = lambda model: [col.key for col in inspect(model).attrs if isinstance(col, ColumnProperty)]

@connection()
async def get_resource(session: AsyncSession, model: DeclarativeMeta, **pks):


    for param, value in pks.items():
        logger.info(f"Type of {param} is {type(value)}")

    #ColumnElement.match
    cols_cls = [
        getattr(model, field_name) == value for field_name, value in pks.items()
    ]

    return (
        await session.execute(select(model).where(*cols_cls))
    ).scalar_one_or_none()

@connection()
async def get_user(session: AsyncSession, **pks):
    email = pks.get("email")
    id = pks.get("id", pks.get("user_id"))

    exp = or_(models.User.id == id, models.User.email == email)
    return (
        await session.execute(select(models.User).where(exp))
    ).scalar_one_or_none()


@connection()
async def get_jwt_token(session: AsyncSession, token: str):

    instance: models.JWTToken = (
        await session.execute(
            select(models.JWTToken).\
                where(
                    or_(
                        models.JWTToken.token==token, 
                        models.JWTToken.refresh_token==token
                    )
                )
            )
        ).scalar_one_or_none()

    if instance is None:
        return None

    instance.grant_access = True

    if instance.refresh_token == token:
        instance.grant_access = False

    return instance
    

@connection(commit=True)
async def get_or_create_user_agent(session: AsyncSession, user_agent: dict):
    id_ = (
         await session.execute(
            select(models.UserAgent).where(
                models.UserAgent.info == user_agent.get("info"),
                models.UserAgent.user_id == user_agent.get("user_id")
            )
        )
    ).scalar_one_or_none().id

    if not id_:
        id_ = (
            await session.execute(insert(models.UserAgent).values(**user_agent))
        ).inserted_primary_key
    return id_


@connection()
async def get_user_agent_by_id(session: AsyncSession, id: int):

    return (
        await session.execute(
            select(models.UserAgent).where(
                models.UserAgent.id == id
            )
        )
    ).scalar_one_or_none()



@connection()
async def get_jwt_token_by_pk(session: AsyncSession, pk: int):

    try:
        instance = (
            await session.execute(
                select(models.JWTToken).where(models.JWTToken.token == pk)
            )
        ).scalar_one_or_none()
    
    except SQLAlchemyError as e:
        raise responses.DATA_ERROR(e._message())
    return instance



@connection(commit=True)
async def create_jwt_token(session: AsyncSession, jwt_token):
    try:
        instance = (
            await session.execute(insert(models.JWTToken).values(**jwt_token).returning(models.JWTToken))
        ).scalar_one_or_none()

    except SQLAlchemyError as e:
        raise responses.DATA_ERROR(e._message())
    return instance

@connection(commit=True)
async def update_jwt_token(session: AsyncSession, jwt_token):

    try:
        instance = (
            await session.execute(
                update(models.JWTToken).values(**jwt_token)\
                    .where(models.JWTToken.user_agent_id==jwt_token.get("user_agent_id")).returning(models.JWTToken)
            )
        ).scalar_one_or_none()

        logger.info(f"Instance user_id sync:{instance.user_id}")

    except IntegrityError as e:
        return None
    return instance


@connection(commit=True)
async def create_user(session: AsyncSession, user):
    try:
        return (
            await session.execute(
                insert(models.User).values(**user)
            )
        ).inserted_primary_key
    except IntegrityError as e:
        if "unique" in e._message().lower():
            raise responses.CONFLICT("User is exist.")
    

@connection(commit=True)
async def create_resume(session: AsyncSession, resume):
    return (
        await session.execute(
            insert(models.Resume).values(**resume.model_dump())
        )
    ).inserted_primary_key

@connection()
async def get_resume(session: AsyncSession, id: int):
    try:
        instance = await session.execute(
            select(models.Resume).where(models.Resume.id==id)
        )
    except NoResultFound as e:
        raise responses.NOT_FOUND(e._message())
    else:
        return instance.scalar_one()


@connection()
async def get_user_resumes(session: AsyncSession, user_id: int):
    return (
        await session.execute(
            select(models.Resume).order_by("id")\
                .where(models.Resume.user_id==user_id)
        )
    ).scalars()

@connection()
async def search_resume(session: AsyncSession, user_id: int, search_resume):
    resume = models.Resume
    title = search_resume.title
    key_word = search_resume.content

    return (
        await session.execute(
            select(resume).where(
                and_(
                    resume.user_id == user_id, 
                    resume.title.icontains(title), 
                    resume.content.icontains(key_word)
                )
            )
        )
    ).scalars()

@connection(commit=True)
async def update_resume(session: AsyncSession, id: int, resume):
    return (
        await session.execute(
            update(models.Resume).values(**resume.model_dump())\
                .where(models.Resume.id==id).returning(models.Resume)
        )
    ).scalar_one_or_none()

@connection(commit=True)
async def delete_resume(session: AsyncSession, id: int):
    try:
        return (
            await session.execute(
                delete(models.Resume).where(models.Resume.id==id).returning(models.Resume)
            )
        ).scalar_one_or_none()
    except NoResultFound as e:
        raise responses.GONE(e._message())