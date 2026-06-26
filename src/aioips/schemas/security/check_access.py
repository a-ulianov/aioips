"""Схема запроса проверки прав доступа текущего пользователя (``checkAccess``).

Описывает тело POST-запросов раздела ``/core/api/security/*/checkAccess``: какое
право (``ActionType``) нужно проверить у ТЕКУЩЕГО пользователя на конкретную цель
защиты (систему, тип объекта, атрибут, шаг ЖЦ, объект и т.п.). Это read-проверка:
сервер только вычисляет результат, права при этом не меняются.

References:
    ``CheckAccessDto`` IPS Server Web API («Модель для проверки прав доступа»).
    Эндпоинты ``POST /core/api/security/.../checkAccess``.
"""

from pydantic import Field

from ..base import IPSModel


class SecurityCheckAccess(IPSModel):
    """Тело запроса проверки доступа (``CheckAccessDto``).

    Задаёт, какое право проверить и как трактовать неопределённость. Передаётся в
    методы ``check_*_security_access`` раздела :class:`aioips.methods.security.SecurityAPI`.
    Проверяется доступ ТЕКУЩЕГО пользователя (того, чьим токеном авторизован клиент) —
    отдельного субъекта в этой модели нет; цель защиты задаётся путём эндпоинта.

    Замечание по типу ``action_type``: в swagger это перечисление ``ActionType`` со
    строковыми значениями (``read``, ``edit``, ``delete``, ``print``, ``getAccess`` и
    т.п.), поэтому поле типизировано как ``str`` (а не ``int``), согласованно с тем, как
    ``action_id`` уже типизирован в :class:`aioips.schemas.security.SecurityAction`.
    Эти enum'ы пока не вынесены в ``aioips.common.enumerations``.

    Attributes:
        action_type: Право (действие ``ActionType``), которое нужно проверить, например
            ``"read"`` / ``"edit"`` / ``"delete"`` / ``"print"``. Алиас JSON ``actionType``.
        default_access: Что вернуть, если на данную цель текущему пользователю права ещё
            НЕ назначали. ``None`` (по умолчанию) — взять значение по умолчанию из списка
            возможных прав для цели. Алиас JSON ``defaultAccess``.
        throw_ac_exception: Поведение при отсутствии прав. ``False`` (по умолчанию) —
            вернуть результат проверки (``true``/``false``). ``True`` — при отсутствии
            прав сервер бросает ``AccessDeniedException`` (HTTP 403). Алиас JSON
            ``throwACException``.
    """

    action_type: str | None = Field(
        default=None,
        alias="actionType",
        description="Право (ActionType), которое нужно проверить",
    )
    default_access: bool | None = Field(
        default=None,
        alias="defaultAccess",
        description="Результат, если права на цель ещё не назначали (None — взять дефолт цели)",
    )
    throw_ac_exception: bool = Field(
        default=False,
        alias="throwACException",
        description="True — бросить AccessDeniedException при отсутствии прав вместо false",
    )
