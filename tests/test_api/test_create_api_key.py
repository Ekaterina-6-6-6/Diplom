import allure
import requests


@allure.title("Получение API-ключа с корректными данными")
@allure.description("Проверка успешной авторизации через API YouGile.")
def test_create_api_key(
    base_url: str,
    login: str,
    password: str,
    company_id: str,
) -> None:
    """Проверяет получение API-ключа с корректными данными."""

    with allure.step("Отправить запрос на получение API-ключа"):
        response = requests.post(
            f"{base_url}/api-v2/auth/keys",
            json={
                "login": login,
                "password": password,
                "companyId": company_id,
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 201

    with allure.step("Проверить наличие API-ключа в ответе"):
        response_data = response.json()

        assert "key" in response_data
        assert response_data["key"]
