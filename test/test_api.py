import requests
import allure


Base_URL = "https://web-agr.chitai-gorod.ru/web/api/v1/"
Token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTYwNTIyMzYsImlhdCI6MTc1NTg4NDIzNiwiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6IjdlYWYxNWY2MzYxOTQ1OGQ5OGQyODc2OTZjOTIxMzdjMDEwMWY1NWYwMjlmZjQ5N2M3Zjg1NmQ4M2VhM2I3NDciLCJ0eXBlIjoxMH0.251CVT_Li0GuLAoM-twqBomMfI3CMvd9KbLg_2t-PWk"

# Заголовки для запросов
headers = {
    "Authorization": Token,
    "Content-type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json"
}

@allure.step("Добавление товара {product_id} в корзину")
def add_product_to_cart(product_id=3092117):
    """Функция добавления товара в корзину (возвращает response)"""
    payload = {
        "id": product_id
    }
    with allure.step(f"Отправка POST запроса на {Base_URL}cart/product"):
        response = requests.post(Base_URL + 'cart/product', headers=headers, json=payload)

    with allure.step("Проверка статус кода"):
        assert response.status_code in [200, 201], f"Ожидался статус код 200 или 201, получен {response.status_code}"

    with allure.step("Проверка пустого ответа"):
        assert not response.text.strip(), f"Ожидался пустой ответ, но получено: {response.text}"
    return response


@allure.epic("API Тестирование")
@allure.feature("Корзина покупок")
@allure.story("Добавление товаров")
@allure.severity(allure.severity_level.CRITICAL)
def test_positive_add_to_cart():
    """Тест добавления товара в корзину"""
    with allure.step("Добавление товара с ID 3092117 в корзину"):
        response = add_product_to_cart(3092117)

    with allure.step("Валидация успешного ответа"):
        assert response.status_code in [200, 201]


@allure.epic("API Тестирование")
@allure.feature("Корзина покупок")
@allure.story("Очистка корзины")
@allure.severity(allure.severity_level.CRITICAL)
def test_positive_clear_cart():
    """Тест очистки всей корзины"""
    with allure.step("Добавление 3 товаров в корзину"):
        add_product_to_cart(3092117)
        add_product_to_cart(2817785)
        add_product_to_cart(2827508)

    with allure.step("Проверка корзины перед очисткой"):
        cart_response_before = requests.get(Base_URL + 'cart', headers=headers)
        cart_data_before = cart_response_before.json()
        print(f"Корзина до очистки: {len(cart_data_before.get('items', []))} товаров")
    
    with allure.step("Очистка корзины"):
        clear_response = requests.delete(Base_URL + 'cart', headers=headers)
        assert clear_response.status_code in [200, 201, 204], f"Ожидался статус 200/201/204, получен {clear_response.status_code}"
    
    with allure.step("Проверка корзины после очистки"):
        cart_response_after = requests.get(Base_URL + 'cart', headers=headers)
        cart_data_after = cart_response_after.json() 
        items_after = cart_data_after.get('items', [])
        assert len(items_after) == 0, f"Ожидалась пустая корзина, но найдено {len(items_after)} товаров"


@allure.epic("API Тестирование")
@allure.feature("Профиль пользователя")
@allure.story("Смена города")
@allure.severity(allure.severity_level.NORMAL)
def test_positive_change_city_user():
    """Тест смены города пользователя"""

    payload = {
        "cityId": 51
    }

    with allure.step(f"Отправка запроса на смену города на ID {payload['cityId']}"):
        response = requests.post(Base_URL + 'profile/change-city', headers=headers, json=payload)
    
    with allure.step("Проверка статус кода"):
        assert response.status_code in [200, 201], f"Ожидался статус код 200 или 201, получен {response.status_code}"

    with allure.step("Проверка пустого ответа"):
        assert not response.text.strip(), f"Ожидался пустой ответ, но получено: {response.text}"


