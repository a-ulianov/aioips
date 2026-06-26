# Объекты (objects)

**Что за раздел.** Главный рабочий раздел: всё, что касается отдельных объектов IPS — чтение карточки
и атрибутов, поиск, разбор состава и правка через жизненный цикл. Именно эти 57 методов вы будете
вызывать чаще всего.

**Когда нужен.** Когда работаете с конкретным изделием/документом: достать объект по id или GUID,
прочитать или записать его атрибуты, найти объекты по условиям, разобрать состав, провести цикл
правки `check_out → … → check_in`. Помните о [двух id-пространствах](index.md#_4): большинство методов
принимает **id объекта** (`object_id`), а методы версий и `object_security` — **id версии**.

## Чтение объекта

| Метод | Назначение |
|---|---|
| `object_get(object_id, *, throw_not_found=False)` | Возвращает полное описание объекта (его базовую версию) по идентификатору объекта. |
| `object_get_by_guid(object_guid, *, throw_not_found=False)` | Возвращает полное описание объекта по GUID объекта (`objectGUID`). |
| `object_info(object_id)` | Возвращает краткие сведения об объекте по идентификатору объекта. |
| `object_info_by_guid(object_guid)` | Возвращает краткие сведения об объекте по GUID объекта (`objectGUID`). |
| `object_base_version(object_id, *, throw_not_found=False)` | Возвращает базовую (актуальную) версию объекта по идентификатору объекта. |
| `objects_all_versions(params)` | Возвращает все версии объекта (история) по его идентификатору. |
| `objects_collection(object_ids, *, throw_not_found=False)` | Возвращает описания нескольких объектов одним запросом по списку идентификаторов. |
| `object_by_version_rule(object_id)` | Возвращает версию объекта, выбранную текущим правилом версий, по id объекта. |
| `object_by_version_rule_by_guid(object_guid)` | Возвращает версию объекта по текущему правилу версий, по GUID объекта. |
| `object_by_versions_rule(object_id, rule_object_id, *, throw_not_found=None)` | Возвращает версию объекта, выбранную по заданному правилу выбора версий. |
| `object_hash_version(object_id)` | Возвращает хэш версии объекта (целочисленный отпечаток состояния). |
| `object_is_parent_type(object_id, object_type_guid)` | Проверяет, является ли тип с заданным GUID родительским для типа объекта. |
| `object_snapshot_info(object_id)` | Возвращает сводку по снимкам объекта: активный снимок и их коллекцию. |
| `object_snapshot_readonly_objects(object_id, snapshot_id)` | Возвращает идентификаторы объектов, доступных только для чтения в снимке. |
| `object_visibilities(object_id)` | Возвращает настройки видимости объекта (как он отображается в дереве/UI). |
| `object_check_visibility_available(object_id)` | Проверяет, доступны ли настройки видимости для объекта. |

## Атрибуты (чтение)

| Метод | Назначение |
|---|---|
| `object_attribute(object_id, attribute_id, *, get_actual_copy=False, extend_by_type=False, throw_not_found=False)` | Возвращает один атрибут объекта по идентификатору типа атрибута. |
| `object_attributes(object_id, *, extend_by_type=False)` | Возвращает все атрибуты объекта вместе с их значениями. |
| `object_attributes_values(object_id, *, extend_by_type=False, attribute_values_modes=None)` | Возвращает значения всех атрибутов объекта с расширенными метаданными. |
| `object_attribute_values(object_id, attribute_id, *, throw_not_found=False)` | Возвращает список «сырых» значений указанного атрибута объекта. |
| `object_attribute_values_by_guid(object_guid, attribute_id)` | Возвращает список «сырых» значений атрибута объекта, заданного по GUID. |
| `object_attribute_as_string(object_id, attribute_id, *, throw_not_found=False)` | Возвращает значение атрибута объекта в виде готовой строки. |
| `object_attributes_descriptions(object_id, *, throw_not_found=False)` | Возвращает текстовые описания значений всех атрибутов объекта. |
| `object_attribute_descriptions(object_id, attribute_id, *, throw_not_found=False)` | Возвращает текстовые описания значений одного атрибута объекта. |
| `object_attributes_init_values(object_id, *, attr_ids=None, extend_by_type=False)` | Возвращает начальные (инициализирующие) значения атрибутов объекта. |
| `object_calculated_attribute_values(object_id, attribute_values, *, modes=None)` | Вычисляет значения формульных (computed) атрибутов объекта на лету. |

## Поиск и состав

| Метод | Назначение |
|---|---|
| `objects_select(object_type_id, *, conditions=None, attribute_ids=None, record_count=None, local_types_mode=False, trash_mode=False)` | Ищет объекты заданного типа по условиям на значения их атрибутов. |
| `objects_select_request(request, *, object_type_id=None)` | Выборка системных атрибутов по списку id объектов (legacy-контроллер `Objects`; ключи — имена атрибутов). |
| `objects_select_by_id(request, *, object_type_id=None)` | То же с ключами-id атрибутов (⚠️ серверный 500 на обследованном билде — см. docstring). |
| `object_composition(project_version_id, *, context_rule=None)` | Возвращает состав объекта по версии проекта с учётом правила контекста. |
| `object_composition_with_params(object_id, *, relation_type_id=0, part_type_ids=None)` | Возвращает состав объекта — его дочерние объекты по связи заданного типа. |

## Запись и жизненный цикл

Правка возможна только в верном режиме. Типичный цикл: `object_check_out` → правка атрибутов →
`object_check_in` (или `object_cancel_changes`). Создание объекта завершается
`object_commit_creation`. Подробнее — в [Жизненном цикле](../concepts/lifecycle.md).

### Цикл правки (checkout / checkin)

| Метод | Назначение |
|---|---|
| `object_check_out(object_id, *, log_history=True)` | Извлекает объект на редактирование и возвращает id его рабочей копии. |
| `object_check_out_with_check_modify(object_id, *, log_history=True)` | Извлекает объект на редактирование с предварительной проверкой модифицируемости. |
| `object_check_in(object_id, *, log_history=True)` | Фиксирует изменения рабочей копии объекта и снимает блокировку редактирования. |
| `object_check_in_command(object_id, *, preserve_working_copies=None, log_history=True)` | Фиксирует изменения объекта командой check-in (МУТИРУЮЩАЯ операция). |
| `object_save_changes(object_id, *, log_history=True)` | Сохраняет изменения извлечённого объекта, НЕ снимая блокировку редактирования. |
| `object_cancel_changes(object_ids, *, confirm=False, admin_mode=None, log_history=True, ignore_exceptions=None)` | Отменяет несохранённые правки объектов. `confirm=True`. |
| `object_edit(object_id, *, log_history=True)` | Переводит объект в режим редактирования (МУТИРУЮЩАЯ операция, меняет состояние). |
| `object_checkout_date(object_id)` | Возвращает дату извлечения объекта на редактирование (checkout). |
| `object_check_relations_edit(object_id)` | Проверяет на сервере допустимость правки связей объекта. |
| `object_check_edit(object_id)` | Проверяет допустимость правки АТРИБУТОВ объекта перед checkout (запрет → исключение). |
| `object_load_descriptions(version_ids, *, throw_exception=False)` | Загружает краткие описания версий по списку их id (только чтение). |
| `object_check_out_versions(version_ids)` | Пакетно извлекает версии на редактирование (обратимо через rollback). |
| `object_rollback_check_out(checkout_result)` | Откатывает пакетный checkout, возвращая результат `object_check_out_versions`. |

### Создание объектов

| Метод | Назначение |
|---|---|
| `object_create(object_type, *, attributes=None, log_history=True)` | Создаёт новый объект указанного типа в режиме создания (черновик). |
| `object_create_by_prototype(prototype, *, log_history=True)` | Создаёт объект по прототипу (объекту-образцу) и возвращает черновик с потомками. |
| `object_create_object_version(object_id, *, log_history=True)` | Создаёт новую версию объекта на основе текущей (МУТИРУЮЩАЯ операция). |
| `object_commit_creation(object_id, *, delete_on_exception=True, auto_checkout=False, related_object_ids=None, log_history=True)` | Фиксирует создание черновика объекта и возвращает его постоянный идентификатор. |
| `object_add_objects_by_template(object_id, body, *, log_history=True)` | Добавляет объекты в состав объекта по шаблону-таблице (МУТИРУЮЩАЯ операция). |

### Запись атрибутов

| Метод | Назначение |
|---|---|
| `object_set_attributes(object_id, attributes, *, log_history=True)` | Записывает набор атрибутов объекта (в формате DTO атрибутов). |
| `object_set_attribute_values(object_id, attribute_values, *, delete_not_existing=False, dont_delete_blobs=False, return_delta=False, log_history=True)` | Записывает значения нескольких атрибутов объекта одним запросом. |
| `object_set_attribute_values_ex(object_id, body, *, log_history=True)` | Записывает значения атрибутов в расширенном режиме (с режимами извлечения). |
| `object_add_temporary_attribute(object_id, attribute_id, *, fail_if_exists=False, values=None)` | Добавляет объекту временный атрибут заданного типа. |
| `object_cleanup_attribute(object_id, attribute_id, *, confirm=False, log_history=True)` | Очищает значения атрибута объекта. `confirm=True`. |
| `object_delete_attribute(object_id, attribute_id, *, confirm=False, log_history=True)` | Удаляет атрибут объекта. `confirm=True`. |

### Состав и связи объекта (запись)

| Метод | Назначение |
|---|---|
| `object_include_in_composition(project_version_id, part_ids, *, log_history=True)` | Включает версии-потомки в состав версии-проекта (МУТИРУЮЩАЯ операция). |
| `object_exclude_from_composition(relation_ids, *, confirm=False, delete_relation_mode=None, log_history=True, ignore_exceptions=None)` | Исключает объекты из состава по id связей. `confirm=True`. |
| `object_connect_to_object(object_id, *, to_object_id=None, log_history=True)` | Присоединяет один объект к другому (МУТИРУЮЩАЯ операция). |

### Жизненный цикл и базовая версия

| Метод | Назначение |
|---|---|
| `object_can_set_next_lc_step(object_id, *, next_step_id=None)` | Проверяет, можно ли перевести объект на следующий шаг ЖЦ (ПРОВЕРКА, без мутации). |
| `object_validate_set_next_lc_step(object_id, *, next_step_id=None)` | Проверяет допустимость перевода объекта на следующий шаг ЖЦ (МУТИРУЮЩАЯ операция). |
| `object_make_base_version(object_id)` | Делает указанную версию объекта базовой (МУТИРУЮЩАЯ операция). |
| `object_make_base_versions(object_ids, *, log_history=True, ignore_exceptions=None)` | Делает указанные версии объектов базовыми (МУТИРУЮЩАЯ, пакетная операция). |

### Видимость и серверные операции

Настройки видимости управляют тем, какие узлы состава показаны/скрыты в дереве UI; запись
обратима (запишите назад прочитанный список). Печать и сохранение на диск/в архивную копию —
серверные операции без мутации данных самого объекта.

| Метод | Назначение |
|---|---|
| `object_check_access_rights_for_visibility(version_ids)` | Проверяет права на правку настроек видимости версий (только чтение). |
| `object_update_visibility_settings(object_id, settings)` | Сохраняет настройки видимости объекта (МУТИРУЮЩАЯ, обратима). |
| `object_print(object_id)` | Инициирует серверную печать объекта по его шаблону печати. |
| `object_save_to_disk(object_id)` | Сохраняет файлы объекта на диск средствами сервера. |
| `object_save_to_arc_copy(object_id, *, log_history=True)` | Сохраняет объект в архивную копию средствами сервера. |

### Удаление

| Метод | Назначение |
|---|---|
| `object_delete(object_id, *, confirm=False, delete_mode=0, log_history=True)` | Удаляет объект. `confirm=True`. |
