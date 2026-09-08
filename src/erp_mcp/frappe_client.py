import os

import httpx


class FrappeConfigError(RuntimeError):
    pass


class FrappeClient:
    """Thin wrapper over the Frappe/ERPNext REST API using token auth."""

    def __init__(self) -> None:
        base_url = os.environ.get("FRAPPE_URL", "").rstrip("/")
        api_key = os.environ.get("FRAPPE_API_KEY", "")
        api_secret = os.environ.get("FRAPPE_API_SECRET", "")

        if not base_url or not api_key or not api_secret:
            raise FrappeConfigError(
                "Thieu cau hinh FRAPPE_URL / FRAPPE_API_KEY / FRAPPE_API_SECRET. "
                "Hay tao file .env tu .env.example va dien gia tri that vao."
            )

        self.base_url = base_url
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"token {api_key}:{api_secret}",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    def close(self) -> None:
        self._client.close()

    def _raise_for_status(self, response: httpx.Response) -> None:
        if response.status_code >= 400:
            detail = response.text
            try:
                data = response.json()
                detail = data.get("exception") or data.get("_server_messages") or detail
            except ValueError:
                pass
            raise RuntimeError(f"Frappe API loi {response.status_code}: {detail}")

    def list_docs(
        self,
        doctype: str,
        filters: list | None = None,
        fields: list[str] | None = None,
        limit_page_length: int = 20,
        order_by: str | None = None,
    ) -> list[dict]:
        params: dict = {"limit_page_length": limit_page_length}
        if filters:
            params["filters"] = str(filters)
        if fields:
            params["fields"] = str(fields)
        if order_by:
            params["order_by"] = order_by

        response = self._client.get(f"/api/resource/{doctype}", params=params)
        self._raise_for_status(response)
        return response.json().get("data", [])

    def get_doc(self, doctype: str, name: str) -> dict:
        response = self._client.get(f"/api/resource/{doctype}/{name}")
        self._raise_for_status(response)
        return response.json().get("data", {})

    def create_doc(self, doctype: str, data: dict) -> dict:
        response = self._client.post(f"/api/resource/{doctype}", json=data)
        self._raise_for_status(response)
        return response.json().get("data", {})

    def update_doc(self, doctype: str, name: str, data: dict) -> dict:
        response = self._client.put(f"/api/resource/{doctype}/{name}", json=data)
        self._raise_for_status(response)
        return response.json().get("data", {})

    def delete_doc(self, doctype: str, name: str) -> None:
        response = self._client.delete(f"/api/resource/{doctype}/{name}")
        self._raise_for_status(response)

    def call_method(self, method_path: str, params: dict | None = None) -> dict:
        response = self._client.post(f"/api/method/{method_path}", json=params or {})
        self._raise_for_status(response)
        return response.json()
