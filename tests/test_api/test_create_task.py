import allure
import pytest

from utils.api_client import YouGileApiClient

pytestmark = pytest.mark.api


@pytest.mark.api
@allure.title("Создание задачи")
@allure.story("Управление задачами")
@allure.description(
    "Проверка создания задачи в колонке через API YouGile."
)
def test_create_task(
    api_client: YouGileApiClient,
    created_column_id: str,
) -> None:
    """Проверяет создание задачи в существующей колонке."""

    with allure.step("Создать тестовую задачу"):
        response = api_client.create_task(
            "Задача для API-тестов",
            created_column_id,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 201, (
            f"Задача не создана: {response.status_code} {response.text}"
        )

    with allure.step("Проверить ID созданной задачи"):
        task_id = response.json().get("id")

        assert task_id, "В ответе отсутствует ID созданной задачи"
