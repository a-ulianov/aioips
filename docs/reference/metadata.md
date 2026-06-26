# Метаданные (metadata)

**Что за раздел.** Самый большой раздел (203 метода) — справочник по **метамодели** IPS: какие
бывают типы объектов, типы атрибутов и типы связей, как они применяются друг к другу (применяемость
состава), как устроены схемы жизненного цикла, дерево наследования типов и группировка/сортировка.
Это «схема базы», а не данные конкретных объектов.

**Когда нужен.** Когда вы строите запросы и формы и вам нужно узнать **устройство модели**: id типа по
имени, какие атрибуты применимы к типу, какие потомки допустимы в составе, какие шаги ЖЦ есть у
типа. Большинство методов чтения существует в двух вариантах — по числовому `id` и по `guid`
(суффикс `_by_guid`); функционально это одно и то же, выбирайте по тому, какой идентификатор у вас на
руках.

## Типы объектов

### Описания и существование

| Метод | Назначение |
|---|---|
| `object_types()` | Возвращает список всех типов объектов, определённых в метаданных IPS. |
| `object_type(object_type_id)` | Возвращает описание типа объекта по его идентификатору. |
| `object_type_by_guid(guid)` | Возвращает описание типа объекта по его глобальному идентификатору (GUID). |
| `object_type_exists(object_type_id)` | Проверяет, существует ли тип объекта с указанным идентификатором. |
| `object_type_exists_by_guid(guid)` | Проверяет, существует ли тип объекта с указанным GUID. |
| `objects_by_object_type(object_type_id)` | Возвращает краткие сведения обо всех объектах заданного типа. |

### Имена и идентификаторы (взаимные преобразования)

| Метод | Назначение |
|---|---|
| `object_type_name(object_type_id)` | Возвращает системное имя типа объекта по его идентификатору. |
| `object_type_name_by_guid(guid)` | Возвращает системное имя типа объекта по его GUID. |
| `object_type_full_name(object_type_id)` | Возвращает полное (иерархическое) имя типа объекта по идентификатору. |
| `object_type_object_name(object_type_id)` | Возвращает имя экземпляра по умолчанию для типа объекта по идентификатору. |
| `object_type_object_name_by_guid(guid)` | Возвращает имя экземпляра по умолчанию для типа объекта по его GUID. |
| `object_type_guid(object_type_id)` | Возвращает GUID типа объекта по его числовому идентификатору. |
| `object_type_id_by_guid(guid)` | Возвращает числовой идентификатор типа объекта по его GUID. |
| `object_type_id_by_name(object_type_name)` | Возвращает идентификатор типа объекта по его имени. |

### Свойства типа объекта

| Метод | Назначение |
|---|---|
| `object_type_is_local(object_type_id)` | Проверяет, является ли тип объекта локальным для текущей базы данных. |
| `object_type_is_local_by_guid(guid)` | Проверяет, является ли тип объекта локальным, по его GUID. |
| `object_type_has_design(object_type_id)` | Проверяет, есть ли у типа объекта проектируемый тип связи (по идентификатору). |
| `object_type_has_design_by_guid(guid)` | Проверяет, есть ли у типа объекта проектируемый тип связи (по GUID). |
| `object_type_has_substitution(id)` | Проверяет, есть ли у типа объекта замещающие типы связей (по id). |
| `object_type_has_substitution_by_guid(guid)` | Проверяет, есть ли у типа объекта замещающие типы связей (по GUID). |
| `object_type_has_visibility_attribute(object_type_id)` | Проверяет, есть ли у типа объекта атрибут видимости (по идентификатору). |
| `object_type_has_visibility_attribute_by_guid(guid)` | Проверяет, есть ли у типа объекта атрибут видимости (по GUID). |
| `designed_object_type_ids()` | Возвращает идентификаторы типов объектов, имеющих проектируемые типы связей. |
| `designed_object_type_guids()` | Возвращает GUID типов объектов, имеющих проектируемые типы связей. |
| `visibility_object_type_ids()` | Возвращает идентификаторы типов объектов, имеющих атрибут видимости. |
| `visibility_object_type_guids()` | Возвращает GUID типов объектов, имеющих атрибут видимости. |
| `substitute_object_type_ids()` | Возвращает id всех типов объектов, участвующих в замещении. |
| `substitute_object_type_guids()` | Возвращает GUID всех типов объектов, участвующих в замещении. |

### Контекст редактирования и PDM

| Метод | Назначение |
|---|---|
| `is_editing_context(id)` | Проверяет, образует ли тип объекта контекст редактирования (по id). |
| `is_editing_context_by_guid(guid)` | Проверяет, образует ли тип объекта контекст редактирования (по GUID). |
| `is_simple_editing_context(id)` | Проверяет, является ли контекст редактирования типа объекта простым (по id). |
| `can_add_object_type_to_editing_context(object_type_id)` | Проверяет, можно ли добавить тип объекта в контекст редактирования (по id). |
| `can_add_object_type_to_editing_context_by_guid(object_type_guid)` | Проверяет, можно ли добавить тип объекта в контекст редактирования (по GUID). |
| `must_append_object_version(id)` | Проверяет, нужно ли добавлять версию объекта в контекст редактирования (по id). |
| `editing_context_object_type_ids()` | Возвращает id всех типов объектов, входящих в контексты редактирования. |
| `editing_context_object_type_guids()` | Возвращает GUID всех типов объектов, входящих в контексты редактирования. |
| `editing_context_top_object_type_ids()` | Возвращает id верхнеуровневых (корневых) типов контекста редактирования. |
| `editing_context_top_object_type_guids()` | Возвращает GUID верхнеуровневых (корневых) типов контекста редактирования. |
| `pdm_object_type_is_root(object_type_id)` | Проверяет, является ли тип объекта корневым в PDM (по идентификатору). |
| `pdm_object_type_is_configurable(object_type_id)` | Проверяет, является ли тип объекта конфигурируемым в PDM (по идентификатору). |
| `pdm_object_type_is_contextable(object_type_id)` | Проверяет, является ли тип объекта контекстируемым в PDM (по идентификатору). |

## Типы атрибутов

### Описания и существование

| Метод | Назначение |
|---|---|
| `attribute_types()` | Возвращает список всех типов атрибутов, определённых в метаданных IPS. |
| `attribute_type(attribute_type_id)` | Возвращает описание типа атрибута по его идентификатору. |
| `attribute_type_by_guid(guid)` | Возвращает описание типа атрибута по его глобальному идентификатору (GUID). |
| `attribute_type_exists(attribute_type_id)` | Проверяет существование типа атрибута по его идентификатору. |
| `attribute_type_exists_by_guid(guid)` | Проверяет существование типа атрибута по его GUID. |
| `attribute_type_ids()` | Возвращает список идентификаторов всех типов атрибутов метаданных. |
| `attribute_type_guids()` | Возвращает список GUID всех типов атрибутов метаданных. |

### Имена и идентификаторы (взаимные преобразования)

| Метод | Назначение |
|---|---|
| `attribute_type_name(attribute_type_id)` | Возвращает имя типа атрибута по его идентификатору. |
| `attribute_type_name_by_guid(guid)` | Возвращает имя типа атрибута по его GUID. |
| `attribute_type_guid(attribute_type_id)` | Возвращает GUID типа атрибута по его идентификатору. |
| `attribute_type_guid_by_name(attribute_name)` | Возвращает GUID типа атрибута по его имени. |
| `attribute_type_id_by_guid(guid)` | Возвращает идентификатор типа атрибута по его GUID. |
| `attribute_type_id_by_name(attribute_name)` | Возвращает идентификатор типа атрибута по его имени. |

### Свойства типа атрибута

