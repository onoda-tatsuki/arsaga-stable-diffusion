from typing import Any, Optional, Union


class APIException(Exception):

    def __init__(
        self,
        error: Any,
        status_code: Optional[int] = None,
        content: Optional[Union[str, Any]] = None,
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
        self.detail = (
            {"description": message, "detail": content} if content else message
        )
