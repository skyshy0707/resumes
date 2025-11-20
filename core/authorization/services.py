from core.authorization.creds import BasicAuth, JWTAuth
from core.config import Config
from db.models import User, JWTToken

from fastapi.security import HTTPBasic

basic_auth = BasicAuth(Config.basic_auth, User, "password")
jwt_auth = JWTAuth(Config.jwt_auth, JWTToken, "token")