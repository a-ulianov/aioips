# Файлы

Это руководство — про работу с файлами объектов: как узнать, какие файлы прикреплены, как скачать
содержимое, как загрузить новый файл во временное хранилище и прикрепить его к атрибуту объекта.

!!! tip "Как устроены файлы в IPS"
    Файлы — это значения атрибутов типа `ftFile`. Само содержимое хранится во внешнем файловом
    хранилище (vault), а через API мы получаем метаданные (имя, размер, `blob_id`) и можем скачать
    содержимое. Прикрепление нового файла — двухшаговое: сначала загрузка во временное хранилище,
    потом привязка к атрибуту объекта (в режиме редактирования).

## Карта методов

| Метод | Что делает |
|---|---|
| `file_attributes(object_id)` | Возвращает файловые атрибуты объекта и метаданные файлов (`blob_id`, имя, размер) |
| `object_file_by_name(object_id, file_name)` | Скачивает содержимое файла по имени |
| `object_file_by_blob_id(object_id, blob_id)` | Скачивает содержимое файла по `blob_id` (однозначно) |
| `upload_temp_file(file_data, file_name)` | Загружает файл во временное хранилище → временное имя |
| `attach_temp_files(object_id, [...])` | Прикрепляет временные файлы к файловым атрибутам объекта |
| `delete_temp_file(temp_file_name)` | Удаляет временный файл из временного хранилища |
| `file_unique_name(file_name=...)` / `file_id_by_name(...)` / `next_file_id()` / `object_ids_by_file_name(...)` | Сервис имён файлов |

---

## Задача 1. Узнать, какие файлы есть у объекта

**Когда нужно:** перед скачиванием — выяснить состав файлов объекта и их `blob_id`.

### Решение

1. Вызовите `file_attributes(object_id)` (передайте **id объекта**).
2. Пройдитесь по `obj.attributes` (файловые атрибуты), а внутри — по `attr.file_info_collection`
   (метаданные файлов). У каждого файла есть `file_name` и `blob_id`.

### Полный пример

```python
import asyncio

from aioips import IPSClient, IPSConfig


async def main() -> None:
    config = IPSConfig()
    async with IPSClient(config=config) as ips:
        obj = await ips.file_attributes(102550)  # 102550 = id объекта
        for attr in obj.attributes:
            for info in attr.file_info_collection:
                print(attr.attribute_id, info.file_name, info.blob_id)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Задача 2. Скачать содержимое файла

**Когда нужно:** получить сам файл. Есть два способа — по имени и по `blob_id`.

### Решение

- По имени: `object_file_by_name(object_id, file_name)` — удобно, когда знаете имя.
- По `blob_id`: `object_file_by_blob_id(object_id, blob_id)` — **однозначно**, когда у объекта есть
  несколько файлов с одинаковым именем.

### Полный пример

```python
async with IPSClient(config=config) as ips:
    # Узнаём blob_id из метаданных...
    obj = await ips.file_attributes(102550)
    info = obj.attributes[0].file_info_collection[0]

    # ...и качаем по нему (надёжнее, чем по имени).
    content = await ips.object_file_by_blob_id(102550, info.blob_id)

    # Или по имени, если оно уникально:
    content_by_name = await ips.object_file_by_name(102550, info.file_name)
```

!!! warning "Содержимое возвращается строкой"
    В swagger тело файла описано как `string` (`format: binary`). Метод отдаёт строку; для двоичных
    файлов это сырое содержимое, которое при необходимости кодируйте в байты на своей стороне. Имя
    файла URL-кодируется автоматически — передавайте его как есть.

!!! tip "По имени — неоднозначно при дубликатах"
    Если у объекта несколько файлов с одинаковым именем, `object_file_by_name` неоднозначен.
    Предпочитайте `object_file_by_blob_id`.

---

## Задача 3. Загрузить файл и прикрепить его к объекту

**Когда нужно:** добавить новый файл в файловый атрибут объекта.

### Решение (двухшаговое прикрепление)

1. **Загрузить во временное хранилище** — `upload_temp_file(file_data, file_name)`. Вернётся
   **временное имя** файла на сервере.
2. **Извлечь объект на редактирование** — `object_check_out(object_id)` (прикрепление — это запись,
   требуется checkout; см. [Редактирование объектов](editing-objects.md)).
3. **Прикрепить** — `attach_temp_files(object_id, [AttachTempFile(...)])`, указав id файлового
   атрибута и временное имя из шага 1.
4. **Зафиксировать** — `object_check_in(working_id)`.
5. Если файл так и не прикрепили — **удалить временный** через `delete_temp_file(temp_name)`, чтобы не
   оставлять мусор.

### Полный пример

```python
from aioips.schemas.files import AttachTempFile

async with IPSClient(config=config) as ips:
    # 1. Загрузка во временное хранилище -> временное имя.
    temp_name = await ips.upload_temp_file(b"...содержимое PDF...", "schema.pdf")
    try:
        # 2. Извлекаем объект на редактирование.
        working_id = await ips.object_check_out(102550)

        # 3. Прикрепляем временный файл к файловому атрибуту (например, 12).
        await ips.attach_temp_files(
            102550,
            [
                AttachTempFile(
                    attribute_id=12,
                    temp_file_name=temp_name,
                    file_type="ftNormal",
                    modify_date_time="2026-06-24T10:00:00",
                    real_file_size=1024,
                )
            ],
        )

        # 4. Фиксируем.
        await ips.object_check_in(working_id)
    finally:
        # 5. Подчищаем временный файл в любом случае.
        await ips.delete_temp_file(temp_name)
```

!!! warning "Прикрепление требует checkout"
    `attach_temp_files` — операция записи. Объект должен быть извлечён на редактирование, иначе будет
    конфликт жизненного цикла (409). Метод сам checkout не делает.

!!! tip "Всегда удаляйте неприкреплённые временные файлы"
    Если по какой-то причине прикрепление не состоялось, вызывайте `delete_temp_file(temp_name)`
    (удобно в блоке `finally`), чтобы не копить мусор во временном хранилище.

---

## Задача 4. Сервис имён файлов

**Когда нужно:** низкоуровневые операции с именами/идентификаторами файлов — например, получить
уникальное имя перед загрузкой или найти объекты по имени файла.

### Что есть

| Метод | Зачем |
|---|---|
| `file_unique_name(file_name="schema.pdf")` | Получить уникальное имя (сервер при коллизии изменит, например `schema(1).pdf`) |
| `file_id_by_name(file_name="schema.pdf")` | Получить id файла по имени (`-1`/`0` — не найдено) |
| `object_ids_by_file_name(file_name="schema.pdf")` | Найти **id объектов**, которым принадлежит файл |
| `next_file_id()` | Получить следующий свободный id файла |

### Полный пример

```python
async with IPSClient(config=config) as ips:
    unique = await ips.file_unique_name(file_name="schema.pdf")
    owners = await ips.object_ids_by_file_name(file_name="schema.pdf")
    print("Уникальное имя:", unique)
    print("Объекты с этим файлом:", owners)  # это id ОБЪЕКТОВ, можно подать в object_get
```

!!! warning "id файла ≠ id объекта"
    `file_id_by_name` и `next_file_id` работают в **отдельном id-пространстве файлов** — это не id
    объектов и не id версий. А вот `object_ids_by_file_name` возвращает именно id **объектов**
    (`F_OBJECT_ID`), которые можно передавать в [`object_get`](reading-objects.md).

## Что дальше

- Прикрепление — частный случай записи; общий цикл — в [Редактировании объектов](editing-objects.md).
- Не знаете id объекта с нужным файлом? [Найдите его](searching.md) или используйте
  `object_ids_by_file_name`.
