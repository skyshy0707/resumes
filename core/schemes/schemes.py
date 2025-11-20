import datetime
from typing import Annotated, Any, ForwardRef, List, Union

from fastapi import Cookie, Query
from fastapi.security import HTTPBasicCredentials
from pydantic import (
    AliasChoices, AliasGenerator, AliasPath, 
    BaseModel, ConfigDict, EmailStr, Field, ValidationInfo, 
    WrapSerializer, computed_field, field_serializer, field_validator, model_serializer
)
from pydantic.fields import FieldInfo
from pydantic.main import create_model
from sqlalchemy.orm import DeclarativeMeta

from core.config import Config
from core.schemes.params import Pagination
from db.dao import get_fields, get_user_agent_by_id


from core.logger import setup_logger

logger = setup_logger(__name__)


def create_pagination_response_model(model) -> BaseModel:
    items_type = List[model]
    total_type = Annotated[int, Field(0, ge=0)]
    return create_model(
        "Items",
        __base__=Pagination,
        **{
            "items": (
                items_type,
                FieldInfo(
                    annotation=items_type
                )
            ),
            "total": (
                total_type,
                FieldInfo(
                    annotation=total_type,
                )
            )
        }
    )


def create_auth_method_model(crypted_param: str, model: DeclarativeMeta) -> BaseModel:

    field_definition = lambda field_name, serialize_name=None: \
        (str, FieldInfo(alias=serialize_name, annotation=str))
    
    aliased_fields = {
        "salt": None, "refresh_token": None, "code": crypted_param, "updated_at": None
    }

    fields = get_fields(model)
    logger.info(f"builded fields: {fields}")
    return create_model(
        "AuthMethodData",
        **{ 
            name: field_definition(name, alias_name) \
                for name, alias_name in aliased_fields.items() \
                if any(variant in get_fields(model) for variant in [name, alias_name])
        }
    )


class Optional(BaseModel):

    
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)

        for field in cls.model_fields.values():
            field.default = None

        cls.model_rebuild(force=True)


class OrderFields:

    @model_serializer(when_used='json')
    def order_fields(self) -> dict:
        data = { "id": self.id }
        data.update(dict(self))
        return data
    

class AuthSettings(BaseModel):
    ALGORITHM: str
    SECRET_KEY: str
    EXPIRES_IN: Union[int, None] = None


class BasicAuth(HTTPBasicCredentials):

    username: str = Field(serialization_alias="email")

class UserCreateModel(BaseModel):

    password: str
    email: str
    salt: str
    created_at: datetime.datetime


class OrdinaryIdResponse(BaseModel):

    id: int


'''
class UserAgent(BaseModel):
    info: str
    user_id: int

'''

class UserJWTTokenResponse(BaseModel):

    token: str = Field(serialization_alias="access_token")
    refresh_token: str
    updated_at: datetime.datetime
    user_id: int
    #user_agent_id: int = Field(exclude=True)

    
    @field_serializer("updated_at")
    def serialize_updated_at(self, value: datetime.datetime):
        return value.isoformat()
    
    model_config = ConfigDict(from_attributes=True)
    
    '''
    @computed_field
    @property
    async def user_id(self) -> int:
        return (await get_user_agent_by_id(self.user_agent_id)).user_id
    '''
    
class ResumeData(BaseModel):

    title: str = "Новое резюме"
    content: str = Field()

class ResumeEditRequest(ResumeData, Optional):
    pass

class ResumeCreateRequest(ResumeData):

    user_id: int

class ResumeViewResponse(ResumeCreateRequest, OrderFields):

    id: int