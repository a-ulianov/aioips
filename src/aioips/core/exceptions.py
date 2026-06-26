"""Иерархия исключений клиента IPS Web API.

Ответы об ошибках IPS приходят в формате ``ApiProblemDetails`` (RFC 7807-подобный):
``{"type", "title", "status", "detail", "instance"}``. Функция
:func:`exception_from_response` разбирает такое тело и подбирает подходящий
класс исключения по HTTP-коду.
"""

from typing import Any


class IPSError(Exception):
    """Базовое исключение для всех ошибок клиента IPS.

    Корень иерархии: ловите его, чтобы перехватить любую ошибку клиента
    (как HTTP-ответы 4xx/5xx, так и сетевые сбои). Конкретные подклассы
    соответствуют HTTP-кодам и позволяют различать причины — см. их docstrings.
    Экземпляры обычно создаёт :func:`exception_from_response` из тела
    ``ApiProblemDetails``; вручную поднимать редко нужно.

    Attributes:
        status: HTTP-код ответа (или ``0`` для сетевых/клиентских ошибок).
        message: Человекочитаемое сообщение об ошибке.
        title: Поле ``title`` из тела ``ApiProblemDetails`` (тип ошибки IPS), если есть.
        detail: Поле ``detail`` из тела ответа, если есть.
        payload: Полное тело ответа об ошибке (для диагностики).

    Examples:
        >>> from aioips import IPSError, IPSNotFoundError
        >>> issubclass(IPSNotFoundError, IPSError)
        True
        >>> try:
        ...     raise IPSNotFoundError(404, "нет объекта")
        ... except IPSError as exc:
        ...     exc.status
        404
    """

    def __init__(
        self,
        status: int,
        message: str,
        *,
        title: str | None = None,
        detail: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Инициализирует исключение IPS.

        Args:
            status: HTTP-код ответа.
            message: Краткое сообщение об ошибке.
            title: Поле ``title`` из ``ApiProblemDetails``.
            detail: Поле ``detail`` из ``ApiProblemDetails``.
            payload: Полное тело ответа об ошибке.
        """
        self.status = status
        self.message = message
        self.title = title
        self.detail = detail
        self.payload = payload or {}
        super().__init__(f"IPS API error {status}: {message}")


class IPSClientError(IPSError):
    """HTTP 400: некорректный запрос (невалидное тело/параметры).

    Возникает, когда сервер отверг запрос как синтаксически или семантически
    неверный. НЕ повторяется (детерминированная клиентская ошибка) — исправьте
    входные данные.
    """


class IPSAuthError(IPSError):
    """HTTP 401: не пройдена аутентификация или истёк токен.

    Возникает при отсутствии/недействительности токена, неудачном
    обновлении/входе либо когда токен истёк, а логин/пароль для повторного
    входа не заданы. Ядро при первом 401 пытается обновить токен и повторить
    запрос; исключение поднимается, если и это не помогло.
    """


class IPSForbiddenError(IPSError):
    """HTTP 403: аутентификация прошла, но прав на операцию недостаточно.

    Не повторяется: смените роль/уровень доступа или права в IPS.
    """


class IPSNotFoundError(IPSError):
    """HTTP 404: запрошенный ресурс не найден.

    Типичная причина в IPS — передан id версии (``F_ID``) туда, где ожидается
    id объекта (``ObjectID``/``F_OBJECT_ID``), либо объект отсутствует. Сверьтесь
    с разделением id-пространств в объектной модели IPS.
    """


class IPSConflictError(IPSError):
    """HTTP 409: конфликт состояния (нарушение жизненного цикла/блокировки).

    Например, попытка правки без checkout, объект занят другим пользователем
    или нарушено бизнес-правило. Не повторяется автоматически.
    """


class IPSTooManyRequestsError(IPSError):
    """HTTP 429: превышен лимит запросов (rate limiting).

    Транзиентная ошибка: ядро повторяет запрос с экспоненциальной задержкой
    согласно конфигурации повторов.
    """


class IPSServerError(IPSError):
    """HTTP 5xx: внутренняя ошибка сервера IPS.

    Поднимается для кода 500 и любого иного ответа ``>= 500``. Транзиентная:
    ядро повторяет запрос с экспоненциальной задержкой.
    """


class IPSConnectionError(IPSError):
    """Сетевая ошибка или таймаут при обращении к серверу IPS.

    HTTP-ответа нет, поэтому ``status`` равен ``0``. Покрывает таймаут запроса
    и низкоуровневые ошибки соединения. Транзиентная: ядро повторяет запрос.
    """


_STATUS_TO_EXCEPTION: dict[int, type[IPSError]] = {
    400: IPSClientError,
    401: IPSAuthError,
    403: IPSForbiddenError,
    404: IPSNotFoundError,
    409: IPSConflictError,
    429: IPSTooManyRequestsError,
    500: IPSServerError,
}


def exception_from_response(status: int, data: dict[str, Any] | None) -> IPSError:
    """Строит подходящее исключение по HTTP-коду и телу ответа IPS.

    Args:
        status: HTTP-код ответа.
        data: Разобранное тело ответа в формате ``ApiProblemDetails`` (или ``None``).

    Returns:
        Экземпляр одного из подклассов :class:`IPSError`, соответствующий коду.

    Examples:
        >>> err = exception_from_response(404, {"title": "NotFound", "detail": "нет объекта"})
        >>> isinstance(err, IPSNotFoundError)
        True
    """
    body = data or {}
    title = body.get("title")
    detail = body.get("detail")
    message = detail or title or f"HTTP {status}"

    exc_class = _STATUS_TO_EXCEPTION.get(status)
    if exc_class is None:
        exc_class = IPSServerError if status >= 500 else IPSError

    return exc_class(status, message, title=title, detail=detail, payload=body)
