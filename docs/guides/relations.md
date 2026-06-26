# Связи и состав

Это руководство — про **связи между объектами**: как их читать, создавать и удалять, и как работать с
атрибутами самих связей. Связь в IPS направленная: «родитель → потомок». Так строится состав изделия.

!!! tip "Что такое связь"
    Связь (`Relation`) соединяет объект-**родитель** (`proj_id` — это `ObjectID` родителя) с **версией
    потомка** (`part_id` — это `ID` версии потомка). У связи есть тип (`relation_type`, например
    «Состоит из») и собственные атрибуты (например, позиционное обозначение или количество).
    Подробнее: [Связи и состав](../concepts/data-model.md).

!!! danger "RelationID нестабилен — не кэшируйте его"
    Числовой `relation_id` **меняется** после `check_out`/`check_in` родителя. Не сохраняйте его как
    долговременный ключ. Для устойчивой идентификации используйте `guid` связи или тройку
    (`proj_id`, `part_id`, `relation_type`). Перед удалением берите свежий id.

## Карта методов

| Метод | Что делает |
|---|---|
| `relation_get(relation_id)` | Возвращает связь по id |
| `relations_by_project(project_id, relation_type_id)` | Все связи родителя указанного типа |
| `relation_create(CreateRelation(...))` | Создаёт связь «родитель → потомок» |
| `relation_delete(relation_id, confirm=True)` | Удаляет связь (необратимо) |
| `relation_attributes(relation_id)` | Читает атрибуты самой связи |
| `relation_set_attribute_values(relation_id, [...])` | Пишет атрибуты связи (нужен checkout родителя) |

---

## Задача 1. Прочитать связи

**Когда нужно:** узнать состав родителя или получить конкретную связь по id.

### Решение

- Все связи родителя одного типа: `relations_by_project(project_id, relation_type_id)`. Здесь
  `project_id` — это **id объекта-родителя** (`ObjectID`), а `relation_type_id` берётся из справочника
  типов (`relation_types`).
- Одна связь по свежему id: `relation_get(relation_id)`.

### Полный пример

```python
import asyncio

from aioips import IPSClient, IPSConfig


async def main() -> None:
    config = IPSConfig()
    async with IPSClient(config=config) as ips:
        # Все связи типа 0 (например, "Состоит из") у родителя с ObjectID 6.
        relations = await ips.relations_by_project(project_id=6, relation_type_id=0)
        print("Связей:", len(relations))
        for r in relations[:5]:
            # proj_id = ObjectID родителя; part_id = ID версии потомка.
            print(r.relation_id, r.proj_id, r.part_id, r.relation_type)

        # Полная запись одной связи по свежему id.
        one = await ips.relation_get(relations[0].relation_id)
        if one is not None:
            print(one.guid, one.create_date)


if __name__ == "__main__":
    asyncio.run(main())
```

!!! warning "project_id — это ObjectID родителя, а не id версии"
    Имя `projectId` в пути вводит в заблуждение: метод принимает `ObjectID` объекта-родителя (общий
    для всех версий). А `part_id` в результате — это **id версии** потомка (`F_ID`); напрямую в
    `object_get` его подавать нельзя — для объекта-потомка используйте поле `part_object_id` связи
    (если оно не `0`).

---

## Задача 2. Создать связь (включить объект в состав другого)

**Когда нужно:** добавить потомка в состав родителя.

### Решение

1. **Извлечь РОДИТЕЛЯ на редактирование** — `object_check_out(id_родителя)`. Создание связи меняет
   родителя, поэтому он должен быть на checkout (см. [Редактирование объектов](editing-objects.md)).
2. Собрать описание связи — `CreateRelation(relation_type=..., proj_version_id=..., part_version_id=...)`.
   Внимание: оба конца — это **id ОБЪЕКТОВ** (`ObjectID`), а не id версий.
3. Вызвать `relation_create(...)`.
4. **Зафиксировать родителя** — `object_check_in(working_id)`.

### Полный пример

