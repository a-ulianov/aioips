# Архитектура

`aioips` — это **асинхронная клиент-библиотека** (обёртка) над IPS Server Web API. Она не содержит
бизнес-логики сервера; её задача — дать удобный типизированный Python-интерфейс поверх HTTP-эндпоинтов
IPS: вызвал `await ips.<метод>(...)` — получил готовую pydantic-схему. Архитектура подчинена двум
целям: **масштабироваться на сотни эндпоинтов** (744 операции в IPS) и оставаться предсказуемой.

## Слои клиента

Каждый модуль отвечает за что-то одно. Запрос проходит сверху вниз: метод-раздел → ядро → авторизация
и сессия → сервер, а на обратном пути сырой JSON превращается в pydantic-схему.

```text
src/aioips/
├── __init__.py            # публичный экспорт: IPSClient, IPSConfig, исключения
├── client.py              # сборка IPSClient множественным наследованием mixin'ов
├── py.typed               # маркер типизированного пакета (PEP 561)
├── core/                  # ЯДРО клиента (общее поведение для всех методов)
│   ├── config.py          #   IPSConfig(BaseSettings): env-prefix IPS_, таймауты, ретраи
│   ├── exceptions.py      #   иерархия IPSError → 401/403/404/409/429/500
│   ├── sessions.py        #   SessionManager: управление aiohttp.ClientSession
│   ├── auth.py            #   AuthManager: жизненный цикл JWT (authenticate/refresh/401)
│   └── core.py            #   APIManager: единый _request() (ретраи, refresh, ошибки, multipart)
├── methods/               # ПУБЛИЧНЫЕ методы-обёртки, сгруппированы по разделам
│   ├── objects/
│   │   ├── object_get.py          # один метод = один файл = один mixin
│   │   ├── object_create.py
│   │   └── ...                     # (57 файлов в разделе objects)
│   ├── metadata/                   # (203 метода)
│   ├── relations/                  # (24 метода)
│   └── ...                         # (всего 42 раздела)
├── schemas/               # pydantic v2 DTO запросов/ответов (парные методам)
│   ├── objects/
│   │   ├── object.py               # ObjectDto и связанные модели
│   │   └── ...
│   └── ...
├── common/
│   └── enumerations/      # доменные enum'ы (FieldType, MultiValueMode, …), сверены со swagger
└── infrastructure/
    └── logging/           # структурное логирование (get_logger)
```

