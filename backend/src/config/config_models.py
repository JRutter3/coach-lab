from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class SQLiteConfig(BaseSettings):
    db_type: Literal["sqlite"]
    db_url: str

    @property
    def cnn_str(self) -> str:
        return "sqlite+aiosqlite:///{self.db_url}"

class APIConfig(BaseSettings):
    db_settings: SQLiteConfig = Field(discriminator="db_type")
