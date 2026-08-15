import os

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = pytest.mark.ui


@pytest.mark.ui
@allure.title("Открытие формы создания проекта")
@allure.story("Управление проектами")
@allure.description(
    "Проверка открытия формы создания нового проекта в YouGile."
)
def test_open_create_project_form(driver) -> None:
    """Проверяет открытие формы создания проекта."""

    login = os.environ["YOUGILE_LOGIN"]
    password = os.environ["YOUGILE_PASSWORD"]

    wait = WebDriverWait(driver, 15)

    with allure.step("Открыть главную страницу YouGile"):
        driver.get("https://ru.yougile.com/")

    with allure.step("Открыть форму авторизации"):
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='Войти']")
            )
        )
        login_button.click()

    with allure.step("Заполнить E-mail"):
        email_field = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[type='email']")
            )
        )
        email_field.send_keys(login)

    with allure.step("Заполнить пароль"):
        password_field = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[type='password']")
            )
        )
        password_field.send_keys(password)

    with allure.step("Выполнить авторизацию"):
        submit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='Войти']")
            )
        )
        submit_button.click()

    with allure.step("Дождаться рабочего пространства"):
        wait.until(EC.url_contains("/team/"))

    with allure.step("Открыть раздел проектов"):
        projects_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[normalize-space()='Проекты']")
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            projects_button,
        )

    with allure.step("Открыть создание проекта"):
        add_project_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Добавить проект с задачами']",
                )
            )
        )

        add_project_button.click()

    with allure.step("Проверить открытие формы создания проекта"):
        project_form_title = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Новый проект с задачами']",
                )
            )
        )

        assert project_form_title.is_displayed()

    with allure.step("Проверить поле названия проекта"):
        project_name_field = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@placeholder='Введите название проекта…']",
                )
            )
        )

        assert project_name_field.is_displayed()

    with allure.step("Проверить тип проекта"):
        project_type = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Проект с задачами']",
                )
            )
        )

        assert project_type.is_displayed()

    with allure.step("Проверить кнопку создания проекта"):
        create_project_button = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Добавить проект с задачами']",
                )
            )
        )

        assert create_project_button.is_displayed()

    with allure.step("Проверить кнопку отмены"):
        cancel_button = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Отмена']",
                )
            )
        )

        assert cancel_button.is_displayed()
