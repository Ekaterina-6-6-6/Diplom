import allure
import requests


@allure.title("Создание проекта с корректным названием")
@allure.description("Проверка создания проекта через API YouGile.")
def test_create_project(api_token: str, base_url: str) -> None:
    """Проверяет создание проекта и получение его ID."""

    project_title = "Автотест проект"

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
        assert response.status_code == 201

    with allure.step("Проверить наличие ID созданного проекта"):
        response_data = response.json()
        assert "id" in response_data
        assert response_data["id"]
