import allure
import pytest

from utils.api_client import YouGileApiClient

pytestmark = pytest.mark.api


@pytest.mark.api
@allure.title("Получение списка колонок доски")
@allure.story("Управление колонками")
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
        "Не удалось создать "
        + f"доску: {board_response.status_code} {board_response.text}"
    )

    board_id = board_response.json().get("id")

    assert board_id, "В ответе отсутствует ID созданной доски"

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

        assert "paging" in data, "В ответе отсутствует поле paging"

        assert "content" in data, "В ответе отсутствует поле content"

        assert isinstance
        (
            data["content"], list
        ), "Поле content должно быть массивом"

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

        assert created_column is not None
        "Созданная колонка отсутствует в списке"

        assert created_column["boardId"] == board_id
        assert created_column["title"] == "Колонка для API-теста"