| Метод | Назначение |
|---|---|
| `attribute_type_applicability(attribute_type_id)` | Возвращает категорию применимости типа атрибута по его идентификатору. |
| `attribute_type_applicability_by_guid(guid)` | Возвращает категорию применимости типа атрибута по его GUID. |
| `attribute_has_possible_values(attribute_type_id)` | Проверяет, задан ли у типа атрибута список допустимых значений (по id). |
| `attribute_has_possible_values_by_guid(guid)` | Проверяет, задан ли у типа атрибута список допустимых значений (по GUID). |
| `attribute_has_system_data(attribute_type_id)` | Проверяет, несёт ли тип атрибута системные данные (по id). |
| `attribute_has_system_data_by_guid(guid)` | Проверяет, несёт ли тип атрибута системные данные (по GUID). |
| `attribute_is_gridable(attribute_type_id)` | Проверяет, можно ли выводить тип атрибута колонкой таблицы (по id). |
| `attribute_is_gridable_by_guid(guid)` | Проверяет, можно ли выводить тип атрибута колонкой таблицы (по GUID). |
| `attribute_is_in_use(attribute_type_id)` | Проверяет, используется ли тип атрибута где-либо (по id). |
| `attribute_is_in_use_by_guid(guid)` | Проверяет, используется ли тип атрибута где-либо (по GUID). |
| `attribute_supports_object_links(guid)` | Проверяет, поддерживает ли системный тип атрибута ссылки на объекты (по GUID). |
| `attribute_linked_object_type_ids(attribute_type_id)` | Возвращает id типов объектов, на которые может ссылаться атрибут-ссылка. |
| `object_link_attribute_type_ids(object_type_id)` | Возвращает id типов атрибутов-ссылок, которые могут указывать на тип объекта. |

## Применяемость атрибутов (атрибут ↔ тип)

| Метод | Назначение |
|---|---|
| `attribute_for_object_type_list(object_type_id)` | Возвращает список типов атрибутов, применимых к заданному типу объекта. |
| `attribute_for_object_type_list_by_guid(object_type_guid)` | Возвращает список атрибутов, применимых к типу объекта, по его GUID. |
| `attribute_for_object_type(object_type_id, attribute_type_id)` | Возвращает настройку применения одного атрибута к одному типу объекта. |
| `attribute_for_object_type_by_guids(object_type_guid, attribute_type_guid)` | Возвращает настройку применения атрибута к типу объекта по паре GUID. |
| `attribute_for_relation_type_list(relation_type_id)` | Возвращает список типов атрибутов, применимых к заданному типу связи. |
| `attribute_for_relation_type_list_by_guid(relation_type_guid)` | Возвращает список атрибутов, применимых к типу связи, по его GUID. |
| `attribute_for_relation_type(relation_type_id, attribute_type_id)` | Возвращает настройку применения одного атрибута к одному типу связи. |
| `attribute_for_relation_type_by_guids(relation_type_guid, attribute_type_guid)` | Возвращает настройку применения атрибута к типу связи по паре GUID. |
| `all_attributes_for_object_type_list(attribute_type_id)` | Возвращает все привязки заданного атрибута ко всем типам объектов. |
| `all_attributes_for_object_type_list_by_guid(attribute_type_guid)` | Возвращает все привязки атрибута ко всем типам объектов по GUID атрибута. |
| `all_attributes_for_relation_type_list(attribute_type_id)` | Возвращает все привязки заданного атрибута ко всем типам связей. |
| `all_attributes_for_relation_type_list_by_guid(attribute_type_guid)` | Возвращает все привязки атрибута ко всем типам связей по GUID атрибута. |
| `related_formula_attributes_for_object(object_type_id, attribute_type_id)` | Возвращает id формульных атрибутов объекта, зависящих от заданного атрибута. |
| `related_formula_attributes_for_relation(relation_type_id, attribute_type_id)` | Возвращает id формульных атрибутов связи, зависящих от заданного атрибута. |

## Группы атрибутов

| Метод | Назначение |
|---|---|
| `attribute_group(attribute_group_id)` | Возвращает описание группы атрибутов по её идентификатору. |
| `attribute_group_by_guid(guid)` | Возвращает описание группы атрибутов по её GUID. |
| `attribute_group_guid(attribute_group_id)` | Возвращает GUID группы атрибутов по её идентификатору. |
| `attribute_group_id_by_guid(guid)` | Возвращает идентификатор группы атрибутов по её GUID. |
| `attributes_in_group_ids(attribute_group_id)` | Возвращает id типов атрибутов, входящих в группу (по id группы). |
| `attributes_in_group_ids_by_guid(guid)` | Возвращает id типов атрибутов, входящих в группу (по GUID группы). |
| `attributes_in_group_guids(attribute_group_id)` | Возвращает GUID типов атрибутов, входящих в группу (по id группы). |
| `attributes_in_group_guids_by_guid(guid)` | Возвращает GUID типов атрибутов, входящих в группу (по GUID группы). |

## Типы связей (метаданные)

| Метод | Назначение |
|---|---|
| `relation_types_meta()` | Возвращает список всех типов связей, определённых в метаданных IPS. |
| `relation_type_meta(relation_type_id)` | Возвращает описание типа связи по его идентификатору. |
| `relation_type_meta_by_guid(guid)` | Возвращает описание типа связи по его глобальному идентификатору (GUID). |
| `relation_type_meta_exists(relation_type_id)` | Проверяет, существует ли тип связи с заданным идентификатором. |
| `relation_type_meta_exists_by_guid(guid)` | Проверяет, существует ли тип связи с заданным GUID. |
| `relation_type_meta_name(relation_type_id)` | Возвращает прямое имя типа связи по его идентификатору. |
| `relation_type_meta_name_by_guid(guid)` | Возвращает прямое имя типа связи по его GUID. |
| `relation_type_meta_guid(relation_type_id)` | Возвращает GUID типа связи по его числовому идентификатору. |
| `relation_type_meta_id_by_guid(guid)` | Возвращает числовой идентификатор типа связи по его GUID. |
| `relation_type_for_prj_link(prj_link_id)` | Возвращает id типа связи для заданной связи проекта (prjLink). |
| `default_relation_type_id(parent_object_type_id)` | Возвращает id типа связи по умолчанию для заданного типа объекта-родителя. |
| `default_relation_type_id_by_guid(parent_object_type_guid)` | Возвращает id типа связи по умолчанию по GUID типа объекта-родителя. |
| `default_relation_type_guid(parent_object_type_id)` | Возвращает GUID типа связи по умолчанию для заданного типа объекта-родителя. |
| `default_relation_type_guid_by_guid(parent_object_type_guid)` | Возвращает GUID типа связи по умолчанию по GUID типа объекта-родителя. |
| `relation_type_has_substitutes(id)` | Проверяет, поддерживает ли тип связи замещения (по id). |
| `relation_type_has_substitutes_by_guid(guid)` | Проверяет, поддерживает ли тип связи замещения (по GUID). |
| `substitute_relation_type_ids()` | Возвращает id всех специальных типов связей замещения. |
| `substitute_relation_type_guids()` | Возвращает GUID всех специальных типов связей замещения. |
| `pdm_relation_type_is_configurable(relation_type_id)` | Проверяет, является ли тип связи конфигурируемым в PDM (по идентификатору). |
| `pdm_relation_type_is_partially_configurable(relation_type_id)` | Проверяет, частично ли конфигурируем тип связи в PDM (по идентификатору). |

## Применяемость состава (родитель / потомок / связь)

Применяемость задаёт, какие потомки и по какой связи допустимы в составе родителя. См.
[Связи и состав](../concepts/data-model.md).

| Метод | Назначение |
|---|---|
| `applicabilities()` | Возвращает ВСЕ настроенные в базе правила применяемости. |
| `applicability(parent_object_type_id, child_object_type_id, relation_type_id)` | Возвращает правило применяемости для конкретной тройки родитель/потомок/связь. |
| `has_applicability(parent_object_type_id)` | Проверяет, может ли объект данного типа иметь состав (хоть одну применяемость). |
| `has_applicability_by_guid(parent_object_type_guid)` | Проверяет, есть ли у типа-родителя (по GUID) хоть одна применяемость. |
| `has_applicability_full(parent_object_type_id, child_object_type_id, relation_type_id)` | Проверяет существование применяемости для конкретной тройки родитель/потомок/связь. |
| `object_type_applicabilities(object_type_id)` | Возвращает правила применяемости для типа объекта как РОДИТЕЛЯ состава. |
| `object_type_applicabilities_by_guid(object_type_guid)` | Возвращает правила применяемости типа-РОДИТЕЛЯ, заданного GUID. |
| `object_type_parent_applicabilities(part_type_id)` | Возвращает правила применяемости для типа объекта как ПОТОМКА состава. |
| `applicability_child_object_types(parent_object_type_id, relation_type_id)` | Возвращает полные описания дочерних типов, допустимых в составе по одной связи. |
| `applicability_child_object_types_by_guids(parent_object_type_guid, relation_type_guid)` | Возвращает описания дочерних типов, допустимых в составе, по GUID родителя и связи. |
| `applicability_child_object_type_ids(parent_object_type_id, relation_type_id)` | Возвращает id дочерних типов, допустимых в составе родителя по одной связи. |
| `applicability_child_object_type_guids(parent_object_type_id, relation_type_id)` | Возвращает GUID дочерних типов, допустимых в составе родителя по одной связи. |
| `child_object_type_ids(parent_object_type_id, relation_type_ids)` | Возвращает id дочерних типов, допустимых в составе родителя по заданным связям. |
| `applicability_relation_type_ids(object_type_id)` | Возвращает id типов связей, участвующих в применяемостях данного типа объекта. |
| `applicability_relation_type_guids(object_type_id)` | Возвращает GUID типов связей, участвующих в применяемостях данного типа объекта. |
| `applicability_relation_type_ids_by_guid(object_type_guid)` | То же, что `applicability_relation_type_ids`, но тип-родитель адресуется GUID. |
| `applicability_relation_type_guids_by_guid(object_type_guid)` | То же, что `applicability_relation_type_guids`, но тип-родитель адресуется GUID. |
| `applicability_child_object_type_ids_by_guids(parent_object_type_guid, relation_type_guid)` | id дочерних типов состава по GUID родителя и GUID типа связи. |
| `applicability_child_object_type_guids_by_guids(parent_object_type_guid, relation_type_guid)` | GUID дочерних типов состава по GUID родителя и GUID типа связи. |
| `object_types_with_applicabilities_ids()` | Возвращает id всех типов объектов, у которых задана хотя бы одна применяемость. |
| `object_types_with_enter_in_applicabilities_ids()` | Возвращает id всех типов объектов, которые могут входить в чей-либо состав. |
| `can_enters_in(part_type_id)` | Проверяет, может ли объект данного типа входить в чей-либо состав. |

### Классификация GUID метаданных

| Метод | Назначение |
|---|---|
| `globals_by_guid(guid)` | Определяет ВИД сущности метаданных по GUID (тип объекта/атрибута/связи/ЖЦ или `unknown`). |
| `displayable_by_guid(guid)` | Возвращает человекочитаемую подпись (`{text}`) сущности метаданных по GUID. |

## Схемы, уровни и шаги жизненного цикла

См. также [Жизненный цикл](../concepts/lifecycle.md).

### Схемы ЖЦ

| Метод | Назначение |
|---|---|
| `life_cycle_schemes()` | Возвращает список всех схем жизненного цикла, определённых в метаданных IPS. |
| `life_cycle_scheme(scheme_id)` | Возвращает описание схемы жизненного цикла по её идентификатору. |
| `life_cycle_scheme_by_guid(guid)` | Возвращает описание схемы жизненного цикла по её GUID. |
| `life_cycle_scheme_exists(scheme_id)` | Проверяет, существует ли схема жизненного цикла с указанным идентификатором. |
| `life_cycle_scheme_exists_by_guid(guid)` | Проверяет, существует ли схема жизненного цикла с указанным GUID. |
| `life_cycle_scheme_name(scheme_id)` | Возвращает имя схемы жизненного цикла по её идентификатору. |
| `life_cycle_scheme_name_by_guid(guid)` | Возвращает имя схемы жизненного цикла по её GUID. |
| `life_cycle_scheme_guid(scheme_id)` | Возвращает GUID схемы жизненного цикла по её числовому идентификатору. |
| `life_cycle_scheme_id_by_guid(guid)` | Возвращает числовой идентификатор схемы жизненного цикла по её GUID. |
| `life_cycle_scheme_steps(scheme_id)` | Возвращает список шагов указанной схемы жизненного цикла. |

### Уровни ЖЦ

| Метод | Назначение |
|---|---|
| `life_cycle_levels()` | Возвращает список всех уровней жизненного цикла, определённых в IPS. |
| `life_cycle_level(life_cycle_level_id)` | Возвращает описание уровня жизненного цикла по его идентификатору. |
| `life_cycle_level_by_guid(guid)` | Возвращает описание уровня жизненного цикла по его GUID. |
| `life_cycle_level_exists(life_cycle_level_id)` | Проверяет, существует ли уровень жизненного цикла с указанным идентификатором. |
| `life_cycle_level_exists_by_guid(guid)` | Проверяет, существует ли уровень жизненного цикла с указанным GUID. |
| `life_cycle_level_name(life_cycle_level_id)` | Возвращает имя уровня жизненного цикла по его идентификатору. |
| `life_cycle_level_name_by_guid(guid)` | Возвращает имя уровня жизненного цикла по его GUID. |
| `life_cycle_level_guid(life_cycle_level_id)` | Возвращает GUID уровня жизненного цикла по его числовому идентификатору. |
| `life_cycle_level_id_by_guid(guid)` | Возвращает числовой идентификатор уровня жизненного цикла по его GUID. |

### Шаги ЖЦ

| Метод | Назначение |
|---|---|
| `life_cycle_steps()` | Возвращает полный список шагов (состояний) жизненного цикла из метаданных. |
| `life_cycle_step(life_cycle_step_id)` | Возвращает описание шага (состояния) жизненного цикла по его идентификатору. |
| `life_cycle_step_by_guid(guid)` | Возвращает описание шага жизненного цикла по его глобальному GUID. |
| `life_cycle_step_exists(life_cycle_step_id)` | Проверяет, существует ли шаг жизненного цикла с указанным идентификатором. |
| `life_cycle_step_exists_by_guid(guid)` | Проверяет, существует ли шаг жизненного цикла с указанным GUID. |
| `life_cycle_step_name(life_cycle_step_id)` | Возвращает название шага жизненного цикла по его идентификатору. |
| `life_cycle_step_name_by_guid(guid)` | Возвращает название шага жизненного цикла по его GUID. |
| `life_cycle_step_guid(life_cycle_step_id)` | Возвращает GUID шага жизненного цикла по его числовому идентификатору. |
| `life_cycle_step_id_by_guid(guid)` | Возвращает числовой идентификатор шага жизненного цикла по его GUID. |
| `object_type_life_cycle_steps(object_type_id)` | Возвращает список шагов жизненного цикла для типа объекта. |

## Группировка и сортировка

| Метод | Назначение |
|---|---|
| `groupable_object_type_ids()` | Возвращает id типов объектов, экземпляры которых можно группировать. |
| `groupable_object_type_guids()` | Возвращает GUID типов объектов, экземпляры которых можно группировать. |
| `grouping_object_type_ids()` | Возвращает id типов объектов, которые ВЫПОЛНЯЮТ группировку. |
| `grouping_object_type_guids()` | Возвращает GUID типов объектов, которые ВЫПОЛНЯЮТ группировку. |
| `grouping_relation_type_ids()` | Возвращает id типов связей, по которым выполняется группировка. |
| `grouping_relation_type_guids()` | Возвращает GUID типов связей, по которым выполняется группировка. |
| `object_type_is_groupable(object_type_id)` | Проверяет, можно ли группировать экземпляры типа объекта (по id). |
| `object_type_is_groupable_by_guid(guid)` | Проверяет, можно ли группировать экземпляры типа объекта (по GUID). |
| `object_type_has_grouping(object_type_id)` | Проверяет, выполняет ли тип объекта группировку (по id). |
| `object_type_has_grouping_by_guid(guid)` | Проверяет, выполняет ли тип объекта группировку (по GUID). |
| `relation_type_has_grouping(relation_type_id)` | Проверяет, участвует ли тип связи в группировке (по id). |
| `relation_type_has_grouping_by_guid(guid)` | Проверяет, участвует ли тип связи в группировке (по GUID). |
| `sorting_object_type_ids()` | Возвращает id типов объектов, экземпляры которых можно сортировать. |
| `sorting_object_type_guids()` | Возвращает GUID типов объектов, экземпляры которых можно сортировать. |
| `sorting_relation_type_ids()` | Возвращает id типов связей, по которым выполняется сортировка. |
| `sorting_relation_type_guids()` | Возвращает GUID типов связей, по которым выполняется сортировка. |
| `object_type_has_sorting(object_type_id)` | Проверяет, поддерживает ли тип объекта сортировку (по id). |
| `object_type_has_sorting_by_guid(guid)` | Проверяет, поддерживает ли тип объекта сортировку (по GUID). |
| `relation_type_has_sorting(relation_type_id)` | Проверяет, участвует ли тип связи в сортировке (по id). |
| `relation_type_has_sorting_by_guid(guid)` | Проверяет, участвует ли тип связи в сортировке (по GUID). |
| `used_sorted_attributes()` | Возвращает используемые типы атрибутов в порядке сортировки. |
| `used_sorted_attribute_ids()` | Возвращает идентификаторы используемых атрибутов в порядке сортировки. |
| `used_unsorted_attribute_ids()` | Возвращает идентификаторы используемых атрибутов без порядка сортировки. |

## Дерево типов (иерархия наследования)

«Дерево типов» — это наследование типов объектов (родитель/потомок), не путать с составом изделия.

### Родители (предки)

| Метод | Назначение |
|---|---|
| `parent_type_id(child_type_id)` | Возвращает id НЕПОСРЕДСТВЕННОГО родительского типа в иерархии типов. |
| `parent_type_guid_by_guid(child_type_guid)` | Возвращает GUID НЕПОСРЕДСТВЕННОГО родительского типа по GUID потомка. |
| `parent_type_ids(child_type_id)` | Возвращает id ВСЕЙ цепочки родительских типов (предков) в иерархии типов. |
| `parent_type_ids_by_guid(child_type_guid)` | Возвращает id ВСЕЙ цепочки родительских типов по GUID потомка. |
| `parent_type_guids(child_type_id)` | Возвращает GUID ВСЕЙ цепочки родительских типов (предков) в иерархии типов. |
| `parent_type_guids_by_guid(child_type_guid)` | Возвращает GUID ВСЕЙ цепочки родительских типов по GUID потомка. |
| `parent_type_ids_reverse(child_type_id)` | Возвращает id цепочки родительских типов в ОБРАТНОМ порядке (от корня вниз). |
| `top_parent_type_id(child_type_id)` | Возвращает id КОРНЕВОГО типа ветви иерархии для заданного типа. |
| `common_parent_type_id(child_type1_id, child_type2_id)` | Возвращает id ближайшего ОБЩЕГО предка для пары типов объектов. |
| `object_type_level(id)` | Возвращает уровень (глубину) типа объекта в дереве типов. |

### Потомки

| Метод | Назначение |
|---|---|
| `children_type_ids(parent_type_id)` | Возвращает id ПРЯМЫХ дочерних типов объектов в иерархии типов. |
| `children_type_ids_by_guid(parent_type_guid)` | Возвращает id ПРЯМЫХ дочерних типов объектов по GUID родительского типа. |
| `children_type_guids(parent_type_id)` | Возвращает GUID ПРЯМЫХ дочерних типов объектов в иерархии типов. |
| `children_type_guids_by_guid(parent_type_guid)` | Возвращает GUID ПРЯМЫХ дочерних типов объектов по GUID родительского типа. |
| `children_type_ids_recursive(parent_type_id)` | Возвращает id ВСЕХ потомков типа объекта рекурсивно (всё поддерево). |
| `children_type_ids_recursive_by_guid(parent_type_guid)` | Возвращает id ВСЕХ потомков типа рекурсивно по GUID родительского типа. |
| `children_type_guids_recursive(parent_type_id)` | Возвращает GUID ВСЕХ потомков типа объекта рекурсивно (всё поддерево). |
| `children_type_guids_recursive_by_guid(parent_type_guid)` | Возвращает GUID ВСЕХ потомков типа рекурсивно по GUID родительского типа. |
| `local_children_type_ids_recursive(parent_type_id)` | Возвращает id ЛОКАЛЬНЫХ потомков типа объекта рекурсивно (всё поддерево). |
| `child_object_type_ids(parent_object_type_id, relation_type_ids)` | Возвращает id дочерних типов, допустимых в составе родителя по заданным связям. |

### Проверки родства и корни

| Метод | Назначение |
|---|---|
| `is_object_type_child(child_type_id, parent_type_id)` | Проверяет, является ли тип потомком другого типа в иерархии (по id обоих). |
| `is_object_type_child_by_guids(child_type_guid, parent_type_guid)` | Проверяет, является ли тип потомком другого (оба адресуются по GUID). |
| `is_object_type_child_by_child_id_parent_guid(child_type_id, parent_type_guid)` | Проверяет, является ли тип потомком другого: id потомка + GUID родителя. |
| `top_object_type_ids()` | Возвращает id всех КОРНЕВЫХ типов объектов (верхний уровень дерева). |
| `top_object_type_guids()` | Возвращает GUID всех КОРНЕВЫХ типов объектов (верхний уровень дерева). |
