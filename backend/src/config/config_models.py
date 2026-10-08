from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class SQLiteConfig(BaseSettings):
    db_type: Literal["sqlite"]
    db_url: str

    @property
    def cnn_str(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_url}"

    @property
    def sync_cnn_str(self) -> str:
        return f"sqlite:///{self.db_url}"

class JWTSettings(BaseSettings):
    secret_key: str
    jwt_algorithm: str = "HS256"
    token_expire_hours: int = 24

class APIConfig(BaseSettings):
    db_settings: SQLiteConfig = Field(discriminator="db_type")
    jwt_settings: JWTSettings
