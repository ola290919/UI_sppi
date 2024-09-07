# UI Tests





## Структура проекта

-




## Инструкция установки и запуска тестов

Перед запуском установить Python 3.12 и выше.
Установить библиотеку ```pip install pytest-playwright``` и браузеры ```playwright install```

Загрузить все необходимые пакеты через ```pip install -r requirements.txt```.

```pip install playwright```
```playwright install```

Необходимые для запуска проекта переменные указаны в файле ```.env.example```.

Конфигурация запуска тестов в файле ```pytest.ini```.

Запустить тест с маркой (например, smoke) ```pytest -m smoke```. Вывести все марки (свои и дефолтные) ```pytest --markers```.