Карта потока запроса (из [`vault/architecture/layers.md`](https://github.com/) проекта):

```text
IPSClient (client.py)
  └─ mixin-разделы (methods/<раздел>/<метод>.py)   ← публичные методы, возвращают схемы
       └─ APIManager._request (core/core.py)        ← авторизация + повторы + ошибки
            ├─ AuthManager (core/auth.py)           ← JWT: authenticate / refresh / 401
            ├─ SessionManager (core/sessions.py)    ← aiohttp.ClientSession
            └─ exceptions (core/exceptions.py)      ← маппинг HTTP-кода в исключение
  schemas/<раздел>/<метод>.py                       ← pydantic-модели (camelCase-алиасы)
  common/enumerations/                              ← доменные enum'ы
```

## Паттерн «метод = файл = mixin»

Главное архитектурное решение ([ADR-0001](#)): **один метод API = один файл = один mixin-класс**,
плюс парный файл схемы. Добавление нового метода — это 3 маленьких файла (метод, схема, тест) и одна
строка в `__init__` раздела. Структура плоская и предсказуемая, её легко генерировать и ревьюить.

Реальный пример — файл `methods/objects/object_get.py`:

```python
"""Метод получения версии объекта по идентификатору."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectGetMixin(APIManager):
    """Реализует метод GET /core/api/objects/{objectId} (Objects_GetObject)."""

    async def object_get(
        self: "ObjectGetMixin",
        object_id: int,
        *,
        throw_not_found: bool = False,
    ) -> ObjectDto | None:
        """Возвращает полное описание объекта по идентификатору ОБЪЕКТА."""
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request("get", f"/core/api/objects/{object_id}", params=params)
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectDto.model_validate(entity) if entity is not None else None
```

Обратите внимание на три типичные детали:

- mixin наследуется от `APIManager` и вызывает защищённый `self._request(...)` — весь транспорт там;
- метод **разворачивает** result-обёртку IPS `{entity, isEntityPresent}` в `ObjectDto | None`, не
  протекая деталь транспорта наружу (см. [Общие принципы](reference/index.md));
- возвращается типизированная схема, а не `dict`.

## Сборка `IPSClient`

Все mixin-разделы собираются в один класс множественным наследованием. Имена методов глобально
уникальны (каждый уже несёт контекст раздела: `object_*`, `attribute_*`), поэтому конфликтов нет.
Файл `client.py`:

```python
from .methods import (
    AuthAPI, MetadataAPI, ObjectsAPI, RelationsAPI, UsersAPI,
    # ... всего 42 раздела
)


class IPSClient(
    AuthAPI,
    MetadataAPI,
    ObjectsAPI,
    RelationsAPI,
    UsersAPI,
    # ... все 37 mixin-разделов
):
    """Основной асинхронный клиент IPS Server Web API."""
```

Использование — как асинхронный контекстный менеджер, чтобы гарантированно закрыть HTTP-сессию:

```python
import asyncio
from aioips import IPSClient, IPSConfig


async def main() -> None:
    config = IPSConfig(
        base_url="http://your-ips-host:8080",
        login_name="your-login",
        password="...",          # из окружения IPS_*, не из кода
        role_name="Администратор",
    )
    async with IPSClient(config=config) as ips:
        me = await ips.user_info()
        types = await ips.object_types()
        print(me.login_name, len(types))


asyncio.run(main())
```

## Ядро: `APIManager._request`

Всё общее поведение HTTP живёт в `core/core.py` в одном защищённом методе `_request`, которым
пользуются все 723 метода-обёртки. Что он берёт на себя:

- **Авторизация.** Перед каждым запросом `AuthManager.ensure_access_token()` гарантирует свежий
  JWT-токен (получает его через `/authenticate` или обновляет через `/refreshTokens`).
- **Обновление по 401.** Если сервер вернул `401`, ядро **один раз** принудительно обновляет токен
  (`force_refresh`) и повторяет запрос. Это покрывает истечение токена между вызовами.
- **Повторы транзиентных ошибок.** Через `tenacity` повторяются ошибки `5xx`, `429` и сетевые
  (`IPSConnectionError`, таймаут) с экспоненциальной задержкой; число попыток и границы задержки —
  из `IPSConfig`. Повтор делается с `reraise=True` — после исчерпания попыток поднимается исходное
  исключение.
- **Маппинг ошибок.** При статусе `>= 400` тело ответа (`ApiProblemDetails` IPS) преобразуется в
  типизированное исключение через `exception_from_response`: `IPSAuthError` (401),
  `IPSClientError` (400), `IPSForbiddenError` (403), `IPSNotFoundError` (404),
  `IPSConflictError` (409), `IPSTooManyRequestsError` (429), `IPSServerError` (500). Ошибки не
  глотаются (fail-closed).
- **Multipart для файлов.** Для загрузки файлов передаётся спецификация полей `multipart`; форма
  `aiohttp.FormData` **пересобирается на каждой попытке**, поэтому повтор безопасен — байты полей
  читаются из памяти и не «расходуются» предыдущей попыткой. При наличии `multipart` параметр `json`
  игнорируется.

Псевдокод одной попытки (`_attempt` внутри `_request`):

```python
token = await self._auth.ensure_access_token()
status, data = await self._raw_request(method, path, json, params=params, token=token, ...)

if status == 401:                       # токен истёк между вызовами
    token = await self._auth.force_refresh()
    status, data = await self._raw_request(..., token=token, ...)

if status >= 400:                       # маппинг тела ошибки в исключение
    raise exception_from_response(status, data if isinstance(data, dict) else None)

return data                             # сырой dict/list — метод-обёртка валидирует в схему
```

Такое разделение даёт тонкие, легко тестируемые методы-обёртки (только путь, параметры и разбор
схемы) и единое, проверенное место для всей логики транспорта.

## Принципы, которым подчинена архитектура

- **Async-first для I/O:** `async def`, `async with`, `aiohttp`, `tenacity`; никаких синхронных
  блокирующих вызовов в async-коде.
- **Pydantic v2 везде:** схемы запросов/ответов и конфиг; алиасы `snake_case` ↔ `camelCase` через
  `pydantic.alias_generators.to_camel`.
- **Одна сессия на экземпляр клиента:** авторизация IPS — это per-session JWT, общий пул соединений
  не даёт выгоды и усложняет код (KISS).
- **Тонкие обёртки над HTTP:** вся доменная логика преобразований — в схемах и методах, транспорт —
  в ядре. DI через конструктор, конфиг — `pydantic-settings` с env-prefix `IPS_`.

Подробнее о доменной модели (объект vs версия, состав, жизненный цикл) — в разделе
[Концепции](concepts/index.md). Полный перечень методов — в [Справочнике API](reference/index.md).
