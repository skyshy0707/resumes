from typing import Annotated, Any, Tuple

from fastapi import Depends, Request

from core import responses
from core.authorization.services import jwt_auth
from db import dao, models

from core.logger import setup_logger

logger = setup_logger(__name__)

async def authorize(request: Request) -> int:
    user_id = request.cookies.get('user_id')

    logger.info(f"user_id: {user_id}, cookies: {request.cookies}")

    assert user_id or responses.UNAUTHORIZED("Token was not provided")

    user_id = int(user_id)

    user_auth_token = request.headers.get('Authorization', '').removeprefix('Bearer ')

    token: models.JWTToken = await dao.get_jwt_token(user_auth_token)
    
    assert token or responses.UNAUTHORIZED("Token was not provided")

    if token.grant_access:
        assert token.valid or responses.UNAUTHORIZED("Token is expired")

    token_salt = getattr(token, "salt")
    user_agent = jwt_auth.decode_to_data(user_auth_token, token_salt) 

    logger.info(f"user_id: {user_id}, user_agent: {user_agent}")
    assert user_agent.get("user_id") == user_id or responses.UNAUTHORIZED("Wrong token")

    return user_id

class is_eligible_user():

    def __init__(self, resource_model: dao.DeclarativeMeta, resource_pk_name="id", owner_fk_name="user_id", type_mapper: Any=None):
        self.resource_model = resource_model
        self.resource_pk_name = resource_pk_name
        self.owner_fk_name = owner_fk_name
        self.type_mapper = type_mapper

    async def __call__(self, request: Request):
        user_id = await authorize(request)
        resource_pk_value = request.path_params.get(
            self.resource_pk_name, request.query_params.get(self.resource_pk_name)
        )

        if self.type_mapper:
            try:
                resource_pk_value = self.type_mapper(resource_pk_value)
            except ValueError:
                pass



        resource = await dao.get_resource(
            self.resource_model, **{ self.resource_pk_name: resource_pk_value }
        )

        assert getattr(resource, self.owner_fk_name) == user_id, \
            responses.FORBIDDEN("You don't have enought rights")
        return True



access_resume = is_eligible_user(models.Resume, type_mapper=int)

grant_access_resume = Annotated[bool, Depends(access_resume)]


