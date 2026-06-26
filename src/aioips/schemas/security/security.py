"""Схемы прав доступа (безопасности) IPS.

Описывают, какие действия (``ActionType``) и для каких субъектов (пользователей,
групп, ролей) разрешены/запрещены на защищаемой сущности — объекте, типе объекта,
атрибуте или операции над объектами. Это «снимок» прав, который IPS отдаёт по
GET-эндпоинтам раздела ``/core/api/security/*``.

Терминология IPS:
- «цель» (target) — субъект безопасности: пользователь, группа пользователей или роль;
- «действие» (action) — операция над сущностью (см. перечень ``ActionType``: чтение,
  изменение, удаление, печать и т.п.);
- «право» (permission) — связка «цель × действие × вид доступа» (``AccessType``:
  default/grant/deny/grantAlways/noGrant).

Перечисления ``ActionType`` / ``ActionCategory`` / ``AccessType`` в этой версии библиотеки
ещё не вынесены в ``aioips.common.enumerations``, поэтому соответствующие поля
типизированы как ``str`` (точные строковые значения см. в swagger). Это сознательное
упрощение, устойчивое к появлению новых значений на стороне сервера.

References:
    ``GET /core/api/security/objects/{objectVersionId}`` — ``Security_GetObjectSecurity``.
    ``GET /core/api/security/objectTypes/{objectTypeId}`` — ``Security_GetObjectTypeSecurity``.
    ``GET /core/api/security/objectTypes`` — ``Security_GetObjectTypeCollectionSecurity``.
    ``GET /core/api/security/attributes/{attributeId}`` — ``Security_GetAttributeSecurity``.
    ``GET /core/api/security/actionOnObjects`` — ``Security_GetActionsOnObjectsSecurity``.
    Источник: ``SecurityDto`` и вложенные DTO IPS Server Web API.
"""

from datetime import datetime
from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class SecurityTarget(IPSModel):
    """Целевой субъект безопасности (пользователь, группа пользователей или роль).

    Идентифицирует, КОМУ адресованы права в данном снимке безопасности. Конкретный вид
    субъекта определяется на стороне IPS (тип цели в ``target_type_id``).

    Attributes:
        target_id: Идентификатор версии объекта-субъекта (пользователь/группа/роль).
        target_type_id: Тип объекта-субъекта.
        target_name: Заголовок (отображаемое имя) субъекта.
        is_full_default_permissions: Все настройки для субъекта являются настройками
            по умолчанию.
    """

    target_id: int = Field(description="Идентификатор версии объекта-субъекта")
    target_type_id: int | None = Field(default=None, description="Тип объекта-субъекта")
    target_name: str | None = Field(default=None, description="Заголовок субъекта безопасности")
    is_full_default_permissions: bool = Field(
        default=False, description="Все настройки субъекта — по умолчанию"
    )


class SecurityAction(IPSModel):
    """Описание действия (операции), которое может контролироваться правами доступа.

    Перечисляет доступные для защищаемой сущности действия и их категории (чтение,
    изменение, администрирование). Значения ``action_id`` соответствуют перечислению
    ``ActionType`` (типизировано как ``str``: эти enum'ы пока не вынесены в библиотеку).

    Attributes:
        action_id: Идентификатор действия (значение ``ActionType``, например ``read``).
        action_name: Человекочитаемое описание действия.
        action_category_id: Категория действия (``ActionCategory``: ``read`` / ``write`` /
            ``admin`` / ``notDefined``).
        action_category_name: Описание категории действия.
        is_allow_by_default: Дано ли право на действие по умолчанию всем пользователям.
        related_action_ids: Связанные действия, права которых снимаются вместе с этим.
    """

    action_id: str = Field(description="Идентификатор действия (ActionType)")
    action_name: str | None = Field(default=None, description="Описание действия")
    action_category_id: str | None = Field(
        default=None, description="Категория действия (ActionCategory)"
    )
    action_category_name: str | None = Field(
        default=None, description="Описание категории действия"
    )
    is_allow_by_default: bool = Field(
        default=False, description="Право дано по умолчанию всем пользователям"
    )
    related_action_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Связанные действия, снимаемые вместе с этим"
    )


