import os
import time

import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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


@allure.title("Открытие формы создания проекта")
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


@allure.title("Создание проекта через UI")
@allure.description(
    "Проверка создания нового проекта через пользовательский интерфейс YouGile."
)
def test_create_project(driver) -> None:
    """Проверяет создание нового проекта через UI."""

    login = os.environ["YOUGILE_LOGIN"]
    password = os.environ["YOUGILE_PASSWORD"]

    wait = WebDriverWait(driver, 15)

    project_name = f"UI Test Project {int(time.time())}"

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

    with allure.step("Проверить открытие формы"):
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Новый проект с задачами']",
                )
            )
        )

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
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@role='button']"
                    "[.//div[normalize-space()='Добавить проект с задачами']]",
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            create_project_button,
        )

    with allure.step("Проверить создание проекта"):
        created_project = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//*[normalize-space()='{project_name}']",
                )
            )
        )

        assert created_project.is_displayed()


@pytest.mark.ui
@allure.title("Отмена создания проекта")
@allure.description(
    "Проверка отмены создания нового проекта через пользовательский интерфейс YouGile."
)
def test_cancel_create_project(driver) -> None:
    """Проверяет отмену создания проекта через UI."""

    login = os.environ["YOUGILE_LOGIN"]
    password = os.environ["YOUGILE_PASSWORD"]

    wait = WebDriverWait(driver, 15)

    project_name = f"UI Cancel Project {int(time.time())}"

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

    with allure.step("Проверить открытие формы"):
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Новый проект с задачами']",
                )
            )
        )

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

    with allure.step("Отменить создание проекта"):
        cancel_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Отмена']",
                )
            )
        )
        cancel_button.click()

    with allure.step("Проверить закрытие формы"):
        wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Новый проект с задачами']",
                )
            )
        )

    with allure.step("Проверить отсутствие проекта"):
        project_elements = driver.find_elements(
            By.XPATH,
            f"//*[normalize-space()='{project_name}']",
        )

        assert not project_elements, (
            f"Проект '{project_name}' не должен быть создан."
        )


@pytest.mark.ui
@allure.title("Создание CRM-проекта через UI")
@allure.description(
    "Проверка создания нового CRM-проекта через пользовательский интерфейс YouGile."
)
def test_create_crm_project(driver) -> None:
    """Проверяет создание CRM-проекта через UI."""

    login = os.environ["YOUGILE_LOGIN"]
    password = os.environ["YOUGILE_PASSWORD"]

    wait = WebDriverWait(driver, 15)

    project_name = f"UI CRM Test Project {int(time.time())}"

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

    with allure.step("Выбрать CRM-проект"):
        crm_project = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='CRM-проект']",
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            crm_project,
        )

    with allure.step("Проверить открытие формы CRM-проекта"):
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Новый CRM-проект']",
                )
            )
        )

    with allure.step("Ввести название CRM-проекта"):
        project_name_field = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@placeholder='Введите название проекта…']",
                )
            )
        )

        project_name_field.send_keys(project_name)

    with allure.step("Создать CRM-проект"):
        create_project_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@role='button'][.//div[normalize-space()='Добавить CRM-проект']]",
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            create_project_button,
        )

    with allure.step("Проверить создание CRM-проекта"):
        created_project = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//*[normalize-space()='{project_name}']",
                )
            )
        )

        assert created_project.is_displayed()


@pytest.mark.ui
@allure.title("Отмена создания CRM-проекта")
@allure.description(
    "Проверка отмены создания CRM-проекта через пользовательский интерфейс YouGile."
)
def test_cancel_create_crm_project(driver) -> None:
    """Проверяет отмену создания CRM-проекта через UI."""

    login = os.environ["YOUGILE_LOGIN"]
    password = os.environ["YOUGILE_PASSWORD"]

    wait = WebDriverWait(driver, 15)

    project_name = f"UI Cancel CRM Project {int(time.time())}"

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

    with allure.step("Выбрать CRM-проект"):
        crm_project = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='CRM-проект']",
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            crm_project,
        )

    with allure.step("Проверить открытие формы CRM-проекта"):
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Новый CRM-проект']",
                )
            )
        )

    with allure.step("Ввести название CRM-проекта"):
        project_name_field = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@placeholder='Введите название проекта…']",
                )
            )
        )
        project_name_field.send_keys(project_name)

    with allure.step("Отменить создание CRM-проекта"):
        cancel_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Отмена']",
                )
            )
        )
        cancel_button.click()

    with allure.step("Проверить закрытие формы"):
        wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Новый CRM-проект']",
                )
            )
        )

    with allure.step("Проверить отсутствие CRM-проекта"):
        project_elements = driver.find_elements(
            By.XPATH,
            f"//*[normalize-space()='{project_name}']",
        )

        assert not project_elements, (
            f"CRM-проект '{project_name}' не должен быть создан."
        )


@pytest.mark.ui
@allure.title("Открытие созданного проекта через UI")
@allure.description(
    "Проверка открытия созданного проекта через пользовательский интерфейс YouGile."
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
                    "//div[@role='button'][.//div[normalize-space()='Добавить проект с задачами']]",
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
