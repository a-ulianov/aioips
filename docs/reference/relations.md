# Связи (relations, relation_queries, relation_types)

**Что за раздел.** Всё про **связи** между объектами — рёбра состава изделия «родитель → потомок».
Здесь три раздела клиента: [`relations`](#relations) (работа с конкретными связями и их атрибутами),
[`relation_queries`](#relation_queries) (готовые запросы состава и вхождений) и
[`relation_types`](#relation_types) (перечни связей по типу). Метаданные самих типов связей — в
разделе [metadata](metadata.md#_8).

**Когда нужен.** Когда разбираете или собираете структуру изделия: получить состав («из чего
состоит») или вхождения («куда входит»), создать/удалить связь, прочитать или записать атрибуты
связи. Важно про id: в связи `projID` — это **id ОБЪЕКТА-родителя**, а `partID` — **id ВЕРСИИ-потомка**
(см. [id-пространства](index.md#_4)). `RelationID` нестабилен — не кэшируйте его.

## relations

### Чтение связей

| Метод | Назначение |
|---|---|
| `relation_get(relation_id)` | Возвращает связь между объектами по её идентификатору. |
| `relation_get_by_guid(relation_guid)` | Возвращает связь между объектами по её GUID. |
| `relation_by_guid_and_project(relation_guid, project_id)` | Возвращает связь по её устойчивому `GUID` в контексте проекта-родителя. |
| `relation_by_project_and_part(project_id, part_id)` | Возвращает связь по паре «объект-родитель → версия-потомок». |
| `relations_by_project(project_id, relation_type_id)` | Возвращает связи объекта-родителя указанного типа. |

### Поиск и выборка

| Метод | Назначение |
|---|---|
| `relations_select(params)` | Произвольная выборка связей по типу, условиям и атрибутам (с пагинацией). |
| `relations_consist_from(params)` | Расширенный поиск состава объекта — связи к объектам, из которых он состоит. |
| `relations_enters_in(params)` | Расширенный поиск вхождений объекта — связи к объектам, в которые он входит. |
| `relations_enters_in_version(params)` | Расширенный поиск вхождений ВЕРСИИ объекта — связи к её родителям. |
| `relations_consist_from_request(request)` | Состав объекта (связи к потомкам) через legacy-контроллер `Relations` по фильтру-запросу. |
| `relations_enters_in_version_request(request)` | Вхождения версии объекта (связи к родителям) через legacy-контроллер `Relations`. |

### Атрибуты связи (чтение)

| Метод | Назначение |
|---|---|
| `relation_attribute(relation_id, attribute_id, *, extend_by_type=False, throw_not_found=False)` | Возвращает один атрибут СВЯЗИ по идентификатору типа атрибута. |
| `relation_attributes(relation_id, *, extend_by_type=False)` | Возвращает все атрибуты СВЯЗИ вместе с их значениями. |
| `relation_attributes_values(relation_id, *, extend_by_type=False)` | Возвращает значения всех атрибутов СВЯЗИ с расширенными метаданными. |
| `relation_attribute_values(relation_id, attribute_id, *, throw_not_found=False)` | Возвращает список «сырых» значений указанного атрибута СВЯЗИ. |
| `relation_attributes_descriptions(relation_id)` | Возвращает текстовые описания значений всех атрибутов СВЯЗИ. |
| `relation_attribute_descriptions(relation_id, attribute_id)` | Возвращает текстовые описания значений одного атрибута СВЯЗИ. |
| `relation_attributes_init_values(relation_id)` | Возвращает исходные (инициализационные) значения атрибутов СВЯЗИ. |

### Запись связей и атрибутов

| Метод | Назначение |
|---|---|
| `relation_create(relation, *, log_history=True)` | Создаёт связь «родитель → потомок» в составе изделия (МУТИРУЮЩАЯ операция). |
| `relation_create_collection(relations, *, log_history=True)` | Создаёт сразу несколько связей «родитель → потомок» одним запросом (МУТИРУЮЩАЯ). |
| `relation_set_attributes(relation_id, attributes, *, log_history=True)` | Записывает (заменяет) набор атрибутов СВЯЗИ переданным списком `Attribute`. |
| `relation_set_attribute_values(relation_id, attribute_values, *, delete_not_existing=False, dont_delete_blobs=False, return_delta=False, log_history=True, modes=None)` | Записывает значения атрибутов СВЯЗИ списком `AttributeValues`. |
| `relation_set_attribute_values_ex(relation_id, body, *, log_history=True)` | Расширенная запись значений атрибутов СВЯЗИ (с режимами извлечения); возвращает ошибки по атрибутам. |
| `relation_update_relations_attributes(body, *, log_history=True)` | Пакетно обновляет атрибуты сразу нескольких связей одним запросом. |
| `relation_add_temporary_attribute(relation_id, attribute_id, *, fail_if_exists=False, values=None)` | Добавляет к СВЯЗИ временный атрибут заданного типа и инициализирует значения. |
| `relation_delete(relation_id, *, confirm=False, delete_mode=None, log_history=True)` | Удаляет связь по её идентификатору. `confirm=True`. |
| `relation_delete_attribute(relation_id, attribute_id, *, confirm=False, log_history=True)` | Удаляет один атрибут СВЯЗИ по id связи и id атрибута. `confirm=True`. |

### Справочник типов связей

| Метод | Назначение |
|---|---|
| `relation_types()` | Возвращает список всех типов связей, определённых в IPS. |

## relation_queries

**Что за раздел.** Готовые высокоуровневые запросы состава и вхождений по id объекта — проще, чем
ручная выборка через `relations_select`.

| Метод | Назначение |
|---|---|
| `consist_from(object_id, *, recure=None, relation_type_id=None, object_type_id=None)` | Возвращает состав объекта — связи к объектам, из которых он состоит. |
| `enters_in_version(object_id, *, recure=None, relation_type_id=None)` | Возвращает вхождения объекта — связи к объектам, в состав которых он входит. |
| `classifier_objects(*, classifier_object_id=None)` | Возвращает идентификаторы объектов, отнесённых к узлу классификатора. |
| `relation_queries_relation_types()` | Возвращает справочник типов связей, определённых в IPS. |

## relation_types

**Что за раздел.** Перечни конкретных связей, сгруппированные по типу связи.

| Метод | Назначение |
|---|---|
| `relation_type_relations(relation_type_id)` | Возвращает все связи заданного типа в краткой форме. |
| `relation_type_relation_ids(relation_type_id)` | Возвращает идентификаторы всех связей заданного типа. |
