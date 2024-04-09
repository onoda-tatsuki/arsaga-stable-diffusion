from typing import Any, Optional


class APIException(Exception):
    # カスタムエラー
    DEFAULT_MESSAGE = "Image generation failed for some reason."

    def __init__(
        self,
        error: Any,
        status_code: Optional[str] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        try:
            error_obj = error()
        except Exception:
            error_obj = error

        try:
            message = error_obj.text
        except Exception:
            message = str(error_obj)

        self.status_code = status_code
        self.headers = headers
        self.id = str(error_obj)
        self.detail = message
