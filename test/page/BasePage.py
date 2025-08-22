from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure

@allure.epic("Базовые операции")  
@allure.feature("Взаимодействие с элементами")
class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Проверка отображения элемента: {locator}")
    def is_element_displayed(self, locator):
        """Проверяет, отображается ли элемент"""
        try:
            return self.driver.find_element(*locator).is_displayed()
        except NoSuchElementException:
            return False
    
    @allure.step("Клик по элементу: {locator}")
    def click_element(self, locator):
        """Кликает на элемент с ожиданием кликабельности"""
        self.wait.until(EC.element_to_be_clickable(locator)).click()
    
    @allure.step("Ввод текста '{text}' в элемент: {locator}")
    def send_keys_to_element(self, locator, text):
        """Вводит текст в элемент с очисткой поля"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator):
        """Получает текст элемента"""
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    @allure.step("Ожидание видимости элемента: {locator} (таймаут: {timeout}с)")
    def wait_for_element_visible(self, locator, timeout=10):
        """Ожидает появления элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url