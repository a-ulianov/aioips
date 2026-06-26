# Редактирование объектов

Это самое важное руководство по записи. В IPS **нельзя просто взять и поменять атрибут** — любые
изменения проходят через жизненный цикл объекта: его сначала извлекают на редактирование (checkout),
правят, а потом фиксируют (checkin) или откатывают. Создание объекта тоже двухшаговое: сначала
черновик, потом фиксация.

!!! danger "Запись идёт по id РАБОЧЕЙ КОПИИ, а не базового объекта"
    Когда вы извлекаете объект на редактирование, метод `object_check_out` возвращает id **рабочей
    копии** (обычно отрицательный, временный). Все методы записи (`set_attribute_values` и др.) надо
    вызывать **именно на этом id рабочей копии**, а не на id исходного объекта. Иначе сервер ответит
    `400`: «Для изменения объекта … нужна рабочая копия». Это ключевая грабля — запомните её.

## Карта методов цикла

| Метод | Что делает | Что возвращает |
|---|---|---|
| `object_create(object_type)` | Создаёт черновик (временный отрицательный id) | `ObjectDto` (черновик) |
| `object_commit_creation(draft_id)` | Фиксирует черновик → постоянный объект | `int` — **положительный** id объекта |
| `object_check_out(object_id)` | Извлекает на редактирование | `int` — id **рабочей копии** |
| `object_set_attribute_values(working_id, [...])` | Записывает значения атрибутов | `list[AttributeValues]` |
| `object_check_in(working_id)` | Фиксирует правку, снимает блокировку | `int` — id результирующей версии |
| `object_cancel_changes([object_id], confirm=True)` | Откатывает несохранённые правки | `list[int]` |
| `object_delete(object_id, confirm=True)` | Удаляет объект (необратимо) | `int` — код (`0` — успех) |

---

## Задача 1. Создать новый объект и записать его атрибуты

**Когда нужно:** добавить в IPS новый объект (например, комментарий, документ, элемент справочника) и
сразу задать его характеристики.

### Решение (полный цикл записи)

1. **Создать черновик** — `object_create(object_type)`. Вернётся `ObjectDto` с временным
   отрицательным `object_id` и `is_creation_mode == True`. Объекта в базе ещё **нет**.
2. **Зафиксировать создание** — `object_commit_creation(draft.object_id)`. Вернётся **постоянный
   положительный** id объекта. Теперь объект существует.
3. **Извлечь на редактирование** — `object_check_out(object_id)`. Вернётся id **рабочей копии**.
4. **Записать атрибуты** — `object_set_attribute_values(working_id, [...])`, передав id **рабочей
   копии** из шага 3.
5. **Зафиксировать правку** — `object_check_in(working_id)`. Изменения сохранены, блокировка снята.

### Полный пример

```python
import asyncio

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import AttributeValues


async def main() -> None:
    config = IPSConfig()
    async with IPSClient(config=config) as ips:
        # 1. Черновик объекта типа 1116 ("Комментарий") — временный отрицательный id.
        draft = await ips.object_create(1116)
        # 2. Фиксация создания -> постоянный положительный id.
        object_id = await ips.object_commit_creation(draft.object_id)
        print("Создан объект:", object_id)

        # 3. Извлекаем на редактирование -> id РАБОЧЕЙ КОПИИ.
        working_id = await ips.object_check_out(object_id)

        # 4. Запись атрибутов идёт по id рабочей копии (НЕ по object_id!).
        #    attribute_id=10 — например, "Наименование".
        await ips.object_set_attribute_values(
            working_id,
            [AttributeValues(attribute_id=10, values=["Привет из aioips"])],
        )

        # 5. Фиксируем изменения.
        await ips.object_check_in(working_id)
        print("Атрибут записан и зафиксирован")


if __name__ == "__main__":
    asyncio.run(main())
```

!!! warning "Тип 1116 «Комментарий» — удобный одноразовый объект"
    Тип 1116 создаётся без обязательного родителя (root-creatable), поэтому он идеален для
    экспериментов. Для «настоящих» типов с ограничением применяемости при фиксации нужно указать
    родителя через `related_object_ids` (см. ниже), иначе будет ошибка.

!!! warning "Без commit_creation объекта нет"
    После `object_create` объект существует только как черновик с отрицательным id. Если не вызвать
    `object_commit_creation`, он не сохранится. При ошибке фиксации черновик удаляется автоматически
    (параметр `delete_on_exception=True` по умолчанию) — мусор не остаётся.

### Если тип требует родителя

Некоторые типы обязаны входить в состав родительского объекта. Тогда id родителей передаётся при
фиксации:

```python
draft = await ips.object_create(некоторый_тип)
object_id = await ips.object_commit_creation(
    draft.object_id,
    related_object_ids=[id_родителя],  # иначе сервер вернёт ошибку применяемости
)
```

---

## Задача 2. Изменить атрибуты существующего объекта

**Когда нужно:** объект уже есть в базе, надо обновить его значения.

### Решение

1. **Извлечь на редактирование** — `object_check_out(object_id)` → id рабочей копии.
2. **Записать значения** — `object_set_attribute_values(working_id, [...])`.
3. **Зафиксировать** — `object_check_in(working_id)`. Либо **откатить** —
   `object_cancel_changes([object_id], confirm=True)`.

### Полный пример

```python
from aioips.schemas.objects import AttributeValues

async with IPSClient(config=config) as ips:
    working_id = await ips.object_check_out(102550)
    try:
        await ips.object_set_attribute_values(
            working_id,
            [AttributeValues(attribute_id=9, values=["550.07.305"])],
        )
        await ips.object_check_in(working_id)
    except Exception:
        # Откат: восстановить состояние до checkout. Передаём id ОБЪЕКТА, не рабочей копии.
        await ips.object_cancel_changes([102550], confirm=True)
        raise
```

!!! tip "cancelChanges — безопасный способ тестировать запись"
    Цикл `check_out → set → cancel_changes` **полностью обратим**: ничего не меняется насовсем.
    Это удобный способ проверить, что запись «доходит», не создавая и не удаляя объекты.

!!! warning "cancel_changes принимает id объекта и требует confirm"
    `object_cancel_changes` откатывает несохранённые правки **безвозвратно**, поэтому требует
    `confirm=True` (иначе `ValueError` ещё до запроса). Передавайте список **id объектов**
    (`F_OBJECT_ID`), а не id рабочих копий.

---

## Задача 3. Удалить объект (и подчистить мусор после экспериментов)

**Когда нужно:** убрать объект из базы. Операция **необратима**.

### Решение

1. Вызовите `object_delete(object_id, confirm=True)`. Без `confirm=True` метод поднимет `ValueError`
   и не сделает запрос.
2. Код результата `0` означает успех.

### Полный пример

```python
async with IPSClient(config=config) as ips:
    code = await ips.object_delete(102550, confirm=True)
    assert code == 0  # 0 — успех
```

!!! danger "После экспериментов удаляйте мусорные объекты"
    Если вы создавали одноразовые объекты (например, тип 1116) для тестов записи — **обязательно
    удаляйте их** через `object_delete(..., confirm=True)`. Не оставляйте мусор в боевой базе.

!!! warning "confirm=True — обязателен для разрушающих операций"
    `object_delete`, `object_cancel_changes`, `relation_delete` и другие необратимые методы защищены
    гейтом: без `confirm=True` они поднимают `ValueError` и **не обращаются к серверу**. Это
    осознанная защита от случайного удаления.

---

## Полный сквозной пример: создать → изменить → удалить

Этот пример показывает весь жизненный цикл одноразового объекта и чистит за собой. Именно так
безопасно проверять запись на боевом сервере.

```python
import asyncio

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import AttributeValues


async def main() -> None:
    config = IPSConfig()
    async with IPSClient(config=config) as ips:
        # --- СОЗДАТЬ ---
        draft = await ips.object_create(1116)              # тип "Комментарий"
        object_id = await ips.object_commit_creation(draft.object_id)

        # --- ИЗМЕНИТЬ ---
        working_id = await ips.object_check_out(object_id)  # id рабочей копии!
        await ips.object_set_attribute_values(
            working_id,
            [AttributeValues(attribute_id=10, values=["временный тест"])],
        )
        await ips.object_check_in(working_id)

        # --- ПРОВЕРИТЬ ---
        text = await ips.object_attribute_as_string(object_id, 10)
        print("Записано:", text)

        # --- УДАЛИТЬ (подчистить мусор) ---
        await ips.object_delete(object_id, confirm=True)
        assert await ips.object_get(object_id) is None  # объекта больше нет


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Частые ошибки

!!! warning "400: «нужна рабочая копия»"
    Вы вызвали метод записи на id исходного объекта, а не на id рабочей копии из `object_check_out`.
    Используйте `working_id`.

!!! warning "409 / конфликт ЖЦ при записи"
    Объект не извлечён на редактирование, или текущий шаг жизненного цикла не разрешает правку, или
    атрибут помечен `read_only`. Сначала `object_check_out`, проверьте права и шаг ЖЦ. Подробнее —
    [Обработка ошибок](error-handling.md).

!!! tip "Альтернативы методов записи"
    - `object_set_attribute_values(working_id, [AttributeValues(...)])` — точечная запись значений по
      id типа атрибута (основной способ).
    - `object_set_attributes(working_id, [Attribute(...)])` — запись готовыми DTO `Attribute` (как их
      возвращает `object_attributes`), удобно для переноса атрибутов между объектами.

## Что дальше

- [Обработка ошибок и повторы](error-handling.md) — как реагировать на 400/409 при записи.
- [Связи и состав](relations.md) — как включить объект в состав другого (тоже требует checkout родителя).
- [Чтение объектов](reading-objects.md) — как проверить результат записи.
