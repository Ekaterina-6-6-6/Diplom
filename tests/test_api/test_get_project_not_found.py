import allure


from utils.api_client import YouGileApiClient


@allure.title("Получение проекта с несуществующим ID")
@allure.description(
    "Проверка корректной обработки запроса проекта с несуществующим ID."
)
def test_get_project_not_found(
    api_client: YouGileApiClient,
) -> None:
    """Проверяет получение проекта с несуществующим ID."""

    fake_project_id = "00000000-0000-0000-0000-000000000000"

    with allure.step("Запросить проект с несуществующим ID"):
        response = api_client.get_project(fake_project_id)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 404, (
            "Ожидался статус 404 для несуществующего проекта: "
            f"{response.status_code} {response.text}"
        )
