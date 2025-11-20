import copy
import hmac
import os
from typing import  Any, Dict, Union

import jwt

from core.schemes.schemes import AuthSettings, create_auth_method_model
from core.utils import generate_salt, now
from db.__init__ import DeclarativeMeta
from db.dao import get_or_create_user_agent

from core.logger import setup_logger

logger = setup_logger(__name__)

class Auth:

    def __init__(
            self, settings: AuthSettings, 
            auth_model: DeclarativeMeta, 
            crypted_param: str
        ):
        self.settings = settings
        self.auth_model = auth_model
        self.crypted_param = crypted_param

    @property
    def settings(self) -> AuthSettings:
        return self._settings
    
    @settings.setter
    def settings(self, auth_settings: AuthSettings) -> None:
        self._settings = auth_settings


    def salt_mix(self, decode_func: callable, token: str, salt: str='0') -> bytes:
        return hex(int(self.settings.SECRET_KEY, 16) ^ int(salt, 16)).removeprefix('0x').encode()
    
    def generate_refresh_token(self, data: Union[dict, str], salt: str='0') -> str:
        return self.encode_to_token(
            data,
            salt
        )
    
    def get_main_keys(self, data: Union[dict, str]) -> Dict[str, str]:
        return {
            "salt": generate_salt(),
            "updated_at": now()
        }
    
    def get_model_params(self, specific_params: Dict[str, Any]) -> Dict[str, Any]:
        keys = self.get_main_keys(specific_params)
        keys.update(specific_params)
        return keys


    def encode_to_token(self, data: Union[dict, str], salt: str='0') -> str:
        return salt


class BasicAuth(Auth):
    
    def encode_to_token(self, data: str, salt: str='0') -> bytes:
        return hmac.HMAC(
            self.salt_mix(self.settings.SECRET_KEY, salt), 
            str(data).encode('utf-8'), 
            self.settings.ALGORITHM
        ).hexdigest().encode()
        
    def verify(self, data: str, encypted: str, salt: str='0') -> bool:
        logger.info(f"data: {data}, saved salt: {salt}")

        encrypted_data = self.encode_to_token(data, salt)
        logger.info(f"encr data: {encrypted_data}, password fr db: {encypted}")
        
        return hmac.compare_digest(encrypted_data, encypted.encode())
    

    def get_model_params(self, specific_params: Union[dict, str]):
        model_params = super().get_model_params(specific_params)
        salt = model_params.get("salt")
        logger.info(f"specific params: {specific_params}, inputed salt: {salt}")

        model_params.update({
            "password": self.encode_to_token(
                specific_params, salt
            ).decode()
        })

        return model_params
    

class JWTAuth(Auth):
    
    def decode_to_data(self, token: str, salt: str='0') -> Dict:
        return jwt.decode(
            token, 
            self.salt_mix(self.settings.SECRET_KEY, salt), 
            algorithms=[self.settings.ALGORITHM]
        )
    
    def encode_to_token(self, data: Dict, salt: str='0') -> str:
        return jwt.encode(
            data, 
            self.salt_mix(self.settings.SECRET_KEY, salt), 
            algorithm=self.settings.ALGORITHM
        )
    
    async def get_model_params(self, specific_params: Union[dict, str]):

        model_params = super().get_model_params(specific_params)
        user_agent_id = await get_or_create_user_agent(specific_params)

        for param in specific_params.keys():
            del model_params[param]

        if isinstance(specific_params, dict):
            refresh_token = copy.deepcopy(specific_params)
            refresh_token.update({ "refresh": True })
        else:
            refresh_token = specific_params.join("refresh")

        salt = model_params.get("salt")
        model_params.update({ 
            "token": self.encode_to_token(specific_params, salt),
            "refresh_token": self.generate_refresh_token(refresh_token, salt),
            "user_agent_id": user_agent_id
        })

        return model_params

    

