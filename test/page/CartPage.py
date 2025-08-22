from selenium.webdriver.common.by import By
from page.BasePage import BasePage
import allure


@allure.epic("Корзина покупок")
@allure.feature("Управление корзиной")
class CartPage(BasePage):
    """Page Object для страницы корзины"""

    # Локаторы элементов
    CART_ITEM_TITLE = (By.CSS_SELECTOR, "div.product-cart-title__head")
    PROMO_CODE_INPUT = (By.XPATH, '//input[@placeholder="Введите промокод"]')
    APPLY_PROMO_BUTTON = (By.CSS_SELECTOR, "span.promo-code__button-text")
    PROMO_CODE_MESSAGE = (By.CSS_SELECTOR, "div.promo-code__message")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Получение названия товара в корзине")
    def get_cart_item_title(self):
        """Получает название товара в корзине"""
        return self.get_element_text(self.CART_ITEM_TITLE)

    @allure.step("Применение промокода: '{promo_code}'")
    def apply_promo_code(self, promo_code):
        """Применяет промокод"""
        self.send_keys_to_element(self.PROMO_CODE_INPUT, promo_code)
        self.click_element(self.APPLY_PROMO_BUTTON)
        return self

    @allure.step("Получение сообщения о результате применения промокода")
    def get_promo_code_message(self):
        """Получает сообщение о результате применения промокода"""
        return self.get_element_text(self.PROMO_CODE_MESSAGE)

    @allure.step("Проверка, что сообщение содержит текст: '{expected_text}'")
    def is_promo_code_message_contains(self, expected_text):
        """Проверяет, содержит ли сообщение ожидаемый текст"""
        return expected_text.lower() in self.get_promo_code_message().lower()

    @allure.step("Получение количества товаров в корзине")
    def get_cart_items_count(self):
        """Возвращает количество товаров в корзине"""
        return len(self.driver.find_elements(*self.CART_ITEMS))

    @allure.step("Проверка, пуста ли корзина")
    def is_cart_empty(self):
        """Проверяет, пуста ли корзина"""
        return self.get_cart_items_count() == 0