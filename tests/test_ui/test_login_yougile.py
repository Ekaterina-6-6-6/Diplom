import os

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


pytestmark = pytest.mark.ui


def test_open_yougile(driver) -> None:
    """Проверяет открытие страницы YouGile."""

    driver.get("https://ru.yougile.com")

    assert driver.title == (
        "Современная система управления проектами и задачами. "
        "Бесплатная онлайн-версия"
    )


@allure.title("Успешная авторизация в YouGile")
@allure.description(
    "Проверка входа пользователя в YouGile с корректными учётными данными."
)
def test_login_yougile(driver) -> None:
    """Проверяет успешную авторизацию в YouGile."""

    login = os.environ["YOUGILE_LOGIN"]
    password = os.environ["YOUGILE_PASSWORD"]

    wait = WebDriverWait(driver, 10)

    with allure.step("Открыть главную страницу YouGile"):
        driver.get("https://ru.yougile.com/")

    with allure.step("Открыть форму авторизации"):
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='Войти']")
            )
        )
        login_button.click()

    with allure.step("Заполнить поле E-mail"):
        email_field = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[type='email']")
            )
        )
        email_field.send_keys(login)

    with allure.step("Заполнить поле пароля"):
        password_field = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[type='password']")
            )
        )
        password_field.send_keys(password)

    with allure.step("Нажать кнопку входа"):
        submit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='Войти']")
            )
        )
        submit_button.click()

    with allure.step("Проверить успешную авторизацию"):
        wait.until(EC.url_contains("/team/"))
        assert "/team/" in driver.current_url
