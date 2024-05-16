# cft-test
Тестовое задание на Python-разработчика в ЦФТ. Залил сюда потому что mos.ru работает на костылях.

## Запуск проекта (порт 3550)

    pip install fastapi uvicorn sqlalchemy fastapi-jwt[authlib]
    python main.py

## Роуты

    /register - создание пользователя
    Обязательные параметры: login, password, salary, raisedate
    raisedate указывается в формате YYYY-MM-DD

    /login - авторизация
    Обязательные параметры: login, password

    /salaryinfo - информация о зарплате и дате повышения
    Обязательные параметры: Bearer Token

## Реализация

Локальный sqlite для базы данных,
sqlalchemy как ORM,
fastapi_jwt для генерации и валидации токена,
fernet для шифрования пароля,
uvicorn для сервера

На Питоне до этого почти не писал, потратил ~2 часов в документации на разных ресурсах
