# Прочие разделы

На этой странице собраны все остальные разделы клиента `aioips`. Каждый — короткое описание (что это
и когда нужно) и таблица методов. Разрушающие методы помечены `confirm=True`. Содержание:

- Пользователь и доступ: [auth](#auth), [users](#users), [settings](#settings), [sso](#sso), [licenses](#licenses)
- Типы объектов: [object_types](#object_types)
- Интерфейс и данные: [forms](#forms), [documents](#documents), [document_editor](#document_editor), [table_report](#table_report), [visibilities](#visibilities), [measure_units](#measure_units)
- Календари и проекты: [calendars](#calendars), [improjects](#improjects)
- Справочники и 3D: [imbase](#imbase), [imviewer](#imviewer)
- Совместная работа: [discussions](#discussions), [workflow](#workflow), [mail_agent](#mail_agent)
- Подписи и снимки: [crypto_signing](#crypto_signing), [signs](#signs), [graph_signs](#graph_signs), [snapshots](#snapshots)
- Классификация и поиск: [selection_classificators](#selection_classificators), [search_schemes](#search_schemes)
- Системное: [config](#config), [attribute_history](#attribute_history), [briefcase](#briefcase), [bridge](#bridge)

---

## object_types

**Что это.** Определения **типов** объектов и перечни их экземпляров. В отличие от раздела
[metadata](metadata.md), который отдаёт справочные сведения о метамодели, здесь — полные определения
типа (`ObjectTypeDto`) и списки реальных объектов данного типа. Нужен, когда строите дерево типов в
UI или перечисляете все объекты определённого типа.

| Метод | Назначение |
|---|---|
| `object_type_definition(object_type_id)` | Возвращает определение типа объекта (`ObjectTypeDto`) по идентификатору. |
| `object_type_definition_by_guid(object_type_guid)` | Возвращает определение типа объекта (`ObjectTypeDto`) по его GUID. |
| `object_type_definition_by_name(object_type_name)` | Возвращает определение типа объекта (`ObjectTypeDto`) по его имени. |
| `object_type_quick_info(object_type_id)` | Возвращает краткую информацию о ТИПЕ объекта по идентификатору. |
| `object_type_quick_info_by_guid(object_type_guid)` | Возвращает краткую информацию о ТИПЕ объекта по его GUID. |
| `object_type_all_child_guids(object_type_guid)` | Возвращает GUID всех дочерних ТИПОВ заданного типа объекта. |
| `object_type_objects(object_type_id)` | Возвращает краткие сведения обо всех РЕАЛЬНЫХ объектах (экземплярах) типа. |
| `object_type_object_ids(object_type_id)` | Возвращает идентификаторы всех РЕАЛЬНЫХ объектов (экземпляров) заданного типа. |
| `object_type_objects_info(object_type_id)` | Возвращает сводку (счётчики) по РЕАЛЬНЫМ объектам (экземплярам) заданного типа. |
| `object_type_icons(object_type_ids)` | Возвращает карту значков `{id типа: иконка}` для списка типов (чтение через POST). |
| `object_types_tree(object_type_ids)` | Возвращает дерево типов для списка id (пустой список — все типы; чтение через POST). |
| `object_type_composition(object_type_id, params)` | Состав ОБЪЕКТОВ типа (объекты + под-состав); `params.attribute_ids` обязателен (пустой → 500). |

## auth

**Что это.** Опции входа пользователя. Нужен на этапе авторизации, чтобы узнать доступные роли и
уровни доступа. Получение и обновление JWT-токена выполняет ядро клиента автоматически (см.
[Аутентификация](../getting-started/authentication.md)).

| Метод | Назначение |
|---|---|
| `login_options(login_name)` | Возвращает роли и уровни доступа, доступные пользователю при входе. |

## users

**Что это.** Сведения о текущем авторизованном пользователе и системные идентификаторы сессии. Нужен,
чтобы узнать, кто вошёл, и получить набор системных id для последующих вызовов.

| Метод | Назначение |
|---|---|
| `user_info()` | Возвращает сведения о пользователе текущей авторизованной сессии. |
| `id_helper()` | Возвращает справочник системных идентификаторов IPS для текущей сессии. |

## settings

**Что это.** Права и группы текущего пользователя и настройки печати. Нужен, чтобы проверить
уровень прав на изменение настроек и получить настройки внедрения данных при печати типа объекта.

| Метод | Назначение |
|---|---|
| `user_rights()` | Возвращает уровень прав ТЕКУЩЕГО пользователя на изменение настроек. |
| `user_group()` | Возвращает группу безопасности инструментов ТЕКУЩЕГО пользователя. |
| `security_data()` | Возвращает данные безопасности пользователей: связки `userId` ↔ группа. |
| `view_print_settings(object_type_id)` | Возвращает настройки внедрения данных при просмотре/печати для типа объекта. |
| `set_view_print_settings(object_type_id, settings, *, confirm=False)` | Записывает настройки просмотра/печати типа (МУТИРУЮЩАЯ, `confirm`; парная к `view_print_settings`). |

## sso

**Что это.** Опции аутентификации через SPNEGO/Kerberos (single sign-on). Нужен в доменной среде,
когда вход выполняется без явного ввода пароля.

| Метод | Назначение |
|---|---|
| `kerberos_auth_options()` | Возвращает опции аутентификации текущего пользователя по SPNEGO/Kerberos. |

## licenses

**Что это.** Лицензирование клиента. Нужен, чтобы получить с сервера идентификатор клиента для
привязки лицензии.

| Метод | Назначение |
|---|---|
| `generate_client_id()` | Генерирует на сервере новый идентификатор клиента для лицензирования IPS. |

## forms

**Что это.** Формы и виджеты IPS: получение форм по версии объекта, состав пользователей/групп
формы, палитры цветов и связанные типы. Нужен при построении пользовательского интерфейса на основе
форм IPS.

| Метод | Назначение |
|---|---|
| `form(version_id)` | Возвращает форму (корневой виджет) по идентификатору версии. |
| `forms_for(version_id, *, is_create_object=None, is_relation=None)` | Возвращает список форм, применимых к указанной версии объекта. |
| `image_for_widget(version_id)` | Возвращает изображение виджета по идентификатору версии (строкой). |
| `default_columns_for_widget()` | Возвращает набор колонок по умолчанию для табличного виджета. |
| `form_related_object_type_guids(form_id)` | Возвращает GUID типов объектов, связанных с формой. |
| `form_related_relation_type_guids(form_id)` | Возвращает GUID типов связей, связанных с формой. |
| `find_user_groups_and_users(version_id)` | Возвращает группы и пользователей состава формы одним вызовом. |
| `find_user_groups_and_users_in_composition(version_id)` | Возвращает группы и пользователей состава формы одним вызовом. |
| `find_user_groups_in_composition(version_id)` | Возвращает группы пользователей, найденные в составе формы данной версии. |
| `rank_find_inner_users(version_id)` | Возвращает пользователей из состава формы, включая входящих в группы. |
| `user_group_find_roots()` | Возвращает корневые (верхнеуровневые) группы пользователей. |
| `subject_area_find_collection()` | Возвращает коллекцию предметных областей форм. |
| `widget_colors()` | Возвращает пользовательскую палитру цветов для оформления виджетов форм. |
| `default_widget_colors()` | Возвращает палитру цветов виджетов по умолчанию. |
| `system_colors()` | Возвращает системную палитру цветов для оформления виджетов форм. |
| `find_applicability(options)` | Поиск применимых объектов по параметрам формы (`FindCollectionOptions` → `FormObjectDto`). |
| `find_collection(options)` | Поиск коллекции объектов по параметрам формы (фильтр/пагинация). |
| `find_composition(options)` | Поиск состава объекта по параметрам формы. |
| `find_objects_list(request)` | Выборка объектов по списку id версий и колонкам (`VersionIdAndColumns4Request`). |
| `find_users(request)` | Поиск пользователей по группам/рангам (`Ids4FindUsersRequest` → `User`). |
| `rank_find_collection(ids)` | Поиск рангов (утверждающих) по списку id. |
| `user_find_collection(ids)` | Поиск пользователей по списку id. |
| `user_group_find_collection(ids)` | Поиск групп пользователей по списку id. |

## documents

**Что это.** Прототипы (шаблоны) документов и настройки документов для типа объекта.

| Метод | Назначение |
|---|---|
| `document_prototypes_common()` | Возвращает общие (доступные всем типам) прототипы документов. |
| `document_prototypes_private()` | Возвращает приватные (привязанные к типам) прототипы документов. |
| `document_settings(object_type_id)` | Возвращает настройки документов для заданного типа объекта. |
| `save_document_settings(object_type_id, settings, *, confirm=False)` | Записывает настройки документов типа (МУТИРУЮЩАЯ, `confirm`; парная к `document_settings`). |

## document_editor

**Что это.** Редактор документов: списки шрифтов, содержимое буфера, имена свойств элементов.

| Метод | Назначение |
|---|---|
| `doc_editor_font_list()` | Возвращает признак готовности (наличия) списка шрифтов редактора документов. |
| `doc_editor_all_fonts_name(*, update=None)` | Возвращает список имён всех шрифтов, доступных редактору документов. |
| `doc_editor_buffer()` | Возвращает структуру документа из буфера редактора как дерево узлов. |
| `doc_editor_prop_name(*, props=None)` | Возвращает наименование назначаемого свойства элемента редактора документов. |
| `doc_editor_non_assignable_prop_name(*, props=None)` | Возвращает наименование неназначаемого свойства элемента редактора документов. |

## table_report

**Что это.** Табличные отчёты, настроенные для объекта, и подсчёт итогов.

| Метод | Назначение |
|---|---|
| `report_content(object_id, params)` | Метод генерации содержимого табличного отчёта объекта IPS |
| `table_report(object_id)` | Метод получения шаблона табличного отчёта объекта |
| `table_report_math_total(math_total)` | Метод расчёта итога табличного отчёта по математическому выражению |

## calendars

**Что это.** Производственные календари (рабочее время, выходные, исключения) — системные,
подразделений и пользовательские. Используются планированием задач/проектов (improjects).

| Метод | Назначение |
|---|---|
| `calendars()` | Список всех календарей системы (`[{calendarId, name}]`). |
| `calendar_settings(calendar_id)` | Полное определение календаря по id (`Calendar` / `CalendarContract`). |
| `user_calendar_settings(user_id)` | Личный календарь пользователя. |
| `unit_calendar_settings(unit_id)` | Календарь подразделения. |
| `unit_calendar_for_user(user_id)` | Календарь подразделения, действующий для пользователя. |
| `base_calendar_filter()` / `user_calendar_filter()` | Фильтры календарей (`FilterContract`). |
| `update_calendar_settings(calendar, *, confirm=False)` | Записывает настройки календаря (МУТИРУЮЩАЯ, `confirm`). |
| `update_user_calendar_settings(calendar, *, confirm=False)` | Записывает пользовательский календарь (МУТИРУЮЩАЯ, `confirm`). |
| `set_base_calendar(object_id, base_calendar_id, *, confirm=False)` | Назначает объекту базовый календарь (МУТИРУЮЩАЯ, `confirm`). |

## imbase

**Что это.** Справочная система IMBASE (каталоги, таблицы, индексы, избранное). Раздел обширный —
полный список методов в [README репозитория](https://github.com/a-ulianov/aioips#readme); ниже —
безопасные операции (конвертеры, резолверы имён и обратимая работа с избранным).

| Метод | Назначение |
|---|---|
| `imbase_rtf_to_plain_text(rtf)` | Конвертирует RTF-значение атрибута имбазы в простой текст. |
| `imbase_rtf_to_svg(rtf, width)` | Конвертирует RTF в SVG (data-URL, base64) заданной ширины. |
| `imbase_object_references_names(references)` | Разрешает имена объектов по ссылкам (`dict {ссылка: имя}`). |
| `imbase_object_by_id_references_names(references)` | То же по ссылкам-вариантам с id. |
| `imbase_record_references_names(references)` | Разрешает имена записей имбазы по ссылкам. |
| `imbase_add_to_favorite_folder(favorite_folder_id, object_id)` | Добавляет объект в папку избранного (ОБРАТИМО; сервер может вернуть `null`). |
| `imbase_remove_from_favorites(parent_id, object_id)` | Убирает объект из избранного (обратная к add). |
| `imbase_table_mix_data(object_id)` | Возвращает смешанные табличные данные объекта имбазы (`TableMixDataDto`). |
| `imbase_find_in_tables(params)` | Поиск записей в таблицах имбазы по условиям (`ImBaseTableSearchParams`). |
| `imbase_find_by_index(params)` | Индексный/полнотекстовый поиск по атрибуту имбазы (`ImBaseIndexSearchParams`). |
| `imbase_attribute_existing_values(attribute_guid, params)` | Существующие значения атрибута для подсказок (по GUID атрибута). |

## archives

**Что это.** Архивы документов IPS (объекты-архивы, на которые ссылается атрибут-ссылка «Архив»).
Пока — проверка применимости настроек типов документов.

| Метод | Назначение |
|---|---|
| `archive_can_apply_settings(archive_id, body)` | Проверяет применимость настроек типов документов к архиву (чтение через POST → bool). |

## graph_signs

**Что это.** Настройки графических подписей (штампов ЭЦП) для архивов, уровней/шагов ЖЦ и рангов.
Чтение + парная запись (config, не права доступа). Пути с префиксом `/api` (не `/core/api`).

| Метод | Назначение |
|---|---|
| `archive_sign_settings(archive_id)` | Настройки подписей архива (чтение). |
| `lifecycle_level_sign_settings(lifecycle_level_id)` | Настройки подписей уровня ЖЦ (чтение). |
| `lifecycle_step_sign_settings(lifecycle_step_id)` | Настройки подписей шага ЖЦ (чтение). |
| `object_type_lifecycle_step_sign_settings(object_type_id, lifecycle_level_id)` | Настройки подписей шага ЖЦ для типа (чтение). |
| `rank_graph_signs(rank_id)` / `rank_graph_sign_object_types()` | Графические подписи ранга / доступные типы (чтение). |
| `update_archive_sign_settings(archive_id, groups, *, confirm=False)` | Запись настроек подписей архива (МУТИРУЮЩАЯ, `confirm`). |
| `update_lifecycle_level_sign_settings(lifecycle_level_id, groups, *, confirm=False)` | Запись настроек подписей уровня ЖЦ. |
| `update_lifecycle_step_sign_settings(lifecycle_step_id, groups, *, confirm=False)` | Запись настроек подписей шага ЖЦ. |
| `update_object_type_lifecycle_step_sign_settings(object_type_id, lifecycle_level_id, groups, *, confirm=False)` | Запись настроек подписей шага ЖЦ для типа. |
| `save_rank_graph_signs(rank_id, signs, *, confirm=False)` | Запись графических подписей ранга. |
