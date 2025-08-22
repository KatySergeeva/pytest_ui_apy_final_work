from selenium.webdriver.common.by import By
from page.BasePage import BasePage
from page.SearchResultsPage import SearchResultsPage
from page.CartPage import CartPage
import allure

@allure.epic("Главная страница")
@allure.feature("Навигация и поиск")
class MainPage(BasePage):
    """Page Object для главной страницы Читай-город"""

    # Локаторы элементов
    LOGO = (By.CSS_SELECTOR, "svg.header__logo")
    SEARCH_FORM = (By.CSS_SELECTOR, "form.search-form")
    CART_BUTTON = (By.CSS_SELECTOR, "button.header-controls__btn")
    CITY_CONFIRM_BUTTON = (By.XPATH, 
        '//button[@class="chg-app-button chg-app-button--primary chg-app-button--l '
        'chg-app-button--brand-blue chg-app-button--block"]'
    )
    SEARCH_INPUT = (By.XPATH, 
        '//input[@class="search-form__input search-form__input--search"]'
    )
    SEARCH_BUTTON = (By.XPATH, 
        '//button[@class="chg-app-button chg-app-button--primary chg-app-button--l '
        'chg-app-button--blue chg-app-button--iconic search-form__button-search '
        'search-form__button-search"]'
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.chitai-gorod.ru/")

    @allure.step("Подтверждение выбора города")
    def confirm_city(self):
        """Подтверждает выбор города"""
        self.click_element(self.CITY_CONFIRM_BUTTON)
        return self

    @allure.step("Поиск книги: '{book_title}'")
    def search_book(self, book_title):
        """Выполняет поиск книги"""
        self.send_keys_to_element(self.SEARCH_INPUT, book_title)
        self.click_element(self.SEARCH_BUTTON)
        return SearchResultsPage(self.driver)

    @allure.step("Переход в корзину")
    def go_to_cart(self):
        """Переходит в корзину"""
        self.click_element(self.CART_BUTTON)
        return CartPage(self.driver)

    @allure.step("Проверка отображения логотипа")
    def is_logo_displayed(self):
        """Проверяет, отображается ли логотип"""
        return self.is_element_displayed(self.LOGO)

    @allure.step("Проверка отображения формы поиска")
    def is_search_form_displayed(self):
        """Проверяет, отображается ли форма поиска"""
        return self.is_element_displayed(self.SEARCH_FORM)

    @allure.step("Проверка отображения кнопки корзины")
    def is_cart_button_displayed(self):
        """Проверяет, отображается ли кнопка корзины"""
        return self.is_element_displayed(self.CART_BUTTON)