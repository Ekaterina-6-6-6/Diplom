# import os
# import time
# 
# import allure
# import pytest
# 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# 
# pytestmark = pytest.mark.ui
# 
# 
# def test_open_yougile(driver) -> None:
#     """Проверяет открытие страницы YouGile."""
# 
#     driver.get("https://ru.yougile.com")
# 
#     assert driver.title == (
#         "Современная система управления проектами и задачами. "
#         "Бесплатная онлайн-версия"
#     )
# 
# Временный для новых тестов
