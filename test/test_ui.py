import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from page.MainPage import MainPage
from page.ProductPage import ProductPage
import allure

@pytest.fixture
@allure.title("Инициализация браузера")
def browser():
    """Фикстура для инициализации и закрытия браузера"""
    with allure.step("Запуск Chrome браузера"):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.implicitly_wait(10)
        driver.maximize_window()

    yield driver

    with allure.step("Закрытие браузера"):
        driver.quit()


@allure.epic("Тестирование интернет-магазина")
@allure.feature("Главная страница")
@allure.story("Элементы интерфейса")
@allure.severity(allure.severity_level.BLOCKER)
def test_positive_main_page_elements(browser):
    """Позитивный тест: проверка основных элементов главной страницы"""
    with allure.step("Инициализация главной страницы"):
        main_page = MainPage(browser)

    with allure.step("Проверка отображения логотипа"):
        assert main_page.is_logo_displayed(), "Логотип не отображается"

    with allure.step("Проверка отображения формы поиска"):
        assert main_page.is_search_form_displayed(), "Форма поиска не отображается"

    with allure.step("Проверка отображения кнопки корзины"):
        assert main_page.is_cart_button_displayed(), "Кнопка корзины не отображается"


@allure.epic("Тестирование интернет-магазина")
@allure.feature("Поиск товаров")
@allure.story("Успешный поиск")
@allure.severity(allure.severity_level.CRITICAL)
def test_positive_book_search(browser):
    """Позитивный тест: поиск существующей книги"""
    with allure.step("Инициализация главной страницы"):
        main_page = MainPage(browser)
        main_page.confirm_city()

    with allure.step("Поиск книги 'Гарри Поттер и философский камень'"):
        search_results = main_page.search_book("Гарри Поттер и философский камень")

    with allure.step("Ожидание загрузки результатов поиска"):
        search_results.wait_for_results_loaded()

    with allure.step("Проверка наличия результатов поиска"):
        assert search_results.has_results(), "Не найдено ни одного результата поиска"

    with allure.step("Получение и анализ первого результата"):
        first_result_title = search_results.get_first_result_title()

    with allure.step("Проверка соответствия поисковому запросу"):
        assert "Гарри Поттер" in first_result_title, \
            f"В результатах поиска не найдено упоминания 'Гарри Поттер'. Первый результат: '{first_result_title}'"


@allure.epic("Тестирование интернет-магазина")
@allure.feature("Поиск товаров")
@allure.story("Неуспешный поиск")
@allure.severity(allure.severity_level.NORMAL)
def test_negative_book_search(browser):
    """Негативный тест: поиск несуществующей книги"""
    with allure.step("Инициализация главной страницы"):
        main_page = MainPage(browser)
        main_page.confirm_city()

    with allure.step("Поиск несуществующей книги с рандомным названием"):
        nonexistent_book = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890"
        search_results = main_page.search_book(nonexistent_book)

    with allure.step("Ожидание загрузки результатов поиска"):
        search_results.wait_for_results_loaded()

    with allure.step("Получение сообщения об отсутствии результатов"):
        actual_message = search_results.get_no_results_message()

    with allure.step("Проверка корректности сообщения"):
        expected_message = "Похоже, у нас такого нет"
        assert expected_message in actual_message, \
            f"Ожидалось сообщение '{expected_message}', но получено: '{actual_message}'"


@allure.epic("Тестирование интернет-магазина")
@allure.feature("Корзина покупок")
@allure.story("Добавление товара")
@allure.severity(allure.severity_level.CRITICAL)
def test_positive_add_book_to_cart(browser):
    """Позитивный тест: добавление книги в корзину"""

    product_url = "https://www.chitai-gorod.ru/product/rassvet-zatvy-3092117"

    with allure.step(f"Открытие страницы товара: {product_url}"):
        product_page = ProductPage(browser, product_url)

    with allure.step("Получение названия товара на странице товара"):
        title_pdp = product_page.get_product_title()

    with allure.step("Добавление товара в корзину"):
        product_page.add_to_cart()

    with allure.step("Переход в корзину"):
        cart_page = product_page.go_to_cart()

    with allure.step("Получение названия товара в корзине"):
        title_cart = cart_page.get_cart_item_title()

    with allure.step("Сравнение названий товара"):
        assert title_pdp == title_cart, \
            f"Название товара на странице '{title_pdp}' не совпадает с названием в корзине '{title_cart}'"


@allure.epic("Тестирование интернет-магазина")
@allure.feature("Корзина покупок")
@allure.story("Промокоды")
@allure.severity(allure.severity_level.NORMAL)
def test_negative_change_quantity_in_cart(browser):
    """Негативный тест: попытка применить несуществующий промокод"""

    product_url = "https://www.chitai-gorod.ru/product/rassvet-zatvy-3092117"

    with allure.step(f"Открытие страницы товара: {product_url}"):
        product_page = ProductPage(browser, product_url)

    with allure.step("Добавление товара в корзину"):
        product_page.add_to_cart()

    with allure.step("Переход в корзину"):
        cart_page = product_page.go_to_cart()

    with allure.step("Применение невалидного промокода"):
        cart_page.apply_promo_code("!@#$%^&*()")
    
    with allure.step("Получение результата применения промокода"):
        result = cart_page.get_promo_code_message()

    with allure.step("Проверка сообщения об ошибке"):
        expected_result = "Промокода не существует"
        assert result == expected_result, \
            f"Ожидалось сообщение '{expected_result}', но получено: '{result}'"