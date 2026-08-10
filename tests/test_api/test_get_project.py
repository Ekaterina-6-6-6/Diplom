import allure

from utils.api_client import YouGileApiClient


@allure.title("Получение проекта по ID")
@allure.description(
    "Проверка получения ранее созданного проекта через API YouGile."
)
def test_get_project(
    api_client: YouGileApiClient,
    created_project_id: str,
) -> None:
    """Проверяет получение проекта по его ID."""

    with allure.step("Получить проект по ID"):
        response = api_client.get_project(
            created_project_id
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200

    with allure.step("Проверить данные проекта"):
        project = response.json()

        assert project["id"] == created_project_id
        assert "title" in project
        assert project["title"] == "Проект для API-тестов"
        assert "timestamp" in project
