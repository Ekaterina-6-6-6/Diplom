import os
import time

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = pytest.mark.ui


@pytest.mark.ui
@allure.title("Открытие созданного проекта через UI")
@allure.story("Управление проектами")
@allure.description(
    "Проверка открытия созданного проекта "
    + "через пользовательский интерфейс YouGile."
)
def test_open_created_project(driver) -> None:
    """Проверяет открытие созданного проекта через UI."""

    login = os.environ["YOUGILE_LOGIN"]
    password = os.environ["YOUGILE_PASSWORD"]

    wait = WebDriverWait(driver, 15)

    project_name = f"UI Open Test Project {int(time.time())}"

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

    with allure.step("Открыть форму создания проекта"):
        add_project_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Добавить проект с задачами']",
                )
            )
        )
        add_project_button.click()

    with allure.step("Ввести название проекта"):
        project_name_field = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@placeholder='Введите название проекта…']",
                )
            )
        )
        project_name_field.send_keys(project_name)

    with allure.step("Создать проект"):
        create_project_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@role='button'][.//div[normalize-space()="
                    + "'Добавить проект с задачами']]",
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            create_project_button,
        )

    with allure.step("Найти созданный проект"):
        created_project = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//*[normalize-space()='{project_name}']",
                )
            )
        )

    with allure.step("Открыть созданный проект"):
        driver.execute_script(
            "arguments[0].click();",
            created_project,
        )

    with allure.step("Проверить открытие проекта"):
        wait.until(
            lambda driver: project_name in driver.find_element(
                By.TAG_NAME,
                "body",
            ).text
        )

        assert project_name in driver.find_element(
            By.TAG_NAME,
            "body",
        ).text
