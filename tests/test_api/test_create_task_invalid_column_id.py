import allure
import pytest

from utils.api_client import YouGileApiClient

pytestmark = pytest.mark.api


@pytest.mark.api
@allure.title("Создание задачи с несуществующей колонкой")
@allure.story("Управление задачами")
@allure.description(
    "Проверка отказа при создании задачи с несуществующим ID колонки "
    + "через API YouGile."
)
def test_create_task_invalid_column_id(
    api_client: YouGileApiClient,
) -> None:
    """Проверяет отказ при создании задачи в несуществующей колонке."""

    invalid_column_id = "00000000-0000-0000-0000-000000000000"

    with allure.step("Создать задачу с несуществующим ID колонки"):
        response = api_client.create_task(
            "Задача для API-тестов",
            invalid_column_id,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 404, (
            "API не вернул ожидаемый статус 404: "
            f"{response.status_code} {response.text}"
        )
