import allure
import pytest

from utils.api_client import YouGileApiClient

pytestmark = pytest.mark.api


@pytest.mark.api
@allure.title("Получение списка задач")
@allure.story("Управление задачами")
@allure.description(
    "Проверка получения списка задач через API YouGile."
)
def test_get_tasks(
    api_client: YouGileApiClient,
) -> None:
    """Проверяет получение списка задач."""

    with allure.step("Отправить запрос на получение списка задач"):
        response = api_client.get_tasks(
            limit=50,
            offset=0,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200, (
            "Не удалось получить список "
            + f"задач: {response.status_code} {response.text}"
        )

    with allure.step("Проверить структуру ответа"):
        data = response.json()

        assert "paging" in data, "В ответе отсутствует поле paging"
        assert "content" in data, "В ответе отсутствует поле content"

        assert isinstance
        (
            data["content"], list
        ), "Поле content должно быть массивом"
