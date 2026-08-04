from typing import Any

import requests
from requests import Response


class YouGileApiClient:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    @property
    def headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }

        if self.token:
            headers["Authorization"] = (
                f"Bearer {self.token}"
            )

        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        return requests.request(
            method=method,
            url=f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=json,
            params=params,
            timeout=15,
        )

    def create_api_key(
        self,
        login: str,
        password: str,
        company_id: str,
    ) -> Response:
        return requests.post(
            f"{self.base_url}/api-v2/auth/keys",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "login": login,
                "password": password,
                "companyId": company_id,
            },
            timeout=15,
        )

    def create_project(
        self,
        title: str,
    ) -> Response:
        return self._request(
            "POST",
            "/api-v2/projects",
            json={
                "title": title,
            },
        )

    def get_project(
        self,
        project_id: str,
    ) -> Response:
        return self._request(
            "GET",
            f"/api-v2/projects/{project_id}",
        )

    def create_board(
        self,
        title: str,
        project_id: str,
    ) -> Response:
        return self._request(
            "POST",
            "/api-v2/boards",
            json={
                "title": title,
                "projectId": project_id,
            },
        )

    def get_boards(
        self,
        project_id: str | None = None,
    ) -> Response:
        params = (
            {"projectId": project_id}
            if project_id
            else None
        )

        return self._request(
            "GET",
            "/api-v2/boards",
            params=params,
        )

    def get_columns(
        self,
        board_id: str,
    ) -> Response:
        return self._request(
            "GET",
            "/api-v2/columns",
            params={
                "boardId": board_id,
            },
        )

    def create_task(
        self,
        title: str,
        column_id: str,
    ) -> Response:
        return self._request(
            "POST",
            "/api-v2/tasks",
            json={
                "title": title,
                "columnId": column_id,
            },
        )

    def get_tasks(
        self,
        **params: Any,
    ) -> Response:
        return self._request(
            "GET",
            "/api-v2/task-list",
            params=params,
        )

    def create_column(
        self,
        title: str,
        board_id: str,
        color: int = 2,
    ) -> Response:
        return self._request(
            "POST",
            "/api-v2/columns",
            json={
                "title": title,
                "color": color,
                "boardId": board_id,
            },
        )


def create_column(
    self,
    title: str,
    board_id: str,
    color: int = 2,
) -> Response:
    return self._request(
        "POST",
        "/api-v2/columns",
        json={
            "title": title,
            "color": color,
            "boardId": board_id,
        },
    )
