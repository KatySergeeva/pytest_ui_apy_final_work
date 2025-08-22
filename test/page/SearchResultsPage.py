from selenium.webdriver.common.by import By
from page.BasePage import BasePage
from selenium.common.exceptions import TimeoutException
import allure


@allure.epic("Результаты поиска")
@allure.feature("Поиск и фильтрация")
class SearchResultsPage(BasePage):
    """Page Object для страницы результатов поиска"""

    # Локаторы элементов
    RESULTS_COUNT = (By.CSS_SELECTOR, ".catalog-products-total")
    FIRST_RESULT_TITLE = (By.CSS_SELECTOR, ".product-card__title")
    NO_RESULTS_MESSAGE = (By.XPATH, 
        '//div[@class="catalog-stub__content catalog-stub__content--row"]'
    )

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Получение количества результатов поиска")
    def get_results_count(self):
        """Возвращает количество результатов поиска"""
        return len(self.driver.find_elements(*self.RESULTS_COUNT))

    @allure.step("Проверка наличия результатов поиска")
    def has_results(self):
        """Проверяет, есть ли результаты поиска"""
        return self.get_results_count() > 0

    @allure.step("Получение заголовка первого результата")
    def get_first_result_title(self):
        """Возвращает заголовок первого результата"""
        return self.get_element_text(self.FIRST_RESULT_TITLE)

    @allure.step("Получение сообщения об отсутствии результатов")
    def get_no_results_message(self):
        """Возвращает сообщение об отсутствии результатов"""
        return self.get_element_text(self.NO_RESULTS_MESSAGE)

    @allure.step("Проверка наличия книги '{book_title}' в результатах")
    def is_book_in_results(self, book_title):
        """Проверяет, содержится ли название книги в результатах"""
        if self.has_results():
            return book_title.lower() in self.get_first_result_title().lower()
        return False

    @allure.step("Ожидание загрузки результатов поиска")
    def wait_for_results_loaded(self):
        """Ожидает загрузки результатов поиска"""
        try:
            self.wait_for_element_visible(self.RESULTS_COUNT, timeout=15)
            return True
        except TimeoutException:
            # Если результатов нет, проверяем сообщение об отсутствии
            try:
                self.wait_for_element_visible(self.NO_RESULTS_MESSAGE, timeout=5)
                return False
            except TimeoutException:
                raise Exception("Не удалось определить состояние результатов поиска")