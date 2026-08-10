## Описание проекта

# YouGile — API и UI автотесты

Автоматизированные тесты для проверки REST API и пользовательского интерфейса YouGile.

## Ссылки

- Тест-план: https://novok-123.yonote.ru/share/ec52ee4d-cce1-470d-9240-9f1e5c96285e
- Результаты тестирования: https://novok-123.yonote.ru/share/36429ae2-41b9-4af9-a6fa-7f7e310247b9
- YouGile: https://ru.yougile.com/
- YouGile REST API: https://ru.yougile.com/api-v2#/

---

## Структура проекта

```text
Diplom/
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── pages/
│   ├── __init__.py
│   └── MainPage.py
│
│
├── tests/
│   ├── test_api/
│   │   ├── test_create_task_invalid_column_id.py
│   │   ├── gest_get_boards.py
│   │   ├── test_create_api_key.py
│   │   ├── test_create_api_key_invalid_password.py
│   │   ├── test_create_project.py
│   │   ├── test_create_project_empty_title.py
│   │   ├── test_create_task.py
│   │   ├── test_get_columns.py
│   │   ├── test_get_project.py
│   │   ├── test_get_project_not_found.py
│   │   └── test_get_tasks.py
│   │
│   ├── test_ui/
│   │   ├── test_cancel_create_crm_project.py
│   │   ├── test_cancel_create_project.py
│   │   ├── test_create_crm_project.py
│   │   ├── test_create_project_ui.py
│   │   ├── test_login_yougile.py
│   │   └── test_open_create_project_form.py
│   │
│   └── __init__.py
│
├── utils/
│   ├── __init__.py
│   └── api_client.py
│
├── .env.example
├── .gitignore
├── API_REQUESTS.md
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

> Папки `.venv`, `.pytest_cache`, `.idea`, `allure-results`, `allure-report` и файл `.env` являются локальными и в итоговый архив не включены.

---

## Назначение основных файлов

### `config/settings.py`

Загружает настройки из `.env` и формирует объект `settings`:

- `YOUGILE_BASE_URL` — адрес YouGile;
- `YOUGILE_LOGIN` — логин;
- `YOUGILE_PASSWORD` — пароль;
- `YOUGILE_COMPANY_ID` — ID компании.

### `conftest.py`

Содержит общие pytest fixtures:

- API-токен;
- API client;
- URL;
- логин/пароль;
- ID компании;
- HTTP session;
- заголовки авторизации;
- создание тестового проекта;
- создание тестовой доски и колонки;
- запуск Chrome для UI-тестов.

### `utils/api_client.py`

Клиент для REST API YouGile.

Реализованы запросы:

- получение API-ключа;
- создание проекта;
- получение проекта;
- создание доски;
- получение досок;
- создание колонки;
- получение колонок;
- создание задачи;
- получение списка задач.

### `pages/`

Каталог Page Object. `MainPage.py` содержит базовый объект главной страницы. Остальные page-файлы подготовлены под дальнейшее развитие Page Object.

### `tests/test_api/`

API-тесты:

- получение API-ключа;
- проверка неверного пароля;
- создание проекта;
- создание проекта с пустым названием;
- получение проекта;
- получение несуществующего проекта;
- получение досок;
- получение колонок;
- создание задачи;
- создание задачи с неверным ID колонки;
- получение списка задач.

### `tests/test_ui/`

UI-тесты:

- авторизация;
- открытие формы создания проекта;
- создание проекта;
- отмена создания проекта;
- создание CRM-проекта;
- отмена создания CRM-проекта;
- дополнительные UI-сценарии.

### `pytest.ini`

Содержит настройки pytest и маркеры:

```text
api — API-тесты
ui  — UI-тесты
```

---

# Установка

## 1. Создать виртуальное окружение

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. Установить зависимости

```powershell
pip install -r requirements.txt
```

## 3. Создать `.env`

Скопировать `.env.example`:

```powershell
Copy-Item .env.example .env
```

Заполнить реальные значения:

```env
YOUGILE_BASE_URL=https://ru.yougile.com
YOUGILE_LOGIN=ваш_логин
YOUGILE_PASSWORD=ваш_пароль
YOUGILE_COMPANY_ID=id_компании
YOUGILE_API_TOKEN=api_ключ
```

**Важно:** `.env` не должен попадать в Git.

---

# Запуск тестов

## Только UI

Запустить все UI-тесты:

```powershell
pytest -m ui -s -v
```

Запустить конкретный UI-тест:

```powershell
pytest -m ui -s -v -k test_login_yougile
```

---

## Только API

Запустить все API-тесты:

```powershell
pytest -m api -s -v
```

Запустить конкретный API-тест:

```powershell
pytest -m api -s -v -k test_create_project
```

---

## Все тесты

```powershell
pytest -s -v
```

---

# Allure

Все тесты в проекте используют `allure-pytest`.

## Только UI + Allure

```powershell
pytest -m ui -s -v --alluredir=allure-results
allure serve allure-results
```

## Только API + Allure

```powershell
pytest -m api -s -v --alluredir=allure-results
allure serve allure-results
```

## Все тесты + Allure

```powershell
pytest -s -v --alluredir=allure-results
allure serve allure-results
```

После запуска `allure serve` Allure откроет HTML-отчёт в браузере.

Если нужно сохранить отчёт в отдельную папку:

```powershell
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

# Полезные команды

Показать все тесты:

```powershell
pytest --collect-only -q
```

Запустить тесты без подробного вывода:

```powershell
pytest -q
```

Запустить API-тесты с Allure:

```powershell
pytest -m api --alluredir=allure-results
```

Запустить UI-тесты с Allure:

```powershell
pytest -m ui --alluredir=allure-results
```

---

# Данные для API-запросов

Подробные методы, URL, JSON-тела запросов, тестовые значения и ожидаемые статус-коды вынесены в:

**`API_REQUESTS.md`**

Основные endpoint:

| Метод | Endpoint | Назначение |
|---|---|---|
| POST | `/api-v2/auth/keys` | получение API-ключа |
| POST | `/api-v2/projects` | создание проекта |
| GET | `/api-v2/projects/{project_id}` | получение проекта |
| POST | `/api-v2/boards` | создание доски |
| GET | `/api-v2/boards` | получение досок |
| POST | `/api-v2/columns` | создание колонки |
| GET | `/api-v2/columns` | получение колонок |
| POST | `/api-v2/tasks` | создание задачи |
| GET | `/api-v2/task-list` | получение списка задач |

---

# Переменные окружения

| Переменная | Назначение |
|---|---|
| `YOUGILE_BASE_URL` | базовый URL YouGile |
| `YOUGILE_LOGIN` | логин тестового пользователя |
| `YOUGILE_PASSWORD` | пароль тестового пользователя |
| `YOUGILE_COMPANY_ID` | ID компании |
| `YOUGILE_API_TOKEN` | API-ключ для API-тестов |

Реальные значения намеренно не хранятся в README и не добавляются в Git.

---

# Git и `.idea`

В `.gitignore` добавлено:

```gitignore
.idea/
```

Если `.idea` уже была добавлена в Git ранее, одного `.gitignore` недостаточно. Для удаления её из индекса:

```powershell
git rm -r --cached .idea
git commit -m "chore: ignore IDE files"
```

Если `.idea` никогда не была закоммичена, достаточно правила `.idea/` в `.gitignore`.

---

# Примечание

UI-тест переименования проекта временно не является частью текущей задачи по исправлению автотестов. Его дальнейшее исправление можно выполнить отдельно после стабилизации локаторов меню проекта.
