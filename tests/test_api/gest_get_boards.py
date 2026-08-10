import allure


from utils.api_client import YouGileApiClient


@allure.title("Получение списка досок проекта")
@allure.description(
    "Проверка получения списка досок через API YouGile."
)
def test_get_boards(
    api_client: YouGileApiClient,
    created_project_id: str,
) -> None:
    """Проверяет получение списка досок проекта."""

    with allure.step("Получить список досок проекта"):
        response = api_client.get_boards(
            created_project_id,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200, (
            "Не удалось получить список досок: "
            f"{response.status_code} {response.text}"
        )

    with allure.step("Проверить структуру ответа"):
        data = response.json()

        assert "paging" in data, (
            "В ответе отсутствует поле paging"
        )
        assert "content" in data, (
            "В ответе отсутствует поле content"
        )

        assert isinstance(data["content"], list), (
            "Поле content должно быть массивом"
        )

    with allure.step("Проверить принадлежность досок проекту"):
        for board in data["content"]:
            assert board["projectId"] == created_project_id