@allure.epic("API Тестирование")
@allure.feature("Корзина покупок")
@allure.story("Негативные сценарии")
@allure.severity(allure.severity_level.NORMAL)
def test_negative_add_to_cart_without_token():
    """
    Негативный тест: добавление товара в корзину без токена авторизации
    Ожидаемый результат: ошибка 401 Unauthorized
    """
    payload = {
        "id": 3092117
    }
    
    with allure.step("Подготовка заголовков без токена авторизации"):
        headers_without_token = headers.copy()
        headers_without_token.pop("Authorization", None)
    
    with allure.step("Отправка запроса без токена авторизации"):
        response = requests.post(Base_URL + 'cart/product', headers=headers_without_token, json=payload)
    
    with allure.step("Проверка ошибки 401 Unauthorized"):
        assert response.status_code == 401, f"Ожидался статус код 401, получен {response.status_code}"


@allure.epic("API Тестирование")
@allure.feature("Корзина покупок")
@allure.story("Негативные сценарии")
@allure.severity(allure.severity_level.NORMAL)
def test_negative_add_to_cart_wrong_method():
    """
    Негативный тест: добавление товара в корзину с неверным HTTP-методом
    Ожидаемый результат: ошибка 405 Method Not Allowed
    """
    payload = {
        "id": 3092117
    }

    with allure.step("Отправка GET запроса вместо POST"):
        response = requests.get(Base_URL + 'cart/product', headers=headers, json=payload)

    with allure.step("Проверка ошибки 405 Method Not Allowed"):
        assert response.status_code == 405, f"Ожидался статус код 405, получен {response.status_code}"

    with allure.step("Анализ ответа сервера"):
        content_type = response.headers.get('Content-Type', '').lower()

        if 'application/json' in content_type:
            response_data = response.json()
            # Проверяем наличие сообщения об ошибке
            error_found = any(
                "method not allowed" in str(value).lower() or 
                "405" in str(value).lower()
                for value in response_data.values()
            )
            assert error_found, f"В JSON ответе должно быть сообщение об ошибке: {response_data}"
        else:
            # Для не-JSON ответов проверяем текст
            response_text = response.text.lower()
            assert "method not allowed" in response_text or "405" in response_text, f"Ответ не содержит ожидаемую ошибку: {response_text}"


@allure.epic("API Тестирование")
@allure.feature("Корзина покупок")
@allure.story("Негативные сценарии")
@allure.severity(allure.severity_level.NORMAL)
def test_negative_add_to_cart_empty_value():
    """
    Негативный тест: добавление товара в корзину с пустым/невалидным значением
    Ожидаемый результат: ошибка 400 или 422
    """
    # Тестовые данные с пустым ID
    payload_empty = {
        "id": None  # Пустое значение
    }

    # Тестовые данные с отрицательным ID
    payload_negative = {
        "id": -1  # Невалидное значение
    }

    # Тестовые данные с строковым ID
    payload_string = {
        "id": "invalid_id"  # Неправильный тип данных
    }

    with allure.step("Тестирование пустого значения ID (None)"):
        response_empty = requests.post(Base_URL + 'cart/product', headers=headers, json=payload_empty)
        assert response_empty.status_code == 422, f"Ожидался статус код 422 для пустого значения, получен {response_empty.status_code}"

    with allure.step("Тестирование отрицательного значения ID (-1)"):
        response_negative = requests.post(Base_URL + 'cart/product', headers=headers, json=payload_negative)
        assert response_negative.status_code == 422, f"Ожидался статус код 422 для отрицательного значения, получен {response_negative.status_code}"

    with allure.step("Тестирование строкового значения ID ('invalid_id')"):
        response_string = requests.post(Base_URL + 'cart/product', headers=headers, json=payload_string)
        assert response_string.status_code == 400, f"Ожидался статус код 400 для строкового значения, получен {response_string.status_code}"
