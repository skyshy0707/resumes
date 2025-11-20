from fastapi import Request

from core import responses
from core.authorization.services import basic_auth, jwt_auth
from core.schemes import schemes, params
from core.utils import paginate_qs
from db import models
from db import dao

from core.logger import setup_logger

logger = setup_logger(__name__)

async def get_refresh_token(request: Request, user_id: int):
    jwt_token_data = await jwt_auth.get_model_params({
        "user_id": user_id,
        "info": request.headers.get("User-Agent")
    })

    jwt_token = await dao.update_jwt_token(jwt_token_data)
    if jwt_token:

        return responses.UPDATED(
            schemes.UserJWTTokenResponse\
                .model_validate(jwt_token)\
                .model_dump(by_alias=True)
        )
    
    return await dao.create_jwt_token(jwt_token_data)


async def registration(credentials: schemes.BasicAuth) -> str:
    user_data = credentials.model_dump(by_alias=True)
    
    user_data = basic_auth.get_model_params(user_data)
    logger.info(f"user_data: {user_data}, credentials: {credentials.__class__}")
    user = await dao.create_user(user_data)
    logger.info(f"User as: {user}")
    return user

async def signup(request: Request, credentials: schemes.BasicAuth) -> models.JWTToken:
  
    user_data = credentials.model_dump(by_alias=True)
    user: models.User = await dao.get_user(email=credentials.username)
    logger.info(f"User data: {user_data}")

    assert basic_auth.verify(user_data, user.password, user.salt) \
        or responses.UNAUTHORIZED("Wrong credentials")
    
    return await get_refresh_token(request, user.id)
    

async def create_resume(resume: schemes.ResumeCreateRequest):
    id_ = await dao.create_resume(resume)
    return id_

async def get_user_resumes(user_id: int, params: params.SearchResume):
    resumes = await dao.search_resume(user_id, params)
    return paginate_qs(resumes, params)

async def get_resume(id: int):
    return await dao.get_resume(id)

async def edit_resume(id: int, resume: schemes.ResumeEditRequest):
    return await dao.update_resume(id, resume)

async def delete_resume(id: int):
    return await dao.delete_resume(id)


    