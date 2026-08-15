import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    login: str
    password: str
    company_id: str


def _required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Environment variable {name} is not set")

    return value


settings = Settings(
    base_url=os.getenv(
        "YOUGILE_BASE_URL",
        "https://ru.yougile.com",
    ),
    login=_required_env("YOUGILE_LOGIN"),
    password=_required_env("YOUGILE_PASSWORD"),
    company_id=_required_env("YOUGILE_COMPANY_ID"),
)
