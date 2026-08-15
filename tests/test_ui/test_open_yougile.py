import allure
import pytest

pytestmark = pytest.mark.ui


@pytest.mark.ui
@allure.title("Открытие страницы YouGile через UI")
@allure.story("Авторизация")
@allure.description(
    "Проверка открытия страницы в YouGile."
)
def test_open_yougile(driver) -> None:
    """Проверяет открытие страницы YouGile."""

    driver.get("https://ru.yougile.com")

    assert driver.title == (
        "Современная система управления проектами и задачами. "
        + "Бесплатная онлайн-версия"
    )
