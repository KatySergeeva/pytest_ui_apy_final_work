# Автоматизированное тестирование интернет-магазина "Читай-город"

## Задача проекта

Разработка автоматизированного тестирования для интернет-магазина "Читай-город", включающего UI-тестирование веб-интерфейса и API-тестирование с интеграцией Allure Framework для создания детальных отчетов.

### Шаги
 
1. Клонирование проекта
git clone https://github.com/KatySergeeva/pytest_ui_api_final_work.git
cd pytest_ui_api_final_work
2. Установка зависимостей 
pip install pytest selenium webdriver-manager requests allure-pytest pytest-allure
3. Запуск тестов

# Запуск всех тестов
pytest

# Запуск только UI-тестов
pytest test/test_ui.py -v

# Запуск только API-тестов
pytest test/test_api.py -v

# Запуск с генерацией Allure отчетов
pytest --alluredir allure-result

4. Генерация и просмотр отчетов Allure
Чтобы открыть отчёт Allure, выполните следующую команду: allure serve allure-result . Отчёт откроется в вашем браузере автоматически

### Тестовое покрытие
UI-тесты
- Проверка основных элементов главной страницы

- Поиск существующих книг

- Поиск несуществующих книг

- Добавление товаров в корзину

- Работа с промокодами

API-тесты
- Добавление товаров в корзину

- Очистка корзины

- Смена города пользователя

- Негативные сценарии (ошибки авторизации, невалидные данные, неверные методы)

### Стек:
- pytest
- selenium
- requests
- _sqlalchemy_
- allure

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- [Документация Pytest](https://docs.pytest.org/en/stable/)
- [Документация Selenium](https://www.selenium.dev/documentation/)
- [Документация Allure](https://allurereport.org/docs/)
