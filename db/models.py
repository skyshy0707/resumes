from sqlalchemy import (
    Column, 
    DateTime, 
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, validates


from core.config import Config
from core.utils import is_token_valid
from db import validators
from db.engine import Base



class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String(2048), nullable=False, unique=True)
    salt = Column(String(1024), nullable=False , unique=True)
    updated_at = Column(DateTime, nullable=False)

    resumes = relationship("Resume", back_populates="user", lazy="selectin")
    user_agents = relationship(
        "UserAgent", back_populates="user", lazy="selectin", foreign_keys=lambda: [UserAgent.user_id]
    )

    @validates('email')
    def validate_email(self, field_name, value):
        return validators(self, field_name, value)

class UserAgent(Base):

    __tablename__ = "user_agent"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    info = Column(String(256), nullable=False)

    user = relationship(
        "User", back_populates="user_agents", lazy="selectin", single_parent=True, foreign_keys=[user_id]
    )
    auth_token = relationship(
        "JWTToken", back_populates="user_agent", lazy="selectin", uselist=False, foreign_keys=lambda: [JWTToken.user_agent_id]
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'info', name='user_agent_c_key'),
    )

class JWTToken(Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grant_access = True
  

    __tablename__ = "jwt"

    token = Column(String(2048), nullable=False, primary_key=True)
    user_agent_id = Column(Integer, ForeignKey("user_agent.id"), nullable=False)
    salt = Column(String(1024), nullable=False)
    refresh_token = Column(String(2048), unique=True)
    updated_at = Column(DateTime, nullable=False)

    user_agent = relationship(
        "UserAgent", back_populates="auth_token", lazy="selectin", single_parent=True, foreign_keys=[user_agent_id] 
    )

    @property
    def grant_access(self):
        return self._grant_access
    
    @grant_access.setter
    def grant_access(self, grant_access_value):
        self._grant_access = grant_access_value

    @property
    def valid(self):
        return is_token_valid(self.updated_at, Config.jwt_auth.EXPIRES_IN)

    @property
    def user_id(self):
        return self.user_agent.user_id

class Resume(Base):

    __tablename__ = "resume"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(20), nullable=False, default="Новое Резюме")
    content = Column(String(2000), nullable=False)

    user = relationship("User", back_populates="resumes", lazy="selectin", single_parent=True)



__all__ = (
    "Base",
    "User",
    "UserAgent",
    "JWTToken",
    "Resume"
)