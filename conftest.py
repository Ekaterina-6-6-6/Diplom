import os

import allure
import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import settings
from utils.api_client import YouGileApiClient

load_dotenv()


@pytest.fixture(scope="session")
def api_key() -> str:
    """Возвращает сохранённый API-ключ YouGile."""
    token = os.getenv("YOUGILE_API_TOKEN")

    assert token, (
        "Переменная окружения YOUGILE_API_TOKEN не задана. "
        "Добавьте действующий API-ключ в файл .env."
    )

    return token


@pytest.fixture
def api_client(
    api_key: str,
) -> YouGileApiClient:
    return YouGileApiClient(
        settings.base_url,
        api_key,
    )


@pytest.fixture(scope="session")
def base_url() -> str:
    """Возвращает базовый URL YouGile."""
    return os.getenv("YOUGILE_BASE_URL", "https://ru.yougile.com")


@pytest.fixture(scope="session")
def login() -> str:
    """Возвращает логин тестового пользователя."""
    return os.environ["YOUGILE_LOGIN"]


@pytest.fixture(scope="session")
def password() -> str:
    """Возвращает пароль тестового пользователя."""
    return os.environ["YOUGILE_PASSWORD"]


@pytest.fixture(scope="session")
def company_id() -> str:
    """Возвращает идентификатор компании."""
    return os.environ["YOUGILE_COMPANY_ID"]


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    """Создаёт HTTP-сессию для API-тестов."""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
    })
    return session


@pytest.fixture(scope="session")
def api_token() -> str:
    """Возвращает сохранённый API-ключ YouGile."""
    token = os.getenv("YOUGILE_API_TOKEN")

    assert token, (
        "Переменная окружения YOUGILE_API_TOKEN не задана. "
        "Добавьте действующий API-ключ в файл .env."
    )

    return token


@pytest.fixture(scope="session")
def auth_headers(api_token: str) -> dict[str, str]:
    """Возвращает заголовки с авторизацией."""
    return {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }


@pytest.fixture
def created_project_id(
    api_client: YouGileApiClient,
) -> str:
    """Создаёт тестовый проект и возвращает его ID."""

    with allure.step("Создать тестовый проект"):
        response = api_client.create_project(
            "Проект для API-тестов"
        )

    assert response.status_code == 201, (
        "Не удалось создать тестовый проект: "
        f"{response.status_code} {response.text}"
    )

    project_id = response.json().get("id")

    assert project_id, "В ответе отсутствует ID проекта"

    return project_id


@pytest.fixture
def created_column_id(
    api_client: YouGileApiClient,
    created_project_id: str,
) -> str:
    """Создаёт доску и колонку и возвращает ID колонки."""

    with allure.step("Создать тестовую доску"):
        board_response = api_client.create_board(
            "Доска для API-тестов",
            created_project_id,
        )

    assert board_response.status_code == 201, (
        "Не удалось создать тестовую доску: "
        f"{board_response.status_code} "
        f"{board_response.text}"
    )

    board_id = board_response.json().get("id")

    assert board_id, "В ответе отсутствует ID доски"

    with allure.step("Создать тестовую колонку"):
        column_response = api_client.create_column(
            "To do",
            board_id,
        )

    assert column_response.status_code == 201, (
        "Не удалось создать тестовую колонку: "
        f"{column_response.status_code} "
        f"{column_response.text}"
    )

    column_id = column_response.json().get("id")

    assert column_id, "В ответе отсутствует ID колонки"

    return column_id


@pytest.fixture
def driver():
    """Создаёт браузер Chrome для UI-тестов."""

    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())

    browser = webdriver.Chrome(
        service=service,
        options=options,
    )

    yield browser

    browser.quit()
