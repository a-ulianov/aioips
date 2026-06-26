"""Схема помощника идентификаторов текущего пользователя IPS.

Описывает тело ``IDHelperDTO`` — справочник системных идентификаторов
(типов объектов, системных атрибутов, групп и ролей), вычисленных для текущей
сессии. Помогает не «хардкодить» магические id системных сущностей IPS в
клиентском коде, а получать их с сервера.

References:
    ``GET /core/api/currentUsers/GetIdHelper`` — ``IDHelperDTO``.
    Домен: [[auth]], [[ips-object-model]].
"""

from pydantic import Field

from ..base import IPSModel


class IdHelper(IPSModel):
    """Справочник системных идентификаторов IPS для текущей сессии.

    Результат :meth:`id_helper`
    (``GET /core/api/currentUsers/GetIdHelper``). Сводит в одном объекте
    идентификаторы системных атрибутов (``nameID``, ``designationID`` и др.),
    типов объектов (``usersTypeID``, ``groupsTypeID``, ``rolesTypeID`` и др.),
    предопределённых групп/ролей (``allUsersGroupID``, ``adminRoleID`` и др.) и
    служебных констант, вычисленных сервером под текущего пользователя.

    Когда применять: чтобы не зашивать «магические» id системных сущностей в
    клиентском коде/MCP-инструментах, а получать их из API. Например, ``nameID``
    и ``designationID`` — id системных атрибутов «Наименование» и «Обозначение»,
    пригодные при чтении/записи атрибутов объектов; ``usersTypeID`` —
    идентификатор типа «Пользователи» для выборок.

    Важно (различие версия/объект, см. [[ips-object-model]]): значения — это
    системные идентификаторы соответствующих сущностей; интерпретировать их как
    ``objectID`` либо id версии нужно по контексту конкретной сущности.

    JSON приходит с акронимом в верхнем регистре (``adminRoleID``, ``nameID``):
    для этих полей задан явный ``alias``, так как автогенератор camelCase дал бы
    ``adminRoleId``/``nameId``. Поля без суффикса ``ID`` (например
    ``compositionVersionBackup``) отображаются обычным camelCase.

    Все поля необязательны (сервер может вернуть не весь набор) и по умолчанию
    ``None``.

    Attributes:
        modify_content_date_id: Id системного атрибута даты изменения состава.
        sort_index_id: Id системного атрибута индекса сортировки.
        plugin_type_id: Id типа объектов «Плагин».
        admin_role_id: Id предопределённой роли администратора.
        internal_service_role_id: Id внутренней служебной роли.
        owner_group_id: Id группы-владельца.
        object_creator_group_id: Id группы создателей объектов.
        relation_creator_group_id: Id группы создателей связей.
        all_users_group_id: Id группы «Все пользователи».
        group_owner_group_id: Id группы-владельца групп.
        deleted_id: Id системного признака «удалён».
        sysdba_id: Id пользователя your-login.
        system_id: Id системного пользователя.
        default_language_id: Идентификатор языка по умолчанию (строка).
        users_type_id: Id типа объектов «Пользователи».
        groups_type_id: Id типа объектов «Группы».
        storage_type_id: Id типа объектов «Хранилище».
        login_name_id: Id системного атрибута «Имя для входа».
        password_id: Id системного атрибута «Пароль».
        external_user_id: Id системного атрибута «Внешний пользователь».
        user_name_id: Id системного атрибута «Имя пользователя».
        roles_type_id: Id типа объектов «Роли».
        measure_type_id: Id типа объектов «Единицы измерения».
        name_id: Id системного атрибута «Наименование».
        short_name_id: Id системного атрибута «Краткое наименование».
        designation_id: Id системного атрибута «Обозначение».
        simple_relation_type_id: Id типа простой связи.
        physic_value_type_id: Id типа «Физическая величина».
        config_data_type_id: Id типа «Данные конфигурации».
        workspace_type_id: Id типа «Рабочая область».
        personal_level_id: Id персонального уровня.
        file_attribute_id: Id системного файлового атрибута.
        config_file_attribute_id: Id файлового атрибута конфигурации.
        created_level_id: Id уровня «Создан».
        sp_relation_type_id: Id типа связи спецификации.
        doc_relation_type_id: Id типа связи документа.
        folder_key_id: Id ключа папки.
        ranks_type_id: Id типа объектов «Ранги».
        projects_type_id: Id типа объектов «Проекты».
        composition_version_id: Id версии состава.
        composition_version_backup: Резервный id версии состава.
        settings_attribute_id: Id системного атрибута настроек.
        substitutes_group_no_id: Id номера группы замещений.
        substitute_in_group: Признак/id замещения в группе.
        sorted_relation_type_id: Id типа сортированной связи.
        objtype_version_rule: Правило версий типа объекта (общее значение).
        objtype_version_rule_common: Правило версий типа объекта (общее).
        objtype_version_rule_user: Правило версий типа объекта (пользователь).
        objtype_version_rule_system: Правило версий типа объекта (система).
        security_level_id: Id уровня секретности.
        annulment_level_id: Id уровня аннулирования.
        keeping_level_id: Id уровня хранения.
        litera_id: Id системного атрибута «Литера».
        attribute_version_in_relation: Id атрибута версии в связи.
        internal_reg_number: Id внутреннего регистрационного номера.
        active_snapshot_id: Id активного снимка (snapshot).
        attribute_redlining: Id атрибута «Редлайнинг».
        attribute_need_for_publication: Id атрибута «Требуется публикация».
        attribute_option_publication: Id атрибута «Опция публикации».
        objtype_incomplete_object: Id типа «Незавершённый объект».
        attribute_access_condition: Id атрибута «Условие доступа».
        attribute_last_editor_id: Id атрибута «Последний редактор».
        block_error_report_sending_id: Id признака блокировки отправки отчётов
            об ошибках.
    """

    modify_content_date_id: int | None = Field(
        default=None, alias="modifyContentDateID", description="Id атрибута даты изменения состава"
    )
    sort_index_id: int | None = Field(
        default=None, alias="sortIndexID", description="Id атрибута индекса сортировки"
    )
    plugin_type_id: int | None = Field(
        default=None, alias="pluginTypeID", description="Id типа объектов «Плагин»"
    )
    admin_role_id: int | None = Field(
        default=None, alias="adminRoleID", description="Id роли администратора"
    )
    internal_service_role_id: int | None = Field(
        default=None, alias="internalServiceRoleID", description="Id внутренней служебной роли"
    )
    owner_group_id: int | None = Field(
        default=None, alias="ownerGroupID", description="Id группы-владельца"
    )
    object_creator_group_id: int | None = Field(
        default=None, alias="objectCreatorGroupID", description="Id группы создателей объектов"
    )
    relation_creator_group_id: int | None = Field(
        default=None, alias="relationCreatorGroupID", description="Id группы создателей связей"
    )
    all_users_group_id: int | None = Field(
        default=None, alias="allUsersGroupID", description="Id группы «Все пользователи»"
    )
    group_owner_group_id: int | None = Field(
        default=None, alias="groupOwnerGroupID", description="Id группы-владельца групп"
    )
    deleted_id: int | None = Field(
        default=None, alias="deletedID", description="Id признака «удалён»"
    )
    sysdba_id: int | None = Field(
        default=None, alias="sysdbaID", description="Id пользователя your-login"
    )
    system_id: int | None = Field(
        default=None, alias="systemID", description="Id системного пользователя"
    )
    default_language_id: str | None = Field(
        default=None, alias="defaultLanguageID", description="Идентификатор языка по умолчанию"
    )
    users_type_id: int | None = Field(
        default=None, alias="usersTypeID", description="Id типа объектов «Пользователи»"
    )
    groups_type_id: int | None = Field(
        default=None, alias="groupsTypeID", description="Id типа объектов «Группы»"
    )
    storage_type_id: int | None = Field(
        default=None, alias="storageTypeID", description="Id типа объектов «Хранилище»"
    )
    login_name_id: int | None = Field(
        default=None, alias="loginNameID", description="Id атрибута «Имя для входа»"
    )
    password_id: int | None = Field(
        default=None, alias="passwordID", description="Id атрибута «Пароль»"
    )
    external_user_id: int | None = Field(
        default=None, alias="externalUserID", description="Id атрибута «Внешний пользователь»"
    )
    user_name_id: int | None = Field(
        default=None, alias="userNameID", description="Id атрибута «Имя пользователя»"
    )
    roles_type_id: int | None = Field(
        default=None, alias="rolesTypeID", description="Id типа объектов «Роли»"
    )
    measure_type_id: int | None = Field(
        default=None, alias="measureTypeID", description="Id типа объектов «Единицы измерения»"
    )
    name_id: int | None = Field(
        default=None, alias="nameID", description="Id атрибута «Наименование»"
    )
    short_name_id: int | None = Field(
        default=None, alias="shortNameID", description="Id атрибута «Краткое наименование»"
    )
    designation_id: int | None = Field(
        default=None, alias="designationID", description="Id атрибута «Обозначение»"
    )
    simple_relation_type_id: int | None = Field(
        default=None, alias="simpleRelationTypeID", description="Id типа простой связи"
    )
    physic_value_type_id: int | None = Field(
        default=None, alias="physicValueTypeID", description="Id типа «Физическая величина»"
    )
    config_data_type_id: int | None = Field(
        default=None, alias="configDataTypeID", description="Id типа «Данные конфигурации»"
    )
    workspace_type_id: int | None = Field(
        default=None, alias="workspaceTypeID", description="Id типа «Рабочая область»"
    )
    personal_level_id: int | None = Field(
        default=None, alias="personalLevelID", description="Id персонального уровня"
    )
    file_attribute_id: int | None = Field(
        default=None, alias="fileAttributeID", description="Id системного файлового атрибута"
    )
    config_file_attribute_id: int | None = Field(
        default=None,
        alias="configFileAttributeID",
        description="Id файлового атрибута конфигурации",
    )
    created_level_id: int | None = Field(
        default=None, alias="createdLevelID", description="Id уровня «Создан»"
    )
    sp_relation_type_id: int | None = Field(
        default=None, alias="spRelationTypeID", description="Id типа связи спецификации"
    )
    doc_relation_type_id: int | None = Field(
        default=None, alias="docRelationTypeID", description="Id типа связи документа"
    )
    folder_key_id: int | None = Field(
        default=None, alias="folderKeyID", description="Id ключа папки"
    )
    ranks_type_id: int | None = Field(
        default=None, alias="ranksTypeID", description="Id типа объектов «Ранги»"
    )
    projects_type_id: int | None = Field(
        default=None, alias="projectsTypeID", description="Id типа объектов «Проекты»"
    )
    composition_version_id: int | None = Field(
        default=None, alias="compositionVersionID", description="Id версии состава"
    )
    composition_version_backup: int | None = Field(
        default=None,
        alias="compositionVersionBackup",
        description="Резервный id версии состава",
    )
    settings_attribute_id: int | None = Field(
        default=None, alias="settingsAttributeID", description="Id атрибута настроек"
    )
    substitutes_group_no_id: int | None = Field(
        default=None, alias="substitutesGroupNoID", description="Id номера группы замещений"
    )
    substitute_in_group: int | None = Field(
        default=None, alias="substituteInGroup", description="Признак/id замещения в группе"
    )
    sorted_relation_type_id: int | None = Field(
        default=None, alias="sortedRelationTypeID", description="Id типа сортированной связи"
    )
    objtype_version_rule: int | None = Field(
        default=None, alias="objtypeVersionRule", description="Правило версий типа объекта"
    )
    objtype_version_rule_common: int | None = Field(
        default=None,
        alias="objtypeVersionRuleCommon",
        description="Правило версий типа объекта (общее)",
    )
    objtype_version_rule_user: int | None = Field(
        default=None,
        alias="objtypeVersionRuleUser",
        description="Правило версий типа объекта (пользователь)",
    )
    objtype_version_rule_system: int | None = Field(
        default=None,
        alias="objtypeVersionRuleSystem",
        description="Правило версий типа объекта (система)",
    )
    security_level_id: int | None = Field(
        default=None, alias="securityLevelID", description="Id уровня секретности"
    )
    annulment_level_id: int | None = Field(
        default=None, alias="annulmentLevelID", description="Id уровня аннулирования"
    )
    keeping_level_id: int | None = Field(
        default=None, alias="keepingLevelID", description="Id уровня хранения"
    )
    litera_id: int | None = Field(
        default=None, alias="literaID", description="Id атрибута «Литера»"
    )
    attribute_version_in_relation: int | None = Field(
        default=None,
        alias="attributeVersionInRelation",
        description="Id атрибута версии в связи",
    )
    internal_reg_number: int | None = Field(
        default=None,
        alias="internalRegNumber",
        description="Id внутреннего регистрационного номера",
    )
    active_snapshot_id: int | None = Field(
        default=None, alias="activeSnapshotID", description="Id активного снимка (snapshot)"
    )
    attribute_redlining: int | None = Field(
        default=None, alias="attributeRedlining", description="Id атрибута «Редлайнинг»"
    )
    attribute_need_for_publication: int | None = Field(
        default=None,
        alias="attributeNeedForPublication",
        description="Id атрибута «Требуется публикация»",
    )
    attribute_option_publication: int | None = Field(
        default=None,
        alias="attributeOptionPublication",
        description="Id атрибута «Опция публикации»",
    )
    objtype_incomplete_object: int | None = Field(
        default=None,
        alias="objtypeIncompleteObject",
        description="Id типа «Незавершённый объект»",
    )
    attribute_access_condition: int | None = Field(
        default=None,
        alias="attributeAccessCondition",
        description="Id атрибута «Условие доступа»",
    )
    attribute_last_editor_id: int | None = Field(
        default=None,
        alias="attributeLastEditorID",
        description="Id атрибута «Последний редактор»",
    )
    block_error_report_sending_id: int | None = Field(
        default=None,
        alias="blockErrorReportSendingID",
        description="Id признака блокировки отправки отчётов об ошибках",
    )
