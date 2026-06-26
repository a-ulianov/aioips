"""Перечисления групп и прав инструментов IPS.

References:
    ``ToolSecurityGroup`` и ``ToolSecurityRights`` из компонентов схем IPS Web API.
    Возвращаются эндпоинтами ``POST /core/api/settings/getUserGroup`` и
    ``POST /core/api/settings/getUserRights``.
"""

from enum import StrEnum


class ToolSecurityGroup(StrEnum):
    """Группа безопасности инструментов, к которой отнесён пользователь.

    Определяет базовый уровень доступа пользователя к инструментам/настройкам IPS.
    Возвращается методом :meth:`~aioips.IPSClient.user_group` и присутствует как
    поле ``security_group`` в :class:`UserSecurityData`.

    Когда применять: чтобы понять привилегированность текущего пользователя
    (администратор против обычного/ограниченного) перед показом или вызовом
    операций редактирования настроек.

    Семантика членов:
        ADMINISTRATOR: ``administrator`` — администратор (полный доступ).
        NORMAL_USER: ``normalUser`` — обычный пользователь.
        RESTRICTED_USER: ``restrictedUser`` — пользователь с ограничениями.
    """

    ADMINISTRATOR = "administrator"
    NORMAL_USER = "normalUser"
    RESTRICTED_USER = "restrictedUser"


class ToolSecurityRights(StrEnum):
    """Уровень прав текущего пользователя на настройки инструментов.

    Описывает, какие настройки пользователь вправе менять (личные, публичные,
    переопределять личные и т. п.). Возвращается методом
    :meth:`~aioips.IPSClient.user_rights`.

    Когда применять: для гейтинга UI/операций редактирования настроек — например,
    разрешать изменение публичных настроек только при ``EDIT_PUBLIC_SETTINGS`` или
    ``ALL``. Значения не складываются в битовую маску; это единичный уровень.

    Семантика членов:
        NONE: ``none`` — прав на изменение настроек нет.
        EDIT_PUBLIC_SETTINGS: ``editPublicSettings`` — правка публичных настроек.
        EDIT_PERSONAL_SETTINGS: ``editPersonalSettings`` — правка личных настроек.
        OVERRIDE_PERSONAL_SETTINGS: ``overridePersonalSettings`` — переопределение
            личных настроек.
        ALL: ``all`` — полный набор прав на настройки.
    """

    NONE = "none"
    EDIT_PUBLIC_SETTINGS = "editPublicSettings"
    EDIT_PERSONAL_SETTINGS = "editPersonalSettings"
    OVERRIDE_PERSONAL_SETTINGS = "overridePersonalSettings"
    ALL = "all"
