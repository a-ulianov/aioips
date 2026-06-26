# Поиск и выборки

Это руководство — про то, как **найти объекты, когда их id заранее неизвестны**: отфильтровать по
типу и значениям атрибутов, перечислить все версии объекта, развернуть состав изделия. Все методы
здесь — только чтение.

!!! tip "Типичный сценарий"
    Сначала находим объекты через `objects_select` (получаем их id), затем при необходимости тащим
    каждый целиком через [`object_get`](reading-objects.md). Поиск возвращает только id и запрошенные
    значения атрибутов, а не полные объекты.

## Карта методов

| Метод | Что делает |
|---|---|
| `objects_select(object_type_id, conditions=[...])` | Ищет объекты типа по условиям на атрибуты |
| `objects_all_versions(AllObjectVersionsParameters(...))` | Перечисляет все версии одного объекта |
| `object_composition(project_version_id)` | Возвращает состав (потомков) по версии проекта |

---

## Задача 1. Найти объекты по значениям атрибутов

**Когда нужно:** есть тип объекта и условие (например, «все документы такого-то архива» или «детали
с массой больше N»), а конкретные id неизвестны.

### Решение

1. Соберите условия — список `SelectCondition`. У каждого: `attribute_id` (по какому атрибуту),
   `relational_operator` (как сравнивать — `RelationalOperator`), `value` (с чем сравнивать).
2. Для атрибута-ссылки (`ftObjectLink`) укажите `content=ColumnContent.ID` и передайте в `value`
   **id связанного объекта**.
3. Вызовите `objects_select(object_type_id, conditions=[...], attribute_ids=[...])`. В `attribute_ids`
   перечислите id атрибутов, значения которых хотите получить в результате.
4. Пройдитесь по `list[ObjectSelectResult]`: у каждого есть `object_id` и `values` (словарь
   `{attribute_id: value}`).

### Полный пример

```python
import asyncio

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ColumnContent, RelationalOperator
from aioips.schemas.objects import SelectCondition


async def main() -> None:
    config = IPSConfig()
    async with IPSClient(config=config) as ips:
        # Все документы типа 1742, входящие в архив с id 1240084.
        # Членство в архиве задаётся атрибутом-ссылкой 1029 (ftObjectLink),
        # поэтому сравниваем по ID связанного объекта.
        results = await ips.objects_select(
            object_type_id=1742,
            conditions=[
                SelectCondition(
                    attribute_id=1029,
                    relational_operator=RelationalOperator.EQUAL,
                    value=1240084,
                    content=ColumnContent.ID,
                )
            ],
            attribute_ids=[9, 10],  # вернуть Обозначение (9) и Наименование (10)
        )

        print("Найдено объектов:", len(results))
        for r in results[:5]:
            print(r.object_id, r.values.get(9), r.values.get(10))


if __name__ == "__main__":
    asyncio.run(main())
```

### Операторы сравнения (`RelationalOperator`)

Чаще всего нужны:

| Оператор | Смысл |
|---|---|
| `EQUAL` / `NOT_EQUAL` | Точное (не)совпадение |
| `GREATER` / `LESS` / `GREATER_OR_EQUAL` / `LESS_OR_EQUAL` | Числовые/датовые сравнения |
| `SUBSTRING` | Содержит подстроку |
| `START_STRING` / `END_STRING` | Начинается / заканчивается на |
| `BETWEEN` | В диапазоне (нужен и `value`, и `value2`) |
| `EMPTY` / `NOT_EMPTY` | Значение (не)пустое |
| `IN` / `NOT_IN` | (Не)входит в перечень значений |

Несколько условий объединяются логическим оператором каждого условия (`logical_operator`, по
умолчанию `AND`) и группируются через `group_id`.

!!! warning "Для ссылок сравнивайте по ID, а не по тексту"
    Архив документа, как и любая ссылка на объект, хранится как **id связанного объекта**, а не как
    его название. Поэтому для атрибута-ссылки всегда `content=ColumnContent.ID` и в `value` — числовой
    id. Если искать по тексту, ничего не найдётся. Подробнее: [Поиск объектов](../concepts/data-model.md).

!!! warning "Результат зависит от контекста версий"
    Сервер фильтрует версии по своему контексту, поэтому одна и та же выборка может вернуть разное в
    зависимости от настроек. Для воспроизводимости фиксируйте условия. Пагинация — keyset (через
    `record_count`), не offset.

---

## Задача 2. Перечислить все версии объекта

**Когда нужно:** нужна история объекта — все его версии (рабочая, предыдущие, при желании заготовки и
удалённые).

### Решение

1. Соберите параметры `AllObjectVersionsParameters(id=..., attribute_ids=[...])`.
2. Вызовите `objects_all_versions(params)`.
3. Результат — `list[ObjectSelectResult]` (тот же формат, что у поиска).

### Полный пример

```python
from aioips.schemas.objects import AllObjectVersionsParameters

async with IPSClient(config=config) as ips:
    versions = await ips.objects_all_versions(
        AllObjectVersionsParameters(id=102550, attribute_ids=[9, 10]),
    )
    for v in versions:
        print(v.object_id, v.values)
```

!!! warning "Семантика id управляется флагом is_object_id"
    В `AllObjectVersionsParameters` поле `id` трактуется в зависимости от `is_object_id`. При
    `is_object_id=False` (поведение сервера по умолчанию) `id` понимается как идентификатор объекта
    (общий для версий). Формулировки в swagger противоречивы — поведение проверено на проде, при
    сомнениях экспериментируйте на тестовом объекте.

---

## Задача 3. Развернуть состав изделия

**Когда нужно:** нужны дочерние объекты в составе сборки/изделия («родитель → потомки»).

### Решение

1. Вызовите `object_composition(project_version_id)`, передав **id версии** проекта.
2. Результат — `list[ObjectDto]` дочерних объектов.

### Полный пример

```python
async with IPSClient(config=config) as ips:
    parts = await ips.object_composition(279514)  # id ВЕРСИИ проекта
    print("Потомков в составе:", len(parts))
    for part in parts[:5]:
        print(part.object_id, part.caption)
```

!!! warning "object_composition принимает id ВЕРСИИ, а не id объекта"
    В отличие от большинства методов чтения, здесь в путь идёт `projectVersionId` — это id **версии**
    (`F_ID`), от которой берётся состав, а **не** id объекта. Это исключение из общего правила —
    легко перепутать.

!!! tip "Когда нужна фильтрация состава"
    Если требуется отобрать потомков по типу связи или типам объектов, используйте
    `object_composition_with_params` — он принимает дополнительные параметры фильтрации. Для связей
    конкретного типа у конкретного родителя см. также [Связи и состав](relations.md).

## Что дальше

- Нашли объекты — теперь [прочитайте](reading-objects.md) их целиком по id.
- Хотите изменить найденное? [Редактирование объектов](editing-objects.md).
- Работа со структурой сборок целиком — [Связи и состав](relations.md).
