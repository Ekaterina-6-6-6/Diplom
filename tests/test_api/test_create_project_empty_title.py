import allure
import requests


@allure.title("Создание проекта проект с пустым названием")
@allure.description("Проверка создания проекта через API YouGile.")
def test_create_project_empty_title(api_token: str, base_url: str) -> None:
    """Проверяет создание проекта с пустым названием."""

    project_title = ""

    with allure.step("Отправить запрос на создание проекта"):
        response = requests.post(
            f"{base_url}/api-v2/projects",
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            },
            json={
                "title": project_title,
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 400, (
            "Ожидался статус 400 для проекта с пустым названием: "
            f"{response.status_code} {response.text}"
        )
