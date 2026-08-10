import allure
import requests


from config.settings import settings


@allure.title("Получение API-ключа с неверным паролем")
@allure.description(
    "Проверка отказа в авторизации при использовании неверного пароля."
)
def test_create_api_key_invalid_password() -> None:
    """Проверяет получение API-ключа с неверным паролем."""

    with allure.step("Отправить запрос с неверным паролем"):
        response = requests.post(
            f"{settings.base_url}/api-v2/auth/keys",
            json={
                "login": settings.login,
                "password": "WrongPassword123!",
                "companyId": settings.company_id,
            },
            headers={
                "Content-Type": "application/json",
            },
            timeout=15,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 401, (
            "Ожидался статус 401 Unauthorized, "
            f"получен {response.status_code}: {response.text}"
        )

    with allure.step("Проверить отсутствие API-ключа"):
        assert "key" not in response.json()
