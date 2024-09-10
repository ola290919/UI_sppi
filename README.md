# SPPI WEB E2E Tests

Тесты для веб приложения SPPI.

## Установка

Перед запуском установить Python 3.12 и выше.

Установить библиотеку ```pip install pytest-playwright``` и браузеры ```playwright install```

Загрузить все необходимые пакеты через ```pip install -r requirements.txt```.

Необходимые для запуска проекта переменные указаны в файле ```.env.example```.

Генерация отчета allure ```C:\Users\mx\Downloads\allure-2.29.0\allure-2.29.0\bin\allure.bat generate allure-results --clean```

Установка переменной ```$Env:JAVA_HOME = "C:\Program Files\Java\jre1.8.0_421"```

## Запуск

`pytest`

### Структура

```text
/
│
├── pages/
│   └── ...
│
├── utils/
│   │── sppi_auth_client.py
│   └── ...
│
├── tests/
│   └── ...
```

В директории [pages](pages) находятся описания страниц по паттерну PageObject.

В директории [utils](utils) находятся разнообразные утилиты, помогающие в тестировании.

В директории [tests](tests) находятся тесты.

### Утилиты

#### sppi_auth_client

[Класс SppiAuthClient](utils/sppi_web_client.py) используется для авторизации и работы с приложением СППИ.

#### sppi_api_client

[Класс SppiApiClient](utils/sppi_api_client.py) используется для обращения к API СППИ при формировании данных авторизации, а также формирования `set up` в фикстурах для тестирования.

#### helpers

В [файле auth_helpers](utils/pw_helpers.py) находятся функции для формирования данных авторизации.

В [файле pw_helpers](utils/pw_helpers.py) находятся функции и классы для работы с Playwright.
