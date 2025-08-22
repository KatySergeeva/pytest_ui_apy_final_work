from selenium.webdriver.common.by import By
from page.BasePage import BasePage
from page.CartPage import CartPage
import allure


@allure.epic("Страница товара")
@allure.feature("Детали товара и покупка")
class ProductPage(BasePage):
    """Page Object для страницы товара"""

    # Локаторы элементов
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product-detail-page__title")
    BUY_BUTTON = (By.CSS_SELECTOR, 
        "button.chg-app-button.product-buttons__main-action"
    )
    CART_ICON = (By.XPATH, '//button[@aria-label="Корзина"]')

    def __init__(self, driver, product_url=None):
        super().__init__(driver)
        if product_url:
            self.driver.get(product_url)
        self.driver.maximize_window()

    @allure.step("Получение названия товара")
    def get_product_title(self):
        """Получает название товара"""
        full_title = self.get_element_text(self.PRODUCT_TITLE)
        return full_title.split("\n")[0].strip()

    @allure.step("Добавление товара в корзину")
    def add_to_cart(self):
        """Добавляет товар в корзину"""
        self.click_element(self.BUY_BUTTON)
        return self

    @allure.step("Переход в корзину")
    def go_to_cart(self):
        """Переходит в корзину"""
        self.click_element(self.CART_ICON)
        return CartPage(self.driver)

    @allure.step("Проверка отображения кнопки 'Купить'")
    def is_buy_button_displayed(self):
        """Проверяет, отображается ли кнопка покупки"""
        return self.is_element_displayed(self.BUY_BUTTON)