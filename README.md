# WordPress API Autotests

Автотесты для WordPress API (посты и комментарии)

## Технологии

- Python 3.11+
- Pytest
- Requests
- MySQL
- Allure Reports

## Установка

git clone https://github.com/armerker/SimberSoft_test_api.git

cd SimberSoft_test_api

pip install -r requirements.txt



## Запуск тестов

# Все тесты
pytest

# С отчетом Allure
pytest --alluredir=allure-results
allure serve allure-results


## Структура проекта

core/              - API и DB клиенты

tests/             - тесты

conftest.py        - фикстуры pytest

config.py          - конфигурация

requirements.txt   - зависимости


## Тест-кейсы

TC-01: Создание поста

TC-02: Редактирование поста

TC-03: Удаление поста

TC-04: Создание комментария

TC-05: Редактирование комментария

TC-06: Удаление комментария