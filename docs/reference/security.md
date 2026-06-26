# Права доступа (security)

**Что за раздел.** Чтение **прав доступа** (кто что может) на различные сущности IPS: объекты, типы
объектов и связей, атрибуты, группы атрибутов, уровни и схемы жизненного цикла, шаги ЖЦ и систему в
целом. Все методы — только чтение прав; их назначение здесь не настраивается.

**Когда нужен.** Когда нужно понять, доступна ли пользователю операция, до её попытки: проверить
права на версию объекта, на тип, на атрибут на конкретном шаге ЖЦ. Обратите внимание:
`object_security` принимает **id ВЕРСИИ** объекта (`object_version_id`), а не id объекта (см.
[id-пространства](index.md#_4)). Методы с суффиксом `*_security()` без аргументов возвращают права на
коллекцию метаданного в целом.

## Права на объекты и их действия

| Метод | Назначение |
|---|---|
| `object_security(object_version_id)` | Возвращает права доступа на конкретную ВЕРСИЮ объекта (кто что может). |
| `actions_on_objects_security()` | Возвращает глобальные права на ДЕЙСТВИЯ над объектами (системный уровень). |
| `system_security()` | Возвращает права доступа на СИСТЕМУ в целом (общесистемная политика). |

## Права на типы объектов и связей

| Метод | Назначение |
|---|---|
| `object_type_security(object_type_id)` | Возвращает права доступа на ТИП объекта (кто что может с объектами типа). |
| `object_types_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ типов объектов (метаданное в целом). |
| `relation_type_security(relation_type_id)` | Возвращает права доступа на ТИП связи (кто что может с данным типом связи). |
| `relation_types_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ типов связей (метаданное в целом). |

## Права на атрибуты и группы

| Метод | Назначение |
|---|---|
| `attribute_security(attribute_id)` | Возвращает права доступа на АТРИБУТ (кто может читать/изменять атрибут). |
| `attributes_collection_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ атрибутов (метаданное в целом). |
| `attribute_group_security(attribute_group_id)` | Возвращает права доступа на ГРУППУ атрибутов (кто что может с группой). |
| `attribute_groups_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ групп атрибутов (метаданное в целом). |

## Права на жизненный цикл

| Метод | Назначение |
|---|---|
| `lifecycle_level_security(lifecycle_level_id)` | Возвращает права доступа на УРОВЕНЬ ЖЦ (кто что может на данном уровне ЖЦ). |
| `lifecycle_levels_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ уровней ЖЦ (метаданное в целом). |
| `lifecycle_scheme_security(lifecycle_scheme_id)` | Возвращает права доступа на СХЕМУ ЖЦ (кто что может с данной схемой ЖЦ). |
| `lifecycle_schemes_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ схем ЖЦ (метаданное в целом). |
| `object_type_lifecycle_step_security(object_type_id, lifecycle_scheme_step_id)` | Возвращает права доступа на ШАГ схемы ЖЦ конкретного типа объекта. |
| `object_type_lifecycle_step_attribute_security(object_type_id, lifecycle_scheme_step_id, attribute_id)` | Возвращает права на АТРИБУТ типа объекта на конкретном шаге схемы ЖЦ. |

## Права на прочие метаданные

| Метод | Назначение |
|---|---|
| `languages_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ языков (метаданное в целом). |
| `subject_areas_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ предметных областей (метаданное в целом). |

## Проверка доступа (checkAccess)

**Read-only.** Проверяют, есть ли у текущего пользователя доступ к конкретному ДЕЙСТВИЮ над целью защиты. Поле `action_type` в `SecurityCheckAccess` — это валидное действие из набора цели (`list` / `view` / `editProperties` / `delete` / `addLink` …; узнать набор можно через соответствующий `*_security`-метод), а НЕ «read».

| Метод | Назначение |
|---|---|
| `check_actions_on_objects_security_access(check)` | Метод проверки доступа текущего пользователя к операциям над объектами |
| `check_attribute_group_security_access(attribute_group_id, check)` | Метод проверки доступа текущего пользователя к конкретной группе атрибутов |
| `check_attribute_groups_security_access(check)` | Метод проверки доступа текущего пользователя к коллекции групп атрибутов |
| `check_attribute_security_access(attribute_id, check)` | Метод проверки доступа текущего пользователя к конкретному атрибуту |
| `check_attributes_security_access(check)` | Метод проверки доступа текущего пользователя к коллекции атрибутов |
| `check_languages_security_access(check)` | Метод проверки доступа текущего пользователя к коллекции языков |
| `check_lifecycle_level_security_access(lifecycle_level_id, check)` | Метод проверки доступа текущего пользователя к конкретному уровню ЖЦ |
| `check_lifecycle_levels_security_access(check)` | Метод проверки доступа текущего пользователя к коллекции уровней ЖЦ |
| `check_lifecycle_scheme_security_access(lifecycle_scheme_id, check)` | Метод проверки доступа текущего пользователя к конкретной схеме ЖЦ |
| `check_lifecycle_schemes_security_access(check)` | Метод проверки доступа текущего пользователя к коллекции схем ЖЦ |
| `check_object_security_access(object_version_id, check)` | Метод проверки доступа текущего пользователя к версии объекта |
| `check_object_type_lifecycle_step_attribute_security_access(object_type_id, lifecycle_scheme_step_id, attribute_id, check)` | Метод проверки доступа к атрибуту на шаге схемы ЖЦ для типа объекта |
| `check_object_type_lifecycle_step_security_access(object_type_id, lifecycle_scheme_step_id, check)` | Метод проверки доступа текущего пользователя к шагу схемы ЖЦ для типа объекта |
| `check_object_type_security_access(object_type_id, check)` | Метод проверки доступа текущего пользователя к конкретному типу объекта |
| `check_object_types_security_access(check)` | Метод проверки доступа текущего пользователя к коллекции типов объектов |
| `check_relation_type_security_access(relation_type_id, check)` | Метод проверки доступа текущего пользователя к конкретному типу связи |
| `check_relation_types_security_access(check)` | Метод проверки доступа текущего пользователя к коллекции типов связей |
| `check_subject_areas_security_access(check)` | Метод проверки доступа текущего пользователя к коллекции предметных областей |
| `check_system_security_access(check)` | Метод проверки доступа текущего пользователя к системе в целом |
