
import time

import allure
from pages.MainPage import MainPage


@allure.story("Создание проекта")
@allure.title("Создание проекта с валидным названием")
@allure.description(
    "Тест проверяет успешное создание нового проекта с корректным названием"
)
def test_create(driver):
    main = MainPage(driver)
    main.open()
    time.sleep(3)