```python
from aioips.schemas.relations import CreateRelation

async with IPSClient(config=config) as ips:
    # 1. Родитель на редактирование.
    working_parent = await ips.object_check_out(102550)

    # 2-3. Создаём связь: оба конца — ObjectID объектов.
    rel = await ips.relation_create(
        CreateRelation(
            relation_type=0,          # тип связи из relation_types()
            proj_version_id=102550,   # ObjectID родителя
            part_version_id=102777,   # ObjectID потомка (0 — без привязки к версии)
        )
    )
    print("Создана связь:", rel.relation_id)

    # 4. Фиксируем родителя.
    await ips.object_check_in(working_parent)
```

!!! warning "Создание связи требует checkout родителя"
    Без извлечения родителя на редактирование сервер вернёт ошибку. Кроме того, тип связи должен быть
    **допустим** для этих типов объектов (применяемость) — иначе будет `400`.

!!! tip "Сразу задать атрибуты связи"
    В `CreateRelation` можно передать `attribute_values=[AttributeValues(...)]`, чтобы создать связь
    уже с заполненными атрибутами. Для пакетного создания нескольких связей за один запрос есть
    `relation_create_collection`.

---

## Задача 3. Удалить связь

**Когда нужно:** исключить потомка из состава (удаляется именно связь, объекты-концы остаются).

### Решение

1. Извлечь родителя на редактирование (`object_check_out`).
2. Получить **свежий** `relation_id` (он нестабилен!).
3. Вызвать `relation_delete(relation_id, confirm=True)`. Без `confirm=True` — `ValueError`.
4. Зафиксировать родителя (`object_check_in`).

### Полный пример

```python
async with IPSClient(config=config) as ips:
    working_parent = await ips.object_check_out(102550)

    # Берём свежий id связи прямо перед удалением.
    relations = await ips.relations_by_project(project_id=102550, relation_type_id=0)
    target = relations[0]

    await ips.relation_delete(target.relation_id, confirm=True)

    await ips.object_check_in(working_parent)
```

!!! danger "relation_delete необратима и требует confirm=True"
    Без `confirm=True` метод поднимает `ValueError` и **не обращается к серверу**. Удаляется связь, а
    не объекты. Поскольку `relation_id` нестабилен, получайте его непосредственно перед удалением.

---

## Задача 4. Атрибуты связи

**Когда нужно:** связь несёт собственные характеристики (позиционное обозначение, количество и т.п.) —
их можно читать и писать отдельно от объектов-концов.

### Решение

- **Чтение:** `relation_attributes(relation_id)` → `list[Attribute]` (checkout не нужен).
- **Запись:** `relation_set_attribute_values(relation_id, [AttributeValues(...)])` — требует, чтобы
  **родитель** связи был извлечён на редактирование.

### Полный пример

```python
from aioips.schemas.objects import AttributeValues

async with IPSClient(config=config) as ips:
    # Чтение атрибутов связи.
    attrs = await ips.relation_attributes(target.relation_id)
    print({a.name: a.as_string for a in attrs})

    # Запись (родитель должен быть на checkout).
    working_parent = await ips.object_check_out(102550)
    await ips.relation_set_attribute_values(
        target.relation_id,
        [AttributeValues(attribute_id=205, values=["A1"])],
        return_delta=True,
    )
    await ips.object_check_in(working_parent)
```

!!! warning "Запись атрибутов связи адресуется по relationID, но правит связь"
    В отличие от записи атрибутов объекта (адресуется по `objectID`), здесь адрес — `relationID`, и
    меняются собственные атрибуты связи, а не её объекты. При `return_delta=False` сервер вернёт
    пустой список (это нормально), а не изменённые значения.

## Что дальше

- Создание/удаление связи — частный случай записи; общий цикл checkout — в
  [Редактировании объектов](editing-objects.md).
- Развернуть состав целиком (потомков по версии проекта) можно через `object_composition` —
  см. [Поиск и выборки](searching.md).
- Что значат ошибки 400/409 при работе со связями — [Обработка ошибок](error-handling.md).
