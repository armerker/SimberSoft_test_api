import requests
import allure


class RequestWrapper:
    """Обертка над requests с логированием в Allure."""

    def __init__(self, auth: tuple):
        self.auth = auth
        self.session = requests.Session()
        self.session.auth = auth
        self.session.headers.update({"Content-Type": "application/json"})

    def _log_request(self, method: str, url: str, **kwargs):
        """Логирует запрос в Allure."""
        with allure.step(f"{method} {url}"):
            allure.attach(method, name="Method", attachment_type=allure.attachment_type.TEXT)
            allure.attach(url, name="URL", attachment_type=allure.attachment_type.TEXT)

            if "json" in kwargs:
                allure.attach(
                    str(kwargs["json"]),
                    name="Request Body",
                    attachment_type=allure.attachment_type.JSON
                )
            if "params" in kwargs:
                allure.attach(
                    str(kwargs["params"]),
                    name="Request Params",
                    attachment_type=allure.attachment_type.TEXT
                )

    def _log_response(self, response: requests.Response):
        """Логирует ответ в Allure."""
        allure.attach(
            str(response.status_code),
            name="Response Status",
            attachment_type=allure.attachment_type.TEXT
        )

        try:
            response_json = response.json()
            allure.attach(
                str(response_json)[:1000],
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
        except:
            allure.attach(
                response.text[:1000],
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT
            )

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Отправляет HTTP запрос с логированием."""
        self._log_request(method, url, **kwargs)
        response = self.session.request(method, url, **kwargs)
        self._log_response(response)
        return response

    def get(self, url: str, **kwargs) -> requests.Response:
        """GET запрос."""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """POST запрос."""
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> requests.Response:
        """PUT запрос."""
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        """DELETE запрос."""
        return self.request("DELETE", url, **kwargs)