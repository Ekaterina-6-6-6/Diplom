import allure
import requests


from config.settings import settings
from utils.api_client import YouGileApiClient


@allure.title("Получение API-ключа с корректными данными")
@allure.description("Проверка успешной авторизации через API YouGile.")
def test_create_api_key(
    base_url: str,
    login: str,
    password: str,
    company_id: str,
) -> None:
    """Проверяет получение API-ключа с корректными данными."""

    with allure.step("Отправить запрос на получение API-ключа"):
        response = requests.post(
            f"{base_url}/api-v2/auth/keys",
            json={
                "login": login,
                "password": password,
                "companyId": company_id,
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 201

    with allure.step("Проверить наличие API-ключа в ответе"):
        response_data = response.json()

        assert "key" in response_data
        assert response_data["key"]


@allure.title("Создание проекта с корректным названием")
@allure.description("Проверка создания проекта через API YouGile.")
def test_create_project(api_token: str, base_url: str) -> None:
    """Проверяет создание проекта и получение его ID."""

    project_title = "Автотест проект"

    with allure.step("Отправить запрос на создание проекта"):
        response = requests.post(
            f"{base_url}/api-v2/projects",
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            },
            json={
                "title": project_title,
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 201

    with allure.step("Проверить наличие ID созданного проекта"):
        response_data = response.json()
        assert "id" in response_data
        assert response_data["id"]


@allure.title("Получение проекта по ID")
@allure.description(
    "Проверка получения ранее созданного проекта через API YouGile."
)
def test_get_project(
    api_client: YouGileApiClient,
    created_project_id: str,
) -> None:
    """Проверяет получение проекта по его ID."""

    with allure.step("Получить проект по ID"):
        response = api_client.get_project(
            created_project_id
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200

    with allure.step("Проверить данные проекта"):
        project = response.json()

        assert project["id"] == created_project_id
        assert "title" in project
        assert project["title"] == "Проект для API-тестов"
        assert "timestamp" in project


@allure.title("Создание задачи")
@allure.description(
    "Проверка создания задачи в колонке через API YouGile."
)
def test_create_task(
    api_client: YouGileApiClient,
    created_column_id: str,
) -> None:
    """Проверяет создание задачи в существующей колонке."""

    with allure.step("Создать тестовую задачу"):
        response = api_client.create_task(
            "Задача для API-тестов",
            created_column_id,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 201, (
            "Задача не создана: "
            f"{response.status_code} {response.text}"
        )

    with allure.step("Проверить ID созданной задачи"):
        task_id = response.json().get("id")

        assert task_id, "В ответе отсутствует ID созданной задачи"


@allure.title("Получение списка задач")
@allure.description(
    "Проверка получения списка задач через API YouGile."
)
def test_get_tasks(
    api_client: YouGileApiClient,
) -> None:
    """Проверяет получение списка задач."""

    with allure.step("Отправить запрос на получение списка задач"):
        response = api_client.get_tasks(
            limit=50,
            offset=0,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200, (
            "Не удалось получить список задач: "
            f"{response.status_code} {response.text}"
        )

    with allure.step("Проверить структуру ответа"):
        data = response.json()

        assert "paging" in data, (
            "В ответе отсутствует поле paging"
        )
        assert "content" in data, (
            "В ответе отсутствует поле content"
        )

        assert isinstance(data["content"], list), (
            "Поле content должно быть массивом"
        )


@allure.title("Получение списка досок проекта")
@allure.description(
    "Проверка получения списка досок через API YouGile."
)
def test_get_boards(
    api_client: YouGileApiClient,
    created_project_id: str,
) -> None:
    """Проверяет получение списка досок проекта."""

    with allure.step("Получить список досок проекта"):
        response = api_client.get_boards(
            created_project_id,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200, (
            "Не удалось получить список досок: "
            f"{response.status_code} {response.text}"
        )

    with allure.step("Проверить структуру ответа"):
        data = response.json()

        assert "paging" in data, (
            "В ответе отсутствует поле paging"
        )
        assert "content" in data, (
            "В ответе отсутствует поле content"
        )

        assert isinstance(data["content"], list), (
            "Поле content должно быть массивом"
        )

    with allure.step("Проверить принадлежность досок проекту"):
        for board in data["content"]:
            assert board["projectId"] == created_project_id


@allure.title("Получение списка колонок доски")
@allure.description(
    "Проверка получения списка колонок через API YouGile."
)
def test_get_columns(
    api_client: YouGileApiClient,
    created_project_id: str,
) -> None:
    """Проверяет получение списка колонок доски."""

    with allure.step("Создать тестовую доску"):
        board_response = api_client.create_board(
            "Доска для получения колонок",
            created_project_id,
        )

    assert board_response.status_code == 201, (
        "Не удалось создать доску: "
        f"{board_response.status_code} "
        f"{board_response.text}"
    )

    board_id = board_response.json().get("id")

    assert board_id, (
        "В ответе отсутствует ID созданной доски"
    )

    with allure.step("Создать тестовую колонку"):
        column_response = api_client.create_column(
            "Колонка для API-теста",
            board_id,
        )

    assert column_response.status_code == 201, (
        "Не удалось создать колонку: "
        f"{column_response.status_code} "
        f"{column_response.text}"
    )

    with allure.step("Получить список колонок доски"):
        response = api_client.get_columns(
            board_id,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200, (
            "Не удалось получить список колонок: "
            f"{response.status_code} "
            f"{response.text}"
        )

    with allure.step("Проверить структуру ответа"):
        data = response.json()

        assert "paging" in data, (
            "В ответе отсутствует поле paging"
        )

        assert "content" in data, (
            "В ответе отсутствует поле content"
        )

        assert isinstance(data["content"], list), (
            "Поле content должно быть массивом"
        )

    with allure.step("Проверить созданную колонку"):
        columns = data["content"]

        created_column = next(
            (
                column
                for column in columns
                if column["id"] == column_response.json()["id"]
            ),
            None,
        )

        assert created_column is not None, (
            "Созданная колонка отсутствует в списке"
        )

        assert created_column["boardId"] == board_id
        assert created_column["title"] == "Колонка для API-теста"


@allure.title("Получение API-ключа с неверным паролем")
@allure.description(
    "Проверка отказа в авторизации при использовании неверного пароля."
)
def test_create_api_key_invalid_password() -> None:
    """Проверяет получение API-ключа с неверным паролем."""

    with allure.step("Отправить запрос с неверным паролем"):
        response = requests.post(
            f"{settings.base_url}/api-v2/auth/keys",
            json={
                "login": settings.login,
                "password": "WrongPassword123!",
                "companyId": settings.company_id,
            },
            headers={
                "Content-Type": "application/json",
            },
            timeout=15,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 401, (
            "Ожидался статус 401 Unauthorized, "
            f"получен {response.status_code}: {response.text}"
        )

    with allure.step("Проверить отсутствие API-ключа"):
        assert "key" not in response.json()


@allure.title("Получение проекта с несуществующим ID")
@allure.description(
    "Проверка корректной обработки запроса проекта с несуществующим ID."
)
def test_get_project_not_found(
    api_client: YouGileApiClient,
) -> None:
    """Проверяет получение проекта с несуществующим ID."""

    fake_project_id = "00000000-0000-0000-0000-000000000000"

    with allure.step("Запросить проект с несуществующим ID"):
        response = api_client.get_project(fake_project_id)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 404, (
            "Ожидался статус 404 для несуществующего проекта: "
            f"{response.status_code} {response.text}"
        )


@allure.title("Создание проекта проект с пустым названием")
@allure.description("Проверка создания проекта через API YouGile.")
def test_create_project_empty_title(api_token: str, base_url: str) -> None:
    """Проверяет создание проекта с пустым названием."""

    project_title = ""

    with allure.step("Отправить запрос на создание проекта"):
        response = requests.post(
            f"{base_url}/api-v2/projects",
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            },
            json={
                "title": project_title,
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 400, (
            "Ожидался статус 400 для проекта с пустым названием: "
            f"{response.status_code} {response.text}"
        )


@allure.title("Создание задачи с несуществующей колонкой")
@allure.description(
    "Проверка отказа при создании задачи с несуществующим ID колонки "
    "через API YouGile."
)
def test_create_task_invalid_column_id(
    api_client: YouGileApiClient,
) -> None:
    """Проверяет отказ при создании задачи в несуществующей колонке."""

    invalid_column_id = "00000000-0000-0000-0000-000000000000"

    with allure.step("Создать задачу с несуществующим ID колонки"):
        response = api_client.create_task(
            "Задача для API-тестов",
            invalid_column_id,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 404, (
            "API не вернул ожидаемый статус 404: "
            f"{response.status_code} {response.text}"
        )