class PermissionAction(IPSModel):
    """Право доступа: связка «субъект × действие × вид доступа».

    Базовая единица настройки безопасности — определяет, какой вид доступа
    (``AccessType``) к действию ``action_id`` предоставлен субъекту ``target_id``.

    Attributes:
        action_id: Идентификатор действия (значение ``ActionType``).
        target_id: Идентификатор субъекта безопасности (пользователь/группа/роль).
        access_type: Вид доступа (``AccessType``: ``default`` / ``noGrant`` / ``grant`` /
            ``deny`` / ``grantAlways``).
        is_default_permission: Настройка доступа является настройкой по умолчанию.
    """

    action_id: str = Field(description="Идентификатор действия (ActionType)")
    target_id: int = Field(description="Идентификатор субъекта безопасности")
    access_type: str | None = Field(default=None, description="Вид доступа (AccessType)")
    is_default_permission: bool = Field(
        default=False, description="Настройка доступа — по умолчанию"
    )


class PermissionDuration(IPSModel):
    """Срок действия прав доступа для субъекта.

    Ограничивает права во времени интервалом ``[start_date_time; end_date_time]``.

    Attributes:
        target_id: Идентификатор субъекта безопасности.
        start_date_time: Начало действия прав доступа (UTC).
        end_date_time: Окончание действия прав доступа (UTC).
    """

    target_id: int = Field(description="Идентификатор субъекта безопасности")
    start_date_time: datetime | None = Field(
        default=None, description="Начало действия прав доступа"
    )
    end_date_time: datetime | None = Field(
        default=None, description="Окончание действия прав доступа"
    )


class PermissionCondition(IPSModel):
    """Условие проверки прав доступа для субъекта.

    Привязывает дополнительное условие (``condition_id``) к правам субъекта; перечень
    условий определяется конфигурацией IPS.

    Attributes:
        target_id: Идентификатор субъекта безопасности.
        condition_id: Идентификатор условия проверки прав.
    """

    target_id: int = Field(description="Идентификатор субъекта безопасности")
    condition_id: int | None = Field(default=None, description="Идентификатор условия")


class Security(IPSModel):
    """Снимок прав доступа на защищаемую сущность IPS (``SecurityDto``).

    Сводное описание безопасности: кто (``targets``) и какие действия (``actions``)
    может выполнять над сущностью, с конкретными правами (``permissions``), сроками
    (``durations``) и условиями (``conditions``). Возвращается GET-методами раздела
    :class:`aioips.methods.security.SecurityAPI` для объекта, типа объекта, коллекции
    типов, атрибута и операций над объектами.

    Когда применять: чтобы прочитать (аудит, отображение «кто что может») текущие
    настройки прав, не изменяя их. Это read-only представление; изменение прав в
    данной версии библиотеки не реализовано.

    Все списочные поля устойчивы к ``null`` в ответе (приводятся к ``[]``). Поле
    ``related_securities`` рекурсивно ссылается на :class:`Security` — IPS может
    вкладывать связанные снимки прав.

    Attributes:
        security_name: Внутреннее имя набора прав (для категории или сущности).
        category_type: Идентификатор категории сущности.
        category_id: Идентификатор типа категории сущности.
        targets: Субъекты безопасности (пользователи/группы/роли), упомянутые в наборе.
        actions: Контролируемые действия над сущностью.
        permissions: Конкретные права (субъект × действие × вид доступа).
        durations: Сроки действия прав по субъектам.
        conditions: Условия проверки прав по субъектам.
        is_conditions_enabled: Включена ли проверка условий доступа.
        related_securities: Вложенные связанные снимки прав (рекурсивно).
    """

    security_name: str | None = Field(default=None, description="Внутреннее имя набора прав")
    category_type: int | None = Field(default=None, description="Идентификатор категории сущности")
    category_id: int | None = Field(
        default=None, description="Идентификатор типа категории сущности"
    )
    targets: Annotated[list[SecurityTarget], EmptyListIfNone] = Field(
        default_factory=list, description="Субъекты безопасности (пользователи/группы/роли)"
    )
    actions: Annotated[list[SecurityAction], EmptyListIfNone] = Field(
        default_factory=list, description="Контролируемые действия над сущностью"
    )
    permissions: Annotated[list[PermissionAction], EmptyListIfNone] = Field(
        default_factory=list, description="Права (субъект × действие × вид доступа)"
    )
    durations: Annotated[list[PermissionDuration], EmptyListIfNone] = Field(
        default_factory=list, description="Сроки действия прав по субъектам"
    )
    conditions: Annotated[list[PermissionCondition], EmptyListIfNone] = Field(
        default_factory=list, description="Условия проверки прав по субъектам"
    )
    is_conditions_enabled: bool = Field(
        default=False, description="Включена ли проверка условий доступа"
    )
    related_securities: Annotated[list["Security"], EmptyListIfNone] = Field(
        default_factory=list, description="Вложенные связанные снимки прав"
    )
