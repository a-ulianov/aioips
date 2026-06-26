# aioips

[![PyPI](https://img.shields.io/pypi/v/aioips.svg)](https://pypi.org/project/aioips/)
[![Python](https://img.shields.io/pypi/pyversions/aioips.svg)](https://pypi.org/project/aioips/)
[![CI](https://github.com/a-ulianov/aioips/actions/workflows/ci.yml/badge.svg)](https://github.com/a-ulianov/aioips/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-2a6db2.svg)](https://mypy-lang.org/)

Асинхронный pydantic-клиент для **IPS Server Web API** (Intermech Professional Solutions).

`aioips` даёт удобный `async/await`-интерфейс к REST API системы IPS: авторизацию по JWT
с автоматическим обновлением токена, типизированные pydantic-схемы запросов и ответов,
повторы при транзиентных ошибках и понятную иерархию исключений.

> Стабильный релиз **1.0.0** ([семантическое версионирование](https://semver.org/lang/ru/)). Ядро
> (авторизация, запросы, повторы, обработка ошибок, multipart, потоковые загрузки, хуки
> наблюдаемости) и **723 метода в 42 разделах** реализованы и прод-проверены — покрыта практически
> вся прикладная поверхность IPS Web API (чтение, запись объектов/связей/файлов, права доступа,
> метаданные, бинарные загрузки).

## Возможности

- **Async-first** на базе `aiohttp`.
- **Два способа авторизации:** логин/пароль (клиент сам получает и обновляет JWT) или готовый access-токен.
- **Автоматическое обновление токена** и повтор запроса при ответе `401`.
- **Повторы транзиентных ошибок** (5xx, 429, сетевые) с экспоненциальной задержкой (`tenacity`).
- **Типизированные схемы** (pydantic v2) с маппингом `snake_case` ↔ `camelCase`.
- **Строгая типизация** (`mypy --strict`) и документация на русском в каждом публичном API.

## Установка

Требуется Python **3.13+**.

```bash
pip install aioips
```

Для разработки — из исходников:

```bash
git clone https://github.com/a-ulianov/aioips.git
cd aioips
python -m venv .venv
. .venv/Scripts/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Конфигурация

Параметры задаются аргументами конструктора, переменными окружения или файлом `.env`
(префикс `IPS_`). См. [`.env.example`](.env.example).

| Параметр | Env | Назначение |
|---|---|---|
| `base_url` | `IPS_BASE_URL` | URL сервера IPS Web API, например `http://your-ips-host:8080` |
| `login_name` | `IPS_LOGIN_NAME` | Имя пользователя IPS |
| `password` | `IPS_PASSWORD` | Пароль пользователя IPS |
| `role_name` | `IPS_ROLE_NAME` | Имя роли (резолвится в идентификатор автоматически) |
| `role_id` | `IPS_ROLE_ID` | Идентификатор роли (если известен) |
| `access_level_id` | `IPS_ACCESS_LEVEL_ID` | Уровень доступа (0 — обычный) |
| `access_token` | `IPS_ACCESS_TOKEN` | Готовый JWT-токен (вместо логина/пароля) |

> ⚠️ Реальные адреса серверов, логины и пароли держите только в `.env` (он в `.gitignore`)
> или в переменных окружения. Никогда не коммитьте их в репозиторий.

## Быстрый старт

```python
import asyncio

from aioips import IPSClient, IPSConfig


async def main() -> None:
    config = IPSConfig(
        base_url="http://your-ips-host:8080",
        login_name="your-login",
        password="...",          # лучше — через переменную окружения IPS_PASSWORD
        role_name="Администратор",
    )
    async with IPSClient(config=config) as ips:
        me = await ips.user_info()
        print(me.login_name, me.is_admin)

        types = await ips.object_types()
        print("Типов объектов:", len(types))


if __name__ == "__main__":
    asyncio.run(main())
```

Если параметры заданы в окружении/`.env`, конфигурацию можно создать без аргументов:
`config = IPSConfig()`.

## Авторизация

Клиент скрывает двухшаговую схему IPS:

1. `GET /core/api/Auth/logins/{loginName}/options` — доступные роли и уровни доступа (без пароля).
2. `POST /core/api/Auth/authenticate` — обмен логина/пароля на пару токенов.
3. `POST /core/api/Auth/refreshTokens` — обновление пары токенов.

Получить токен и обновлять его не нужно вручную — это делает ядро при первом запросе и при
получении ответа `401`. Доступные роли можно посмотреть заранее:

```python
options = await ips.login_options("your-login")
print({role.name: role.id for role in options.roles})
```

## Документация

Полная многостраничная документация — в каталоге [`docs/`](docs/) (рендерится на GitHub) и как
сайт **MkDocs Material** (GitHub Pages, собирается из `docs/` через CI):

- [**Начало работы**](docs/getting-started/index.md) — установка, конфигурация, первый запрос, авторизация
- [**Концепции IPS**](docs/concepts/index.md) — модель данных (объект/версия), атрибуты, жизненный цикл, связи, поиск
- [**Руководства**](docs/guides/index.md) — пошаговые сценарии: чтение, редактирование, поиск, файлы, связи, ошибки
- [**Справочник API**](docs/reference/index.md) — все методы по разделам
- [**Архитектура**](docs/architecture.md) · [**Участие в разработке**](docs/contributing.md)

Локальный предпросмотр сайта: `pip install -e ".[docs]" && mkdocs serve`.

## Реализованные методы

Клиент покрывает **723 методов** в **42 разделах** IPS Server Web API. Каждый метод снабжён MCP-grade docstring и (где применимо) прод-проверен на боевом сервере.

Имена выводятся из адреса эндпоинта ([ADR-0003](vault/architecture/ADR-0003-naming-convention.md)); разрушающие операции защищены гейтом `confirm=True`. Полный плоский список — [docs/reference/all-methods.md](docs/reference/all-methods.md). Разделы свёрнуты:

<details>
<summary><b><code>metadata</code></b> — Метамодель: типы/атрибуты/связи, применяемость, ЖЦ, дерево типов <b>(225)</b></summary>

| Метод | Назначение |
|---|---|
| `all_attributes_for_object_type_list(attribute_type_id)` | Возвращает все привязки заданного атрибута ко всем типам объектов |
| `all_attributes_for_object_type_list_by_guid(attribute_type_guid)` | Возвращает все привязки атрибута ко всем типам объектов по GUID атрибута |
| `all_attributes_for_relation_type_list(attribute_type_id)` | Возвращает все привязки заданного атрибута ко всем типам связей |
| `all_attributes_for_relation_type_list_by_guid(attribute_type_guid)` | Возвращает все привязки атрибута ко всем типам связей по GUID атрибута |
| `applicabilities()` | Возвращает ВСЕ настроенные в базе правила применяемости |
| `applicability(parent_object_type_id, child_object_type_id, relation_type_id)` | Возвращает правило применяемости для конкретной тройки родитель/потомок/связь |
| `applicability_child_object_type_guids(parent_object_type_id, relation_type_id)` | Возвращает GUID дочерних типов, допустимых в составе родителя по одной связи |
| `applicability_child_object_type_guids_by_guids(parent_object_type_guid, relation_type_guid)` | Возвращает GUID дочерних типов состава по GUID родителя и GUID типа связи |
| `applicability_child_object_type_guids_by_parent_guid_relation_guids(parent_object_type_guid, relation_type_guids)` | Возвращает GUID дочерних типов состава по GUID родителя и набору GUID связей |
| `applicability_child_object_type_guids_by_parent_id_relation_ids(parent_object_type_id, relation_type_ids)` | Возвращает GUID дочерних типов состава по id родителя и набору id связей |
| `applicability_child_object_type_ids(parent_object_type_id, relation_type_id)` | Возвращает id дочерних типов, допустимых в составе родителя по одной связи |
| `applicability_child_object_type_ids_by_guids(parent_object_type_guid, relation_type_guid)` | Возвращает id дочерних типов состава по GUID родителя и GUID типа связи |
| `applicability_child_object_type_ids_by_parent_guid_relation_guids(parent_object_type_guid, relation_type_guids)` | Возвращает id дочерних типов состава по GUID родителя и набору GUID связей |
| `applicability_child_object_types(parent_object_type_id, relation_type_id)` | Возвращает полные описания дочерних типов, допустимых в составе по одной связи |
| `applicability_child_object_types_by_guids(parent_object_type_guid, relation_type_guid)` | Возвращает описания дочерних типов, допустимых в составе, по GUID родителя и связи |
| `applicability_relation_type_guids(object_type_id)` | Возвращает GUID типов связей, участвующих в применяемостях данного типа объекта |
| `applicability_relation_type_guids_by_guid(object_type_guid)` | Возвращает GUID типов связей применяемости типа объекта, адресованного по GUID |
| `applicability_relation_type_ids(object_type_id)` | Возвращает id типов связей, участвующих в применяемостях данного типа объекта |
| `applicability_relation_type_ids_by_guid(object_type_guid)` | Возвращает id типов связей применяемости типа объекта, адресованного по GUID |
| `attribute_for_object_type(object_type_id, attribute_type_id)` | Возвращает настройку применения одного атрибута к одному типу объекта |
| `attribute_for_object_type_by_guids(object_type_guid, attribute_type_guid)` | Возвращает настройку применения атрибута к типу объекта по паре GUID |
| `attribute_for_object_type_list(object_type_id)` | Возвращает список типов атрибутов, применимых к заданному типу объекта |
| `attribute_for_object_type_list_by_guid(object_type_guid)` | Возвращает список атрибутов, применимых к типу объекта, по его GUID |
| `attribute_for_relation_type(relation_type_id, attribute_type_id)` | Возвращает настройку применения одного атрибута к одному типу связи |
| `attribute_for_relation_type_by_guids(relation_type_guid, attribute_type_guid)` | Возвращает настройку применения атрибута к типу связи по паре GUID |
| `attribute_for_relation_type_list(relation_type_id)` | Возвращает список типов атрибутов, применимых к заданному типу связи |
| `attribute_for_relation_type_list_by_guid(relation_type_guid)` | Возвращает список атрибутов, применимых к типу связи, по его GUID |
| `attribute_group(attribute_group_id)` | Возвращает описание группы атрибутов по её идентификатору |
| `attribute_group_by_guid(guid)` | Возвращает описание группы атрибутов по её GUID |
| `attribute_group_guid(attribute_group_id)` | Возвращает GUID группы атрибутов по её идентификатору |
| `attribute_group_id_by_guid(guid)` | Возвращает идентификатор группы атрибутов по её GUID |
| `attribute_has_possible_values(attribute_type_id)` | Проверяет, задан ли у типа атрибута список допустимых значений (по id) |
| `attribute_has_possible_values_by_guid(guid)` | Проверяет, задан ли у типа атрибута список допустимых значений (по GUID) |
| `attribute_has_system_data(attribute_type_id)` | Проверяет, несёт ли тип атрибута системные данные (по id) |
| `attribute_has_system_data_by_guid(guid)` | Проверяет, несёт ли тип атрибута системные данные (по GUID) |
| `attribute_is_gridable(attribute_type_id)` | Проверяет, можно ли выводить тип атрибута колонкой таблицы (по id) |
| `attribute_is_gridable_by_guid(guid)` | Проверяет, можно ли выводить тип атрибута колонкой таблицы (по GUID) |
| `attribute_is_in_use(attribute_type_id)` | Проверяет, используется ли тип атрибута где-либо (по id) |
| `attribute_is_in_use_by_guid(guid)` | Проверяет, используется ли тип атрибута где-либо (по GUID) |
| `attribute_linked_object_type_ids(attribute_type_id)` | Возвращает id типов объектов, на которые может ссылаться атрибут-ссылка |
| `attribute_supports_object_links(guid)` | Проверяет, поддерживает ли системный тип атрибута ссылки на объекты (по GUID) |
| `attribute_type(attribute_type_id)` | Возвращает описание типа атрибута по его идентификатору |
| `attribute_type_applicability(attribute_type_id)` | Возвращает категорию применимости типа атрибута по его идентификатору |
| `attribute_type_applicability_by_guid(guid)` | Возвращает категорию применимости типа атрибута по его GUID |
| `attribute_type_by_guid(guid)` | Возвращает описание типа атрибута по его глобальному идентификатору (GUID) |
| `attribute_type_exists(attribute_type_id)` | Проверяет существование типа атрибута по его идентификатору |
| `attribute_type_exists_by_guid(guid)` | Проверяет существование типа атрибута по его GUID |
| `attribute_type_guid(attribute_type_id)` | Возвращает GUID типа атрибута по его идентификатору |
| `attribute_type_guid_by_name(attribute_name)` | Возвращает GUID типа атрибута по его имени |
| `attribute_type_guids()` | Возвращает список GUID всех типов атрибутов метаданных |
| `attribute_type_id_by_guid(guid)` | Возвращает идентификатор типа атрибута по его GUID |
| `attribute_type_id_by_name(attribute_name)` | Возвращает идентификатор типа атрибута по его имени |
| `attribute_type_ids()` | Возвращает список идентификаторов всех типов атрибутов метаданных |
| `attribute_type_name(attribute_type_id)` | Возвращает имя типа атрибута по его идентификатору |
| `attribute_type_name_by_guid(guid)` | Возвращает имя типа атрибута по его GUID |
| `attribute_types()` | Возвращает список всех типов атрибутов, определённых в метаданных IPS |
| `attributes_in_group_guids(attribute_group_id)` | Возвращает GUID типов атрибутов, входящих в группу (по id группы) |
| `attributes_in_group_guids_by_guid(guid)` | Возвращает GUID типов атрибутов, входящих в группу (по GUID группы) |
| `attributes_in_group_ids(attribute_group_id)` | Возвращает id типов атрибутов, входящих в группу (по id группы) |
| `attributes_in_group_ids_by_guid(guid)` | Возвращает id типов атрибутов, входящих в группу (по GUID группы) |
| `can_add_object_type_to_editing_context(object_type_id)` | Проверяет, можно ли добавить тип объекта в контекст редактирования (по id) |
| `can_add_object_type_to_editing_context_by_guid(object_type_guid)` | Проверяет, можно ли добавить тип объекта в контекст редактирования (по GUID) |
| `can_enters_in(part_type_id)` | Проверяет, может ли объект данного типа входить в чей-либо состав |
| `child_object_type_ids(parent_object_type_id, relation_type_ids)` | Возвращает id дочерних типов, допустимых в составе родителя по заданным связям |
| `children_type_guids(parent_type_id)` | Возвращает GUID ПРЯМЫХ дочерних типов объектов в иерархии типов |
| `children_type_guids_by_guid(parent_type_guid)` | Возвращает GUID ПРЯМЫХ дочерних типов объектов по GUID родительского типа |
| `children_type_guids_recursive(parent_type_id)` | Возвращает GUID ВСЕХ потомков типа объекта рекурсивно (всё поддерево) |
| `children_type_guids_recursive_by_guid(parent_type_guid)` | Возвращает GUID ВСЕХ потомков типа рекурсивно по GUID родительского типа |
| `children_type_ids(parent_type_id)` | Возвращает id ПРЯМЫХ дочерних типов объектов в иерархии типов |
| `children_type_ids_by_guid(parent_type_guid)` | Возвращает id ПРЯМЫХ дочерних типов объектов по GUID родительского типа |
| `children_type_ids_recursive(parent_type_id)` | Возвращает id ВСЕХ потомков типа объекта рекурсивно (всё поддерево) |
| `children_type_ids_recursive_by_guid(parent_type_guid)` | Возвращает id ВСЕХ потомков типа рекурсивно по GUID родительского типа |
| `common_parent_object_type_id_by_ids(object_type_ids)` | Возвращает id ближайшего общего родительского типа для НАБОРА типов по их id |
| `common_parent_object_type_id_by_version_ids(version_ids)` | Возвращает id ближайшего общего родительского типа для объектов по id их версий |
| `common_parent_type_id(child_type1_id, child_type2_id)` | Возвращает id ближайшего ОБЩЕГО предка для пары типов объектов |
| `default_relation_type_guid(parent_object_type_id)` | Возвращает GUID типа связи по умолчанию для заданного типа объекта-родителя |
| `default_relation_type_guid_by_guid(parent_object_type_guid)` | Возвращает GUID типа связи по умолчанию по GUID типа объекта-родителя |
| `default_relation_type_id(parent_object_type_id)` | Возвращает id типа связи по умолчанию для заданного типа объекта-родителя |
| `default_relation_type_id_by_guid(parent_object_type_guid)` | Возвращает id типа связи по умолчанию по GUID типа объекта-родителя |
| `designed_object_type_guids()` | Возвращает GUID типов объектов, имеющих проектируемые типы связей |
| `designed_object_type_ids()` | Возвращает идентификаторы типов объектов, имеющих проектируемые типы связей |
| `displayable_by_guid(guid)` | Возвращает «отображаемое» (человекочитаемое) представление сущности по GUID |
| `editing_context_object_type_guids()` | Возвращает GUID всех типов объектов, входящих в контексты редактирования |
| `editing_context_object_type_ids()` | Возвращает id всех типов объектов, входящих в контексты редактирования |
| `editing_context_top_object_type_guids()` | Возвращает GUID верхнеуровневых (корневых) типов контекста редактирования |
| `editing_context_top_object_type_ids()` | Возвращает id верхнеуровневых (корневых) типов контекста редактирования |
| `globals_by_guid(guid)` | Определяет ВИД сущности метаданных по её GUID |
| `groupable_object_type_guids()` | Возвращает GUID типов объектов, экземпляры которых можно группировать |
| `groupable_object_type_ids()` | Возвращает id типов объектов, экземпляры которых можно группировать |
| `grouping_object_type_guids()` | Возвращает GUID типов объектов, которые ВЫПОЛНЯЮТ группировку |
| `grouping_object_type_ids()` | Возвращает id типов объектов, которые ВЫПОЛНЯЮТ группировку |
| `grouping_relation_type_guids()` | Возвращает GUID типов связей, по которым выполняется группировка |
| `grouping_relation_type_ids()` | Возвращает id типов связей, по которым выполняется группировка |
| `has_applicability(parent_object_type_id)` | Проверяет, может ли объект данного типа иметь состав (хоть одну применяемость) |
| `has_applicability_by_guid(parent_object_type_guid)` | Проверяет, есть ли у типа-родителя (по GUID) хоть одна применяемость |
| `has_applicability_full(parent_object_type_id, child_object_type_id, relation_type_id)` | Проверяет существование применяемости для конкретной тройки родитель/потомок/связь |
| `has_local_object_type(object_type_ids)` | Проверяет, есть ли среди переданных типов хотя бы один ЛОКАЛЬНЫЙ |
| `is_editing_context(id)` | Проверяет, образует ли тип объекта контекст редактирования (по id) |
| `is_editing_context_by_guid(guid)` | Проверяет, образует ли тип объекта контекст редактирования (по GUID) |
| `is_enabled_parent_type(parent_object_type_id, enabled_parent_type_ids, disabled_parent_type_ids, default_value)` | Проверяет, разрешён ли тип объекта как родитель по спискам разрешённых/запрещённых |
| `is_object_type_child(child_type_id, parent_type_id)` | Проверяет, является ли тип потомком другого типа в иерархии (по id обоих) |
| `is_object_type_child_by_child_id_parent_guid(child_type_id, parent_type_guid)` | Проверяет, является ли тип потомком другого: id потомка + GUID родителя |
| `is_object_type_child_by_guids(child_type_guid, parent_type_guid)` | Проверяет, является ли тип потомком другого (оба адресуются по GUID) |
| `is_simple_editing_context(id)` | Проверяет, является ли контекст редактирования типа объекта простым (по id) |
| `life_cycle_level(life_cycle_level_id)` | Возвращает описание уровня жизненного цикла по его идентификатору |
| `life_cycle_level_by_guid(guid)` | Возвращает описание уровня жизненного цикла по его GUID |
| `life_cycle_level_exists(life_cycle_level_id)` | Проверяет, существует ли уровень жизненного цикла с указанным идентификатором |
| `life_cycle_level_exists_by_guid(guid)` | Проверяет, существует ли уровень жизненного цикла с указанным GUID |
| `life_cycle_level_guid(life_cycle_level_id)` | Возвращает GUID уровня жизненного цикла по его числовому идентификатору |
| `life_cycle_level_id_by_guid(guid)` | Возвращает числовой идентификатор уровня жизненного цикла по его GUID |
| `life_cycle_level_name(life_cycle_level_id)` | Возвращает имя уровня жизненного цикла по его идентификатору |
| `life_cycle_level_name_by_guid(guid)` | Возвращает имя уровня жизненного цикла по его GUID |
| `life_cycle_levels()` | Возвращает список всех уровней жизненного цикла, определённых в IPS |
| `life_cycle_scheme(scheme_id)` | Возвращает описание схемы жизненного цикла по её идентификатору |
| `life_cycle_scheme_by_guid(guid)` | Возвращает описание схемы жизненного цикла по её GUID |
| `life_cycle_scheme_exists(scheme_id)` | Проверяет, существует ли схема жизненного цикла с указанным идентификатором |
| `life_cycle_scheme_exists_by_guid(guid)` | Проверяет, существует ли схема жизненного цикла с указанным GUID |
| `life_cycle_scheme_guid(scheme_id)` | Возвращает GUID схемы жизненного цикла по её числовому идентификатору |
| `life_cycle_scheme_id_by_guid(guid)` | Возвращает числовой идентификатор схемы жизненного цикла по её GUID |
| `life_cycle_scheme_name(scheme_id)` | Возвращает имя схемы жизненного цикла по её идентификатору |
| `life_cycle_scheme_name_by_guid(guid)` | Возвращает имя схемы жизненного цикла по её GUID |
| `life_cycle_scheme_steps(scheme_id)` | Возвращает список шагов указанной схемы жизненного цикла |
| `life_cycle_schemes()` | Возвращает список всех схем жизненного цикла, определённых в метаданных IPS |
| `life_cycle_step(life_cycle_step_id)` | Возвращает описание шага (состояния) жизненного цикла по его идентификатору |
| `life_cycle_step_by_guid(guid)` | Возвращает описание шага жизненного цикла по его глобальному GUID |
| `life_cycle_step_exists(life_cycle_step_id)` | Проверяет, существует ли шаг жизненного цикла с указанным идентификатором |
| `life_cycle_step_exists_by_guid(guid)` | Проверяет, существует ли шаг жизненного цикла с указанным GUID |
| `life_cycle_step_guid(life_cycle_step_id)` | Возвращает GUID шага жизненного цикла по его числовому идентификатору |
| `life_cycle_step_id_by_guid(guid)` | Возвращает числовой идентификатор шага жизненного цикла по его GUID |
| `life_cycle_step_name(life_cycle_step_id)` | Возвращает название шага жизненного цикла по его идентификатору |
| `life_cycle_step_name_by_guid(guid)` | Возвращает название шага жизненного цикла по его GUID |
| `life_cycle_steps()` | Возвращает полный список шагов (состояний) жизненного цикла из метаданных |
| `local_children_type_ids_recursive(parent_type_id)` | Возвращает id ЛОКАЛЬНЫХ потомков типа объекта рекурсивно (всё поддерево) |
| `local_object_type_children_ids_recursive_by_ids(object_type_ids)` | Возвращает id ЛОКАЛЬНЫХ потомков рекурсивно для НАБОРА типов по их id |
| `metadata_filters(names)` | Возвращает именованные фильтры метамодели как словарь «имя → список id типов» |
| `metadata_select(request, Any])` | Выполняет SQL-подобную выборку из системной таблицы метаданных IPS |
| `metadata_state(request, Any], partial_fetch_mode)` | Возвращает состояние (срез) метамодели с учётом известных клиенту дат обновления |
| `must_append_object_version(id)` | Проверяет, нужно ли добавлять версию объекта в контекст редактирования (по id) |
| `object_link_attribute_type_ids(object_type_id)` | Возвращает id типов атрибутов-ссылок, которые могут указывать на тип объекта |
| `object_type(object_type_id)` | Возвращает описание типа объекта по его идентификатору |
| `object_type_applicabilities(object_type_id)` | Возвращает правила применяемости для типа объекта как РОДИТЕЛЯ состава |
| `object_type_applicabilities_by_guid(object_type_guid)` | Возвращает правила применяемости типа-РОДИТЕЛЯ, заданного GUID |
| `object_type_by_guid(guid)` | Возвращает описание типа объекта по его глобальному идентификатору (GUID) |
| `object_type_children_guids_recursive_by_guids(object_type_guids)` | Возвращает GUID всех потомков рекурсивно для НАБОРА типов, заданных их GUID |
| `object_type_children_ids_recursive_by_ids(object_type_ids)` | Возвращает id всех потомков рекурсивно для НАБОРА типов, заданных их id |
| `object_type_exists(object_type_id)` | Проверяет, существует ли тип объекта с указанным идентификатором |
| `object_type_exists_by_guid(guid)` | Проверяет, существует ли тип объекта с указанным GUID |
| `object_type_full_name(object_type_id)` | Возвращает полное (иерархическое) имя типа объекта по идентификатору |
| `object_type_guid(object_type_id)` | Возвращает GUID типа объекта по его числовому идентификатору |
| `object_type_has_design(object_type_id)` | Проверяет, есть ли у типа объекта проектируемый тип связи (по идентификатору) |
| `object_type_has_design_by_guid(guid)` | Проверяет, есть ли у типа объекта проектируемый тип связи (по GUID) |
| `object_type_has_grouping(object_type_id)` | Проверяет, выполняет ли тип объекта группировку (по id) |
| `object_type_has_grouping_by_guid(guid)` | Проверяет, выполняет ли тип объекта группировку (по GUID) |
| `object_type_has_sorting(object_type_id)` | Проверяет, поддерживает ли тип объекта сортировку (по id) |
| `object_type_has_sorting_by_guid(guid)` | Проверяет, поддерживает ли тип объекта сортировку (по GUID) |
| `object_type_has_substitution(id)` | Проверяет, есть ли у типа объекта замещающие типы связей (по id) |
| `object_type_has_substitution_by_guid(guid)` | Проверяет, есть ли у типа объекта замещающие типы связей (по GUID) |
| `object_type_has_visibility_attribute(object_type_id)` | Проверяет, есть ли у типа объекта атрибут видимости (по идентификатору) |
| `object_type_has_visibility_attribute_by_guid(guid)` | Проверяет, есть ли у типа объекта атрибут видимости (по GUID) |
| `object_type_id_by_guid(guid)` | Возвращает числовой идентификатор типа объекта по его GUID |
| `object_type_id_by_name(object_type_name)` | Возвращает идентификатор типа объекта по его имени |
| `object_type_is_groupable(object_type_id)` | Проверяет, можно ли группировать экземпляры типа объекта (по id) |
| `object_type_is_groupable_by_guid(guid)` | Проверяет, можно ли группировать экземпляры типа объекта (по GUID) |
| `object_type_is_local(object_type_id)` | Проверяет, является ли тип объекта локальным для текущей базы данных |
| `object_type_is_local_by_guid(guid)` | Проверяет, является ли тип объекта локальным, по его GUID |
| `object_type_level(id)` | Возвращает уровень (глубину) типа объекта в дереве типов |
| `object_type_life_cycle_steps(object_type_id)` | Возвращает список шагов жизненного цикла для типа объекта |
| `object_type_name(object_type_id)` | Возвращает системное имя типа объекта по его идентификатору |
| `object_type_name_by_guid(guid)` | Возвращает системное имя типа объекта по его GUID |
| `object_type_object_name(object_type_id)` | Возвращает имя экземпляра по умолчанию для типа объекта по идентификатору |
| `object_type_object_name_by_guid(guid)` | Возвращает имя экземпляра по умолчанию для типа объекта по его GUID |
| `object_type_parent_applicabilities(part_type_id)` | Возвращает правила применяемости для типа объекта как ПОТОМКА состава |
| `object_types()` | Возвращает список всех типов объектов, определённых в метаданных IPS |
| `object_types_with_applicabilities_ids()` | Возвращает id всех типов объектов, у которых задана хотя бы одна применяемость |
| `object_types_with_enter_in_applicabilities_ids()` | Возвращает id всех типов объектов, которые могут входить в чей-либо состав |
| `objects_by_object_type(object_type_id)` | Возвращает краткие сведения обо всех объектах заданного типа |
| `optimize_child_object_types(object_type_ids)` | Сворачивает набор дочерних типов до минимального эквивалентного покрытия |
| `parent_type_guid_by_guid(child_type_guid)` | Возвращает GUID НЕПОСРЕДСТВЕННОГО родительского типа по GUID потомка |
| `parent_type_guids(child_type_id)` | Возвращает GUID ВСЕЙ цепочки родительских типов (предков) в иерархии типов |
| `parent_type_guids_by_guid(child_type_guid)` | Возвращает GUID ВСЕЙ цепочки родительских типов по GUID потомка |
| `parent_type_id(child_type_id)` | Возвращает id НЕПОСРЕДСТВЕННОГО родительского типа в иерархии типов |
| `parent_type_ids(child_type_id)` | Возвращает id ВСЕЙ цепочки родительских типов (предков) в иерархии типов |
| `parent_type_ids_by_guid(child_type_guid)` | Возвращает id ВСЕЙ цепочки родительских типов по GUID потомка |
| `parent_type_ids_reverse(child_type_id)` | Возвращает id цепочки родительских типов в ОБРАТНОМ порядке (от корня вниз) |
| `pdm_object_type_is_configurable(object_type_id)` | Проверяет, является ли тип объекта конфигурируемым в PDM (по идентификатору) |
| `pdm_object_type_is_contextable(object_type_id)` | Проверяет, является ли тип объекта контекстируемым в PDM (по идентификатору) |
| `pdm_object_type_is_root(object_type_id)` | Проверяет, является ли тип объекта корневым в PDM (по идентификатору) |
| `pdm_relation_type_is_configurable(relation_type_id)` | Проверяет, является ли тип связи конфигурируемым в PDM (по идентификатору) |
| `pdm_relation_type_is_partially_configurable(relation_type_id)` | Проверяет, частично ли конфигурируем тип связи в PDM (по идентификатору) |
| `related_formula_attributes_for_object(object_type_id, attribute_type_id)` | Возвращает id формульных атрибутов объекта, зависящих от заданного атрибута |
| `related_formula_attributes_for_relation(relation_type_id, attribute_type_id)` | Возвращает id формульных атрибутов связи, зависящих от заданного атрибута |
| `relation_type_for_prj_link(prj_link_id)` | Возвращает id типа связи для заданной связи проекта (prjLink) |
| `relation_type_has_grouping(relation_type_id)` | Проверяет, участвует ли тип связи в группировке (по id) |
| `relation_type_has_grouping_by_guid(guid)` | Проверяет, участвует ли тип связи в группировке (по GUID) |
| `relation_type_has_sorting(relation_type_id)` | Проверяет, участвует ли тип связи в сортировке (по id) |
| `relation_type_has_sorting_by_guid(guid)` | Проверяет, участвует ли тип связи в сортировке (по GUID) |
| `relation_type_has_substitutes(id)` | Проверяет, поддерживает ли тип связи замещения (по id) |
| `relation_type_has_substitutes_by_guid(guid)` | Проверяет, поддерживает ли тип связи замещения (по GUID) |
| `relation_type_meta(relation_type_id)` | Возвращает описание типа связи по его идентификатору |
| `relation_type_meta_by_guid(guid)` | Возвращает описание типа связи по его глобальному идентификатору (GUID) |
| `relation_type_meta_exists(relation_type_id)` | Проверяет, существует ли тип связи с заданным идентификатором |
| `relation_type_meta_exists_by_guid(guid)` | Проверяет, существует ли тип связи с заданным GUID |
| `relation_type_meta_guid(relation_type_id)` | Возвращает GUID типа связи по его числовому идентификатору |
| `relation_type_meta_id_by_guid(guid)` | Возвращает числовой идентификатор типа связи по его GUID |
| `relation_type_meta_name(relation_type_id)` | Возвращает прямое имя типа связи по его идентификатору |
| `relation_type_meta_name_by_guid(guid)` | Возвращает прямое имя типа связи по его GUID |
| `relation_types_meta()` | Возвращает список всех типов связей, определённых в метаданных IPS |
| `sorting_object_type_guids()` | Возвращает GUID типов объектов, экземпляры которых можно сортировать |
| `sorting_object_type_ids()` | Возвращает id типов объектов, экземпляры которых можно сортировать |
| `sorting_relation_type_guids()` | Возвращает GUID типов связей, по которым выполняется сортировка |
| `sorting_relation_type_ids()` | Возвращает id типов связей, по которым выполняется сортировка |
| `substitute_object_type_guids()` | Возвращает GUID всех типов объектов, участвующих в замещении |
| `substitute_object_type_ids()` | Возвращает id всех типов объектов, участвующих в замещении |
| `substitute_relation_type_guids()` | Возвращает GUID всех специальных типов связей замещения |
| `substitute_relation_type_ids()` | Возвращает id всех специальных типов связей замещения |
| `top_object_type_guids()` | Возвращает GUID всех КОРНЕВЫХ типов объектов (верхний уровень дерева) |
| `top_object_type_ids()` | Возвращает id всех КОРНЕВЫХ типов объектов (верхний уровень дерева) |
| `top_parent_enabled_object_type_guids_by_guids(object_type_guids)` | Возвращает GUID верхних РАЗРЕШЁННЫХ родительских типов для НАБОРА типов по GUID |
| `top_parent_enabled_object_type_ids_by_ids(object_type_ids)` | Возвращает id верхних РАЗРЕШЁННЫХ родительских типов для НАБОРА типов по их id |
| `top_parent_type_id(child_type_id)` | Возвращает id КОРНЕВОГО типа ветви иерархии для заданного типа |
| `used_sorted_attribute_ids()` | Возвращает идентификаторы используемых атрибутов в порядке сортировки |
| `used_sorted_attributes()` | Возвращает используемые типы атрибутов в порядке сортировки |
| `used_unsorted_attribute_ids()` | Возвращает идентификаторы используемых атрибутов без порядка сортировки |
| `visibility_object_type_guids()` | Возвращает GUID типов объектов, имеющих атрибут видимости |
| `visibility_object_type_ids()` | Возвращает идентификаторы типов объектов, имеющих атрибут видимости |

</details>

<details>
<summary><b><code>objects</code></b> — Объекты: чтение, поиск, запись, жизненный цикл, состав, версии <b>(70)</b></summary>

| Метод | Назначение |
|---|---|
| `object_add_objects_by_template(object_id, body, log_history)` | Добавляет объекты в состав объекта по шаблону-таблице (МУТИРУЮЩАЯ операция) |
| `object_add_temporary_attribute(object_id, attribute_id, fail_if_exists, values)` | Добавляет объекту временный атрибут заданного типа |
| `object_attribute(object_id, attribute_id, get_actual_copy, extend_by_type, throw_not_found)` | Возвращает один атрибут объекта по идентификатору типа атрибута |
| `object_attribute_as_string(object_id, attribute_id, throw_not_found)` | Возвращает значение атрибута объекта в виде готовой строки |
| `object_attribute_descriptions(object_id, attribute_id, throw_not_found)` | Возвращает текстовые описания значений одного атрибута объекта |
| `object_attribute_values(object_id, attribute_id, throw_not_found)` | Возвращает список «сырых» значений указанного атрибута объекта |
| `object_attribute_values_by_guid(object_guid, attribute_id)` | Возвращает список «сырых» значений атрибута объекта, заданного по GUID |
| `object_attributes(object_id, extend_by_type)` | Возвращает все атрибуты объекта вместе с их значениями |
| `object_attributes_descriptions(object_id, throw_not_found)` | Возвращает текстовые описания значений всех атрибутов объекта |
| `object_attributes_init_values(object_id, attr_ids, extend_by_type)` | Возвращает начальные (инициализирующие) значения атрибутов объекта |
| `object_attributes_values(object_id, extend_by_type, attribute_values_modes)` | Возвращает значения всех атрибутов объекта с расширенными метаданными |
| `object_base_version(object_id, throw_not_found)` | Возвращает базовую (актуальную) версию объекта по идентификатору объекта |
| `object_by_version_rule(object_id)` | Возвращает версию объекта, выбранную текущим правилом версий, по id объекта |
| `object_by_version_rule_by_guid(object_guid)` | Возвращает версию объекта по текущему правилу версий, по GUID объекта |
| `object_by_versions_rule(object_id, rule_object_id, throw_not_found)` | Возвращает версию объекта, выбранную по заданному правилу выбора версий |
| `object_calculated_attribute_values(object_id, attribute_values, modes)` | Вычисляет значения формульных (computed) атрибутов объекта на лету |
| `object_can_set_next_lc_step(object_id, next_step_id)` | Проверяет, можно ли перевести объект на следующий шаг ЖЦ (ПРОВЕРКА, без мутации) |
| `object_cancel_changes(object_ids, confirm, admin_mode, log_history, ignore_exceptions)` | Отменяет несохранённые правки объектов (МУТИРУЮЩАЯ; защищена ``confirm``) |
| `object_check_access_rights_for_visibility(version_ids)` | Проверяет права текущего пользователя на правку настроек видимости версий |
| `object_check_edit(object_id)` | Проверяет на сервере допустимость правки атрибутов объекта |
| `object_check_in(object_id, log_history)` | Фиксирует изменения рабочей копии объекта и снимает блокировку редактирования |
| `object_check_in_command(object_id, preserve_working_copies, log_history)` | Фиксирует изменения объекта командой check-in (МУТИРУЮЩАЯ операция) |
| `object_check_out(object_id, log_history)` | Извлекает объект на редактирование и возвращает id его рабочей копии |
| `object_check_out_versions(version_ids, throw_exception)` | Извлекает несколько версий объектов на редактирование одним запросом |
| `object_check_out_with_check_modify(object_id, log_history)` | Извлекает объект на редактирование с предварительной проверкой модифицируемости |
| `object_check_relations_edit(object_id)` | Проверяет на сервере допустимость правки связей объекта |
| `object_check_visibility_available(object_id)` | Проверяет, доступны ли настройки видимости для объекта |
| `object_checkout_date(object_id)` | Возвращает дату извлечения объекта на редактирование (checkout) |
| `object_cleanup_attribute(object_id, attribute_id, confirm, log_history)` | Очищает значения атрибута объекта (РАЗРУШАЮЩАЯ операция) |
| `object_commit_creation(object_id, delete_on_exception, auto_checkout, related_object_ids, log_history)` | Фиксирует создание черновика объекта и возвращает его постоянный идентификатор |
| `object_composition(project_version_id, context_rule, Any] | None)` | Возвращает состав объекта по версии проекта с учётом правила контекста |
| `object_composition_with_params(object_id, relation_type_id, part_type_ids)` | Возвращает состав объекта — его дочерние объекты по связи заданного типа |
| `object_connect_to_object(object_id, to_object_id, log_history)` | Присоединяет один объект к другому (МУТИРУЮЩАЯ операция) |
| `object_create(object_type, attributes, log_history)` | Создаёт новый объект указанного типа в режиме создания (черновик) |
| `object_create_by_prototype(prototype, log_history)` | Создаёт объект по прототипу (объекту-образцу) и возвращает черновик с потомками |
| `object_create_object_version(object_id, log_history)` | Создаёт новую версию объекта на основе текущей (МУТИРУЮЩАЯ операция) |
| `object_delete(object_id, confirm, delete_mode, log_history)` | Удаляет объект (РАЗРУШАЮЩАЯ операция, защищена параметром ``confirm``) |
| `object_delete_attribute(object_id, attribute_id, confirm, log_history)` | Удаляет атрибут объекта (РАЗРУШАЮЩАЯ операция) |
| `object_edit(object_id, log_history)` | Переводит объект в режим редактирования (МУТИРУЮЩАЯ операция, меняет состояние) |
| `object_exclude_from_composition(relation_ids, confirm, delete_relation_mode, log_history, ignore_exceptions)` | Исключает объекты из состава по id связей (РАЗРУШАЮЩАЯ операция, гейт ``confirm``) |
| `object_get(object_id, throw_not_found)` | Возвращает полное описание объекта (его базовую версию) по идентификатору объекта |
| `object_get_by_guid(object_guid, throw_not_found)` | Возвращает полное описание объекта по GUID объекта (``objectGUID``) |
| `object_hash_version(object_id)` | Возвращает хэш версии объекта (целочисленный отпечаток состояния) |
| `object_include_in_composition(project_version_id, part_ids, log_history)` | Включает версии-потомки в состав версии-проекта (МУТИРУЮЩАЯ операция) |
| `object_info(object_id)` | Возвращает краткие сведения об объекте по идентификатору объекта |
| `object_info_by_guid(object_guid)` | Возвращает краткие сведения об объекте по GUID объекта (``objectGUID``) |
| `object_is_parent_type(object_id, object_type_guid)` | Проверяет, является ли тип с заданным GUID родительским для типа объекта |
| `object_load_descriptions(version_ids, throw_exception)` | Загружает краткие описания версий объектов по списку их идентификаторов |
| `object_make_base_version(object_id)` | Делает указанную версию объекта базовой (МУТИРУЮЩАЯ операция) |
| `object_make_base_versions(object_ids, log_history, ignore_exceptions)` | Делает указанные версии объектов базовыми (МУТИРУЮЩАЯ, пакетная операция) |
| `object_print(object_id)` | Инициирует серверную печать объекта по его связанному шаблону печати |
| `object_rollback_check_out(check_out_result, Any], throw_exception)` | Откатывает пакетный check-out, выполненный :meth:`object_check_out_versions` |
| `object_save_changes(object_id, log_history)` | Сохраняет изменения извлечённого объекта, НЕ снимая блокировку редактирования |
| `object_save_to_arc_copy(object_id, log_history)` | Сохраняет объект в архивную копию средствами сервера |
| `object_save_to_disk(object_id)` | Сохраняет файлы (blob-атрибуты) объекта на диск средствами сервера |
| `object_set_attribute_values(object_id, attribute_values, delete_not_existing, dont_delete_blobs, return_delta, log_history)` | Записывает значения нескольких атрибутов объекта одним запросом |
| `object_set_attribute_values_ex(object_id, body, log_history)` | Записывает значения атрибутов в расширенном режиме (с режимами извлечения) |
| `object_set_attributes(object_id, attributes, log_history)` | Записывает набор атрибутов объекта (в формате DTO атрибутов) |
| `object_set_modify_content_date(object_id, confirm)` | Помечает контент объекта изменённым, проставляя текущую дату модификации (МУТАЦИЯ) |
| `object_snapshot_info(object_id)` | Возвращает сводку по снимкам объекта: активный снимок и их коллекцию |
| `object_snapshot_readonly_objects(object_id, snapshot_id)` | Возвращает идентификаторы объектов, доступных только для чтения в снимке |
| `object_update_visibility_settings(object_id, settings)` | Сохраняет настройки видимости объекта (что показано/скрыто в дереве/UI) |
| `object_validate_set_next_lc_step(object_id, next_step_id)` | Проверяет допустимость перевода объекта на следующий шаг ЖЦ (МУТИРУЮЩАЯ операция) |
| `object_visibilities(object_id)` | Возвращает настройки видимости объекта (как он отображается в дереве/UI) |
| `objects_all_versions(params)` | Возвращает все версии объекта (история) по его идентификатору |
| `objects_collection(object_ids, throw_not_found)` | Возвращает описания нескольких объектов одним запросом по списку идентификаторов |
| `objects_select(object_type_id, conditions, attribute_ids, record_count, local_types_mode, trash_mode, last_key_value, last_order_value)` | Ищет объекты заданного типа по условиям на значения их атрибутов |
| `objects_select_by_id(request, object_type_id)` | Возвращает атрибуты заданных объектов с ключами-id атрибутов через POST |
| `objects_select_iter(object_type_id, conditions, attribute_ids, page_size, local_types_mode, trash_mode)` | Итерирует ВСЕ объекты выборки постранично, не держа всё в памяти |
| `objects_select_request(request, object_type_id)` | Возвращает системные атрибуты заданных объектов (ключи-имена) через POST |

</details>

<details>
<summary><b><code>security</code></b> — Права доступа: чтение, проверки, восстановление доступа админа, запись прав <b>(63)</b></summary>

| Метод | Назначение |
|---|---|
| `actions_on_objects_security()` | Возвращает глобальные права на ДЕЙСТВИЯ над объектами (системный уровень) |
| `attribute_group_security(attribute_group_id)` | Возвращает права доступа на ГРУППУ атрибутов (кто что может с группой) |
| `attribute_groups_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ групп атрибутов (метаданное в целом) |
| `attribute_security(attribute_id)` | Возвращает права доступа на АТРИБУТ (кто может читать/изменять атрибут) |
| `attributes_collection_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ атрибутов (метаданное в целом) |
| `check_actions_on_objects_security_access(check)` | Проверяет доступ текущего пользователя к категории «операции над объектами» |
| `check_attribute_group_security_access(attribute_group_id, check)` | Проверяет доступ текущего пользователя к конкретной группе атрибутов |
| `check_attribute_groups_security_access(check)` | Проверяет доступ текущего пользователя к коллекции групп атрибутов |
| `check_attribute_security_access(attribute_id, check)` | Проверяет доступ текущего пользователя к конкретному атрибуту |
| `check_attributes_security_access(check)` | Проверяет доступ текущего пользователя к коллекции атрибутов |
| `check_languages_security_access(check)` | Проверяет доступ текущего пользователя к коллекции языков |
| `check_lifecycle_level_security_access(lifecycle_level_id, check)` | Проверяет доступ текущего пользователя к конкретному уровню жизненного цикла |
| `check_lifecycle_levels_security_access(check)` | Проверяет доступ текущего пользователя к коллекции уровней жизненного цикла |
| `check_lifecycle_scheme_security_access(lifecycle_scheme_id, check)` | Проверяет доступ текущего пользователя к конкретной схеме жизненного цикла |
| `check_lifecycle_schemes_security_access(check)` | Проверяет доступ текущего пользователя к коллекции схем жизненного цикла |
| `check_object_security_access(object_version_id, check)` | Проверяет доступ текущего пользователя к конкретной ВЕРСИИ объекта |
| `check_object_type_lifecycle_scheme_step_access_for_attribute(object_type_id, lifecycle_scheme_step_id, attribute_id, check)` | Проверяет доступ к АТРИБУТУ типа объекта на конкретном шаге схемы ЖЦ |
| `check_object_type_lifecycle_step_attribute_security_access(object_type_id, lifecycle_scheme_step_id, attribute_id, check)` | Проверяет доступ к атрибуту на конкретном шаге схемы ЖЦ для типа объекта |
| `check_object_type_lifecycle_step_security_access(object_type_id, lifecycle_scheme_step_id, check)` | Проверяет доступ текущего пользователя к шагу схемы ЖЦ для типа объекта |
| `check_object_type_security_access(object_type_id, check)` | Проверяет доступ текущего пользователя к конкретному типу объекта |
| `check_object_types_security_access(check)` | Проверяет доступ текущего пользователя к коллекции типов объектов |
| `check_relation_type_security_access(relation_type_id, check)` | Проверяет доступ текущего пользователя к конкретному типу связи |
| `check_relation_types_security_access(check)` | Проверяет доступ текущего пользователя к коллекции типов связей |
| `check_subject_areas_security_access(check)` | Проверяет доступ текущего пользователя к коллекции предметных областей |
| `check_system_security_access(check)` | Проверяет доступ текущего пользователя к системе в целом (общесистемное право) |
| `check_update_object_type_lifecycle_scheme_step_access(object_type_id, lifecycle_scheme_step_id, check)` | Проверяет доступ к ШАГУ схемы ЖЦ типа объекта (право настраивать его права) |
| `languages_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ языков (метаданное в целом) |
| `lifecycle_level_security(lifecycle_level_id)` | Возвращает права доступа на УРОВЕНЬ ЖЦ (кто что может на данном уровне ЖЦ) |
| `lifecycle_levels_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ уровней ЖЦ (метаданное в целом) |
| `lifecycle_scheme_security(lifecycle_scheme_id)` | Возвращает права доступа на СХЕМУ ЖЦ (кто что может с данной схемой ЖЦ) |
| `lifecycle_schemes_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ схем ЖЦ (метаданное в целом) |
| `object_security(object_version_id)` | Возвращает права доступа на конкретную ВЕРСИЮ объекта (кто что может) |
| `object_type_lifecycle_step_attribute_security(object_type_id, lifecycle_scheme_step_id, attribute_id)` | Возвращает права на АТРИБУТ типа объекта на конкретном шаге схемы ЖЦ |
| `object_type_lifecycle_step_security(object_type_id, lifecycle_scheme_step_id)` | Возвращает права доступа на ШАГ схемы ЖЦ конкретного типа объекта |
| `object_type_security(object_type_id)` | Возвращает права доступа на ТИП объекта (кто что может с объектами типа) |
| `object_types_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ типов объектов (метаданное в целом) |
| `relation_type_security(relation_type_id)` | Возвращает права доступа на ТИП связи (кто что может с данным типом связи) |
| `relation_types_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ типов связей (метаданное в целом) |
| `restore_admin_access_actions_on_objects(confirm)` | Восстанавливает доступ администратора к правам операций над объектами (МУТАЦИЯ) |
| `restore_admin_access_attribute(attribute_id, confirm)` | Восстанавливает доступ администратора к правам конкретного атрибута (МУТАЦИЯ) |
| `restore_admin_access_attribute_group(attribute_group_id, confirm)` | Восстанавливает доступ администратора к правам конкретной группы атрибутов (МУТАЦИЯ) |
| `restore_admin_access_attribute_groups(confirm)` | Восстанавливает доступ администратора к правам коллекции групп атрибутов (МУТАЦИЯ) |
| `restore_admin_access_attributes(confirm)` | Восстанавливает доступ администратора к правам коллекции атрибутов (МУТАЦИЯ) |
| `restore_admin_access_languages(confirm)` | Восстанавливает доступ администратора к правам коллекции языков (МУТАЦИЯ) |
| `restore_admin_access_lifecycle_level(lifecycle_level_id, confirm)` | Восстанавливает доступ администратора к правам конкретного уровня ЖЦ (МУТАЦИЯ) |
| `restore_admin_access_lifecycle_levels(confirm)` | Восстанавливает доступ администратора к правам коллекции уровней ЖЦ (МУТАЦИЯ) |
| `restore_admin_access_lifecycle_scheme(lifecycle_scheme_id, confirm)` | Восстанавливает доступ администратора к правам конкретной схемы ЖЦ (МУТАЦИЯ) |
| `restore_admin_access_lifecycle_schemes(confirm)` | Восстанавливает доступ администратора к правам коллекции схем ЖЦ (МУТАЦИЯ) |
| `restore_admin_access_object(object_version_id, confirm)` | Восстанавливает доступ администратора к правам конкретного объекта (версии) (МУТАЦИЯ) |
| `restore_admin_access_object_type(object_type_id, confirm)` | Восстанавливает доступ администратора к правам конкретного типа объекта (МУТАЦИЯ) |
| `restore_admin_access_object_type_lifecycle_scheme_step(object_type_id, lifecycle_scheme_step_id, confirm)` | Восстанавливает доступ администратора к правам цели безопасности (МУТАЦИЯ) |
| `restore_admin_access_object_types(confirm)` | Восстанавливает доступ администратора к правам коллекции типов объектов (МУТАЦИЯ) |
| `restore_admin_access_relation_type(relation_type_id, confirm)` | Восстанавливает доступ администратора к правам конкретного типа связи (МУТАЦИЯ) |
| `restore_admin_access_relation_types(confirm)` | Восстанавливает доступ администратора к правам коллекции типов связей (МУТАЦИЯ) |
| `restore_admin_access_subject_areas(confirm)` | Восстанавливает доступ администратора к правам коллекции предметных областей (МУТАЦИЯ) |
| `restore_admin_access_system(confirm)` | Восстанавливает доступ администратора к правам системы (глобальные права) (МУТАЦИЯ) |
| `restore_object_type_lifecycle_scheme_step_for_attribute(object_type_id, lifecycle_scheme_step_id, attribute_id, confirm)` | Восстанавливает доступ администратора к правам цели безопасности (МУТАЦИЯ) |
| `subject_areas_security()` | Возвращает права доступа на КОЛЛЕКЦИЮ предметных областей (метаданное в целом) |
| `system_security()` | Возвращает права доступа на СИСТЕМУ в целом (общесистемная политика) |
| `update_object_type_lifecycle_scheme_step_child_targets(object_type_id, lifecycle_scheme_step_id, body, Any], confirm)` | Записывает права ДОЧЕРНИХ целей для ШАГА схемы ЖЦ типа объекта (МУТАЦИЯ) |
| `update_object_type_lifecycle_scheme_step_security(object_type_id, lifecycle_scheme_step_id, body, Any], confirm)` | Записывает права доступа на ШАГ схемы ЖЦ типа объекта (МУТАЦИЯ) |
| `update_object_type_lifecycle_scheme_step_security_for_attribute(object_type_id, lifecycle_scheme_step_id, attribute_id, body, Any], confirm)` | Записывает права на АТРИБУТ типа объекта на конкретном шаге схемы ЖЦ (МУТАЦИЯ) |
| `update_object_type_security_child_targets(object_type_id, body, Any], confirm)` | Записывает права для ДОЧЕРНИХ целей безопасности ТИПА объекта (МУТАЦИЯ) |

</details>

<details>
<summary><b><code>imbase</code></b> — Справочная система: каталоги, индексы, поиск, избранное, конвертеры <b>(43)</b></summary>

| Метод | Назначение |
|---|---|
| `imbase_add_from_im_base(request, Any], confirm)` | Добавляет объект из справочника IMBASE в состав объекта (МУТАЦИЯ; ``confirm``) |
| `imbase_add_to_favorite_folder(favorite_folder_id, object_id)` | Добавляет объект в папку избранного IMBASE (личная закладка) |
| `imbase_attribute_existing_values(attribute_guid, params)` | Возвращает существующие значения атрибута в таблицах IMBASE (чтение) |
| `imbase_catalog_id_by_object(object_id)` | Возвращает идентификатор каталога IMBASE, которому принадлежит объект |
| `imbase_catalogs()` | Возвращает идентификаторы каталогов справочной системы IMBASE |
| `imbase_client_cache_state()` | Возвращает сводное состояние клиентского кэша справочной системы IMBASE |
| `imbase_common_params()` | Возвращает основные ОБЩИЕ (системные) параметры IMBASE |
| `imbase_create_object(base_id, confirm, record_id, commit_creation, need_type)` | Создаёт объект IPS из записи справочника IMBASE (МУТАЦИЯ; защищена ``confirm``) |
| `imbase_display_mode_options()` | Возвращает доступные режимы отображения каталогов/таблиц IMBASE |
| `imbase_extended_item(attribute_type_id)` | Возвращает расширенные настройки IMBASE для типа атрибута |
| `imbase_favorite_folders_count(object_id)` | Возвращает число папок «Избранное», в которые добавлен объект IMBASE |
| `imbase_fill_object_attributes(destination_object_id, confirm, object_type_id, base_id, record_id)` | Заполняет атрибуты объекта значениями из записи IMBASE (МУТАЦИЯ; ``confirm``) |
| `imbase_find_by_index(params)` | Выполняет индексный (полнотекстовый) поиск по атрибуту IMBASE (чтение) |
| `imbase_find_in_tables(params)` | Ищет записи в таблицах справочника IMBASE по заданным условиям (чтение) |
| `imbase_find_in_tables_with_progress(params, progress_report_step)` | Ищет записи в таблицах IMBASE по условиям с отчётом о прогрессе (ЧТЕНИЕ) |
| `imbase_get_table_search_existing_attribute_values_with_progress(attribute_guid, params, progress_report_step)` | Ищет существующие значения атрибута IMBASE с отчётом о прогрессе (ЧТЕНИЕ) |
| `imbase_indexes()` | Возвращает информацию об индексах справочной системы IMBASE |
| `imbase_linked_object_path(object_id)` | Возвращает путь к СВЯЗАННОМУ объекту IMBASE в иерархии справочника |
| `imbase_object_applicability(object_version_id)` | Проверяет применяемость (ограничительный перечень) записи IMBASE |
| `imbase_object_by_id_references_names(references)` | Разрешает отображаемые имена объектов по ссылкам-строкам (адресация по id) |
| `imbase_object_create_info(base_id)` | Возвращает информацию о создании объекта на основе элемента IMBASE |
| `imbase_object_linked_table_record_attributes(object_id)` | Возвращает атрибуты записи таблицы справочника IMBASE, связанной с объектом |
| `imbase_object_path(object_id)` | Возвращает путь к объекту IMBASE в иерархии каталогов справочной системы |
| `imbase_object_path_by_key(key_id)` | Возвращает путь к объекту IMBASE по идентификатору ключа |
| `imbase_object_references_names(references)` | Разрешает отображаемые имена объектов по списку ссылок-строк |
| `imbase_record_references_names(references)` | Разрешает отображаемые имена записей по списку ссылок-строк |
| `imbase_remove_from_favorites(parent_id, object_id)` | Удаляет объект из папки избранного IMBASE (обратная операция к add) |
| `imbase_restrictive_applicability_cache(object_version_id)` | Проверяет наличие записи IMBASE в кэше ограничительного перечня |
| `imbase_role_display_mode_options()` | Возвращает ролевые режимы отображения таблиц IMBASE |
| `imbase_rtf_to_plain_text(rtf)` | Конвертирует RTF-значение атрибута IMBASE в простой текст |
| `imbase_rtf_to_svg(rtf, width)` | Конвертирует RTF-значение атрибута IMBASE в SVG (base64-строка) |
| `imbase_supported_catalogs(object_type_id, attribute_type_id)` | Возвращает каталоги IMBASE, применимые для типа объекта и типа атрибута |
| `imbase_table_check_composition(table_id, parent_object_type_id)` | Проверяет возможность включения таблицы справочника в состав типа объекта |
| `imbase_table_created_objects(object_version_id)` | Возвращает объекты, созданные из записей табличной части справочника IMBASE |
| `imbase_table_data(object_version_id)` | Возвращает данные табличной части справочника IMBASE для версии объекта |
| `imbase_table_display_settings(object_version_id)` | Возвращает настройки отображения таблицы справочника IMBASE для версии объекта |
| `imbase_table_mix_data(object_id)` | Возвращает смешанные табличные данные (table mix) объекта IMBASE |
| `imbase_table_record_mix_usage(link_id, record_id)` | Возвращает сведения о вхождении записи таблицы в таблицы составных объектов |
| `imbase_table_search_links(root_object_id)` | Возвращает список связей поиска по таблицам справочника для корневого объекта |
| `imbase_table_user_filter(object_version_id)` | Возвращает пользовательский фильтр таблицы справочника IMBASE для версии объекта |
| `imbase_terminal_folder_ids()` | Возвращает идентификаторы терминальных (конечных) папок IMBASE |
| `imbase_text_note_by_guid(guid)` | Возвращает значение атрибута-текстовой заметки объекта IMBASE по GUID |
| `imbase_user_params()` | Возвращает основные ПОЛЬЗОВАТЕЛЬСКИЕ (персональные) параметры IMBASE |

</details>

<details>
<summary><b><code>bridge</code></b> — Клиентский мост: настройки, плагины, действия запуска, temp-файлы, загрузки <b>(34)</b></summary>

| Метод | Назначение |
|---|---|
| `bridge_add_or_update_settings_xml(integrator_guid, xml_data, confirm)` | Создаёт или обновляет XML-настройки интегратора IPS Bridge (МУТАЦИЯ) |
| `bridge_common_settings()` | Возвращает общие настройки клиентского моста IPS Bridge |
| `bridge_create_launch_action(body, Any] | None, confirm)` | Создаёт новое действие запуска IPS Bridge (МУТАЦИЯ) |
| `bridge_create_temp_directory(confirm)` | Создаёт временный каталог в хранилище сессии IPS Bridge (МУТАЦИЯ) |
| `bridge_delete_temp_stored_item(path, confirm)` | Удаляет временный файл или каталог из хранилища сессии (МУТАЦИЯ) |
| `bridge_download_app(platform_name)` | Скачивает дистрибутив приложения IPS Bridge для указанной платформы (БАЙТЫ) |
| `bridge_download_integrated_app_plugin(plugin_name, with_file)` | Находит и отдаёт плагин встроенного приложения через IPS Bridge |
| `bridge_download_library(library_name)` | Находит и отдаёт библиотеку (DLL) для десктоп-клиента через IPS Bridge |
| `bridge_download_temp_folder_as_zip(file_path, confirm)` | Готовит временную папку к скачиванию как ZIP и возвращает путь (МУТАЦИЯ) |
| `bridge_extract_zip_file(file_path, confirm)` | Распаковывает ZIP-файл во временном хранилище сессии (МУТАЦИЯ) |
| `bridge_get_action_list(body, Any] | None)` | Возвращает список действий запуска IPS Bridge по заданному фильтру |
| `bridge_get_default_actions(object_type_id, user_id)` | Возвращает действия запуска ПО УМОЛЧАНИЮ для типа объекта и пользователя |
| `bridge_get_full_action_list(object_type_id, user_id)` | Возвращает ПОЛНЫЙ список действий запуска для типа объекта и пользователя |
| `bridge_get_integrators()` | Возвращает карту интеграторов, зарегистрированных в IPS Bridge |
| `bridge_get_modifications_history_list()` | Возвращает список изменений, накопленных за время логирования сессии |
| `bridge_launch_action_data(action_id)` | Возвращает полезные данные действия запуска IPS Bridge по идентификатору |
| `bridge_launch_action_info(action_id)` | Возвращает сведения о действии запуска IPS Bridge по его идентификатору |
| `bridge_pack_directory_as_zip(dir_path, confirm)` | Упаковывает временный каталог в ZIP-файл (МУТАЦИЯ) |
| `bridge_plugins()` | Возвращает список клиентских плагинов, зарегистрированных в IPS Bridge |
| `bridge_remove_integrator(integrator_guid, confirm)` | Удаляет интегратор IPS Bridge по его GUID (МУТАЦИЯ) |
| `bridge_remove_launch_action(action_id, confirm)` | Удаляет действие запуска IPS Bridge по его идентификатору (МУТАЦИЯ) |
| `bridge_reset_default_action(object_type_id, action_id, user_id, confirm)` | Сбрасывает действие запуска ПО УМОЛЧАНИЮ для типа объекта (МУТАЦИЯ) |
| `bridge_set_default_action(object_type_id, action_id, user_id, confirm)` | Назначает действие запуска ПО УМОЛЧАНИЮ для типа объекта (МУТАЦИЯ) |
| `bridge_settings_xml(integrator_guid)` | Возвращает XML-настройки интегратора IPS Bridge |
| `bridge_start_log_history(confirm)` | Включает журналирование истории изменений сессии IPS Bridge (МУТАЦИЯ) |
| `bridge_stop_log_history(confirm)` | Выключает журналирование истории изменений сессии IPS Bridge (МУТАЦИЯ) |
| `bridge_update_launch_action(settings_xml, action_id, confirm)` | Обновляет XML-настройки действия запуска IPS Bridge (МУТАЦИЯ) |
| `bridge_upload_file(body, Any] | None, confirm)` | Загружает файл целиком во временное хранилище сессии (МУТАЦИЯ) |
| `bridge_upload_large_file_cancel(request_guid, confirm)` | Отменяет открытую сессию чанковой загрузки файла (МУТАЦИЯ) |
| `bridge_upload_large_file_chunk(body, Any] | None, confirm)` | Передаёт одну часть большого файла в открытую сессию загрузки (МУТАЦИЯ) |
| `bridge_upload_large_file_chunk_base64(body, Any] | None, confirm)` | Передаёт часть большого файла как Base64-строку в сессию (МУТАЦИЯ) |
| `bridge_upload_large_file_request(body, Any] | None, confirm)` | Открывает сессию чанковой загрузки большого файла (МУТАЦИЯ) |
| `bridge_user_defined_launch_action(object_type_id, launch_type)` | Возвращает пользовательское действие запуска для типа объекта и режима |
| `bridge_user_info()` | Возвращает сведения о текущем пользователе IPS Bridge |

</details>

<details>
<summary><b><code>relations</code></b> — Связи: чтение, атрибуты, создание/удаление, расширенный поиск <b>(28)</b></summary>

| Метод | Назначение |
|---|---|
| `relation_add_temporary_attribute(relation_id, attribute_id, fail_if_exists, values)` | Добавляет к СВЯЗИ временный атрибут заданного типа и инициализирует значения |
| `relation_attribute(relation_id, attribute_id, extend_by_type, throw_not_found)` | Возвращает один атрибут СВЯЗИ по идентификатору типа атрибута |
| `relation_attribute_descriptions(relation_id, attribute_id)` | Возвращает текстовые описания значений одного атрибута СВЯЗИ |
| `relation_attribute_values(relation_id, attribute_id, throw_not_found)` | Возвращает список «сырых» значений указанного атрибута СВЯЗИ |
| `relation_attributes(relation_id, extend_by_type)` | Возвращает все атрибуты СВЯЗИ вместе с их значениями |
| `relation_attributes_descriptions(relation_id)` | Возвращает текстовые описания значений всех атрибутов СВЯЗИ |
| `relation_attributes_init_values(relation_id)` | Возвращает исходные (инициализационные) значения атрибутов СВЯЗИ |
| `relation_attributes_values(relation_id, extend_by_type)` | Возвращает значения всех атрибутов СВЯЗИ с расширенными метаданными |
| `relation_by_guid_and_project(relation_guid, project_id)` | Возвращает связь по её устойчивому ``GUID`` в контексте проекта-родителя |
| `relation_by_project_and_part(project_id, part_id)` | Возвращает связь по паре «объект-родитель → версия-потомок» |
| `relation_create(relation, log_history)` | Создаёт связь «родитель → потомок» в составе изделия (МУТИРУЮЩАЯ операция) |
| `relation_create_collection(relations, log_history)` | Создаёт сразу несколько связей «родитель → потомок» одним запросом (МУТИРУЮЩАЯ) |
| `relation_delete(relation_id, confirm, delete_mode, log_history)` | Удаляет связь по её идентификатору (РАЗРУШАЮЩАЯ операция, защищена ``confirm``) |
| `relation_delete_attribute(relation_id, attribute_id, confirm, log_history)` | Удаляет один атрибут СВЯЗИ по id связи и id атрибута (РАЗРУШАЮЩАЯ, ``confirm``) |
| `relation_get(relation_id)` | Возвращает связь между объектами по её идентификатору |
| `relation_get_by_guid(relation_guid)` | Возвращает связь между объектами по её GUID |
| `relation_set_attribute_values(relation_id, attribute_values, delete_not_existing, dont_delete_blobs, return_delta, log_history, modes)` | Записывает значения атрибутов СВЯЗИ списком ``AttributeValues`` |
| `relation_set_attribute_values_ex(relation_id, body, log_history)` | Записывает значения атрибутов СВЯЗИ в расширенном режиме (с режимами извлечения) |
| `relation_set_attributes(relation_id, attributes, log_history)` | Записывает (заменяет) набор атрибутов СВЯЗИ переданным списком ``Attribute`` |
| `relation_types()` | Возвращает список всех типов связей, определённых в IPS |
| `relation_update_relations_attributes(body, Any], log_history)` | Пакетно обновляет атрибуты сразу нескольких связей одним запросом |
| `relations_by_project(project_id, relation_type_id)` | Возвращает связи объекта-родителя указанного типа |
| `relations_consist_from(params)` | Расширенный поиск состава объекта — связи к объектам, из которых он состоит |
| `relations_consist_from_request(request)` | Возвращает рёбра состава объекта (из чего состоит) через POST-запрос |
| `relations_enters_in(params)` | Расширенный поиск вхождений объекта — связи к объектам, в которые он входит |
| `relations_enters_in_version(params)` | Расширенный поиск вхождений ВЕРСИИ объекта — связи к её родителям |
| `relations_enters_in_version_request(request)` | Возвращает рёбра вхождения версии объекта (куда входит) через POST-запрос |
| `relations_select(params)` | Произвольная выборка связей по типу, условиям и атрибутам (с пагинацией) |

</details>

<details>
<summary><b><code>files</code></b> — Файловые атрибуты: загрузка/прикрепление/удаление, таблицы, прототипы <b>(27)</b></summary>

| Метод | Назначение |
|---|---|
| `add_object_file(object_id, attribute_id, file_data, file_name, file_type, modify_date_time, real_file_size)` | Прикрепляет НОВЫЙ файл прямо к файловому атрибуту объекта (МУТИРУЮЩАЯ) |
| `attach_temp_files(object_id, attachments)` | Прикрепляет загруженные временные файлы к файловым атрибутам объекта (МУТИРУЮЩАЯ) |
| `check_unique_file_names(file_id, file_names)` | Проверяет список имён файлов на уникальность относительно записи файла |
| `delete_object_file(object_id, attribute_id, blob_id, confirm)` | Удаляет файл из файлового атрибута объекта (РАЗРУШАЮЩАЯ, ``confirm``) |
| `delete_temp_file(temp_file_name)` | Удаляет ранее загруженный временный файл из временного хранилища (МУТИРУЮЩАЯ) |
| `file_attributes(object_id)` | Возвращает объект вместе со всеми его файловыми атрибутами и файлами |
| `file_id_by_name(file_name)` | Возвращает идентификатор файла по его имени из сервиса имён файлов IPS |
| `file_prototypes(object_id)` | Возвращает список файлов-прототипов (шаблонов), доступных для объекта |
| `file_unique_name(file_name, id)` | Возвращает уникальное имя файла на основе предложенного имени |
| `get_file_name_table(file_name)` | Возвращает таблицу метаданных имён файлов (опционально по образцу имени) |
| `get_file_names_table(file_names)` | Возвращает таблицу метаданных файлов по заданному списку имён |
| `get_files_table(file_ids)` | Возвращает таблицу метаданных файлов по списку идентификаторов файлов |
| `get_files_table_all_attributes(body, Any])` | Возвращает таблицу файлов объектов со всеми атрибутами (фильтр по имени) |
| `get_files_table_by_fields(body, Any])` | Возвращает таблицу файлов заданных объектов с выбранными колонками |
| `get_files_table_with_snapshot_ids(body, Any])` | Возвращает таблицу файлов объектов в состоянии на момент снимков |
| `handle_file_attributes_for_object_creation(object_id, prototype)` | Готовит файловые атрибуты создаваемого объекта по прототипу (подготовка) |
| `next_file_id()` | Возвращает следующий свободный идентификатор файла из id-пространства IPS |
| `object_file_by_blob_id(object_id, blob_id)` | Загружает содержимое файла объекта по идентификатору BLOB-записи |
| `object_file_by_name(object_id, file_name)` | Загружает содержимое файла объекта, выбранного по его имени |
| `object_files_with_composition(object_id, body, Any] | None)` | Возвращает дерево файлов объекта с рекурсивным разворачиванием состава |
| `object_ids_by_file_name(file_name)` | Возвращает идентификаторы объектов, владеющих файлом с заданным именем |
| `set_file_attr_prototype(object_id, confirm)` | Назначает объекту прототипы его файловых атрибутов (МУТИРУЮЩАЯ) |
| `set_prototype(object_id, prototype, confirm)` | Назначает объекту конкретный файл-прототип по описанию (МУТИРУЮЩАЯ) |
| `swap_object_files(object_id, body, confirm)` | Переставляет два файла внутри файлового атрибута объекта (МУТИРУЮЩАЯ) |
| `update_object_file(object_id, attribute_id, blob_id, file_data, file_name, modify_date_time, real_file_size)` | Заменяет СОДЕРЖИМОЕ уже прикреплённого файла объекта (МУТИРУЮЩАЯ) |
| `update_object_file_info(object_id, body)` | Правит ИМЯ и/или КОММЕНТАРИЙ файла объекта без замены байтов (МУТИРУЮЩАЯ) |
| `upload_temp_file(file_data, file_name, is_already_packed)` | Загружает файл во временное хранилище сервера и возвращает его имя (МУТИРУЮЩАЯ) |

</details>

<details>
<summary><b><code>forms</code></b> — Формы и виджеты, пользователи и группы, цвета, предметные области, find* <b>(24)</b></summary>

| Метод | Назначение |
|---|---|
| `default_columns_for_widget()` | Возвращает набор колонок по умолчанию для табличного виджета |
| `default_widget_colors()` | Возвращает палитру цветов виджетов по умолчанию |
| `find_applicability(options)` | Подбирает объекты по применимости в контексте формы (чтение через POST) |
| `find_collection(options)` | Подбирает коллекцию объектов по параметрам формы (чтение через POST) |
| `find_composition(options)` | Подбирает объекты состава формы по параметрам (чтение через POST) |
| `find_objects_list(request)` | Возвращает строки списка объектов формы по версиям (чтение через POST) |
| `find_user_groups_and_users(version_id)` | Возвращает группы и пользователей состава формы одним вызовом |
| `find_user_groups_and_users_in_composition(version_id)` | Возвращает группы и пользователей состава формы одним вызовом |
| `find_user_groups_in_composition(version_id)` | Возвращает группы пользователей, найденные в составе формы данной версии |
| `find_users(request)` | Разворачивает источники адресатов в список пользователей (чтение через POST) |
| `form(version_id)` | Возвращает форму (корневой виджет) по идентификатору версии |
| `form_related_object_type_guids(form_id)` | Возвращает GUID типов объектов, связанных с формой |
| `form_related_relation_type_guids(form_id)` | Возвращает GUID типов связей, связанных с формой |
| `forms_for(version_id, is_create_object, is_relation)` | Возвращает список форм, применимых к указанной версии объекта |
| `image_for_widget(version_id)` | Возвращает изображение виджета по идентификатору версии (строкой) |
| `rank_find_collection(ids)` | Возвращает ранги (роли) по списку версий (чтение через POST) |
| `rank_find_inner_users(version_id)` | Возвращает пользователей из состава формы, включая входящих в группы |
| `save_form_widget(widget, Any], form_id, confirm)` | Сохраняет (создаёт/перезаписывает) виджет формы IPS (МУТАЦИЯ) |
| `subject_area_find_collection()` | Возвращает коллекцию предметных областей форм |
| `system_colors()` | Возвращает системную палитру цветов для оформления виджетов форм |
| `user_find_collection(ids)` | Возвращает пользователей по списку версий (чтение через POST) |
| `user_group_find_collection(ids)` | Возвращает группы пользователей по списку версий (чтение через POST) |
| `user_group_find_roots()` | Возвращает корневые (верхнеуровневые) группы пользователей |
| `widget_colors()` | Возвращает пользовательскую палитру цветов для оформления виджетов форм |

</details>

<details>
<summary><b><code>improjects</code></b> — Проекты и задачи (Gantt): чтение + создание/правка/удаление/исполнение <b>(24)</b></summary>

| Метод | Назначение |
|---|---|
| `change_task_progress(task_id, progress, is_need_to_log_modification_history, confirm)` | Изменяет процент выполнения (прогресс) задачи проекта Improject (МУТАЦИЯ) |
| `complete_project(project_id, is_need_to_log_modification_history, confirm)` | Завершает проект Improject (переводит в финальное состояние) (МУТАЦИЯ) |
| `create_dependency(project_id, request, Any], confirm)` | Создаёт зависимость (связь) между задачами проекта Improject (МУТАЦИЯ) |
| `create_project(request, Any], confirm)` | Создаёт новый проект Improject (план-график / диаграмму Ганта) (МУТАЦИЯ) |
| `create_task(project_id, request, Any], confirm)` | Создаёт новую задачу в проекте Improject (строку диаграммы Ганта) (МУТАЦИЯ) |
| `delete_dependency(dependency_id, confirm)` | Удаляет зависимость между задачами проекта Improject (МУТАЦИЯ) |
| `delete_task(task_id, confirm)` | Удаляет задачу из проекта Improject (МУТАЦИЯ, необратимо в API) |
| `grid_columns()` | Возвращает набор колонок табличного представления (грида) проектов Improject |
| `move_task_level_down(task_id, new_parent_task_id, confirm)` | Понижает уровень задачи в иерархии проекта Improject (делает подзадачей) (МУТАЦИЯ) |
| `move_task_level_up(task_id, new_parent_task_id, new_prev_task_id, confirm)` | Повышает уровень задачи в иерархии проекта Improject (выносит из подзадач) (МУТАЦИЯ) |
| `project(project_id)` | Возвращает проект Improject (план-график) с задачами, связями и ресурсами |
| `reorder_task(task_id, new_parent_task_id, new_prev_task_id, new_next_task_id, confirm)` | Меняет порядок (позицию) задачи в проекте Improject (МУТАЦИЯ) |
| `resource_assignments()` | Возвращает сводку назначений ресурсов на задачи проектов Improject |
| `save_approval_result(task_id, request, Any], is_need_to_log_modification_history, confirm)` | Сохраняет результат согласования (резолюцию) задачи проекта Improject (МУТАЦИЯ) |
| `save_project_zoom_level(project_id, scale_type, confirm)` | Сохраняет масштаб (zoom) шкалы времени диаграммы Ганта проекта (МУТАЦИЯ) |
| `start_executing_project(project_id, is_need_to_log_modification_history, confirm)` | Запускает исполнение проекта Improject (переводит план-график в работу) (МУТАЦИЯ) |
| `start_executing_task(task_id, is_need_to_log_modification_history, confirm)` | Запускает исполнение задачи проекта Improject (переводит в работу) (МУТАЦИЯ) |
| `stop_executing_project(project_id, is_need_to_log_modification_history, confirm)` | Останавливает исполнение проекта Improject (приостанавливает работы) (МУТАЦИЯ) |
| `task(task_id)` | Возвращает сведения об одной задаче проекта Improject (карточку задачи) |
| `task_attachments(task_id)` | Возвращает список вложений задачи проекта Improject |
| `task_attachments_allowed_types()` | Возвращает id типов объектов, допустимых как вложения задач проектов Improject |
| `update_dependency(dependency_id, request, Any], confirm)` | Обновляет существующую зависимость между задачами проекта Improject (МУТАЦИЯ) |
| `update_grid_columns(request, Any], confirm)` | Сохраняет состав и порядок колонок грида (таблицы) проектов Improject (МУТАЦИЯ) |
| `update_task(task_id, request, Any], confirm)` | Обновляет существующую задачу проекта Improject (МУТАЦИЯ) |

</details>

<details>
<summary><b><code>document_editor</code></b> — Редактор документов: буфер, свойства, шрифты, содержимое, формулы <b>(19)</b></summary>

| Метод | Назначение |
|---|---|
| `doc_editor_all_fonts_name(update)` | Возвращает список имён всех шрифтов, доступных редактору документов |
| `doc_editor_buffer()` | Возвращает структуру документа из буфера редактора как дерево узлов |
| `doc_editor_close_document(object_guid, file_blob_id, mode, confirm)` | Закрывает открытый в редакторе документ (МУТАЦИЯ сессии) |
| `doc_editor_complect_document_content(object_guid)` | Возвращает содержимое комплектного (сборного) документа в редакторе |
| `doc_editor_content(object_guid, file_blob_id, mode)` | Возвращает содержимое документа (``DocumentContentDto``) в редакторе |
| `doc_editor_element_props(body, Any] | None)` | Возвращает свойства конкретного элемента документа в редакторе |
| `doc_editor_execute_batch_transactions(body, Any] | None, confirm)` | Выполняет пакет транзакций правок документа в редакторе (МУТАЦИЯ) |
| `doc_editor_font_list()` | Возвращает признак готовности (наличия) списка шрифтов редактора документов |
| `doc_editor_formulas(object_guid, file_blob_id, mode)` | Возвращает список формул документа (``FormulaInfo``) в редакторе |
| `doc_editor_general_formulas_view(formulas, Any]] | None)` | Возвращает представление (вид) общих формул редактора документов |
| `doc_editor_get_font()` | Возвращает сведения о текущем шрифте редактора документов |
| `doc_editor_non_assignable_prop_name(props)` | Возвращает наименование неназначаемого свойства элемента редактора документов |
| `doc_editor_page_child_nodes(body, Any] | None)` | Возвращает содержимое страницы документа с её дочерними узлами |
| `doc_editor_page_svg(body, Any] | None)` | Возвращает SVG-представление страницы документа в редакторе |
| `doc_editor_prop_name(props)` | Возвращает наименование назначаемого свойства элемента редактора документов |
| `doc_editor_remove_from_open_documents(object_guid, file_blob_id, confirm)` | Удаляет документ из списка открытых в редакторе документов (МУТАЦИЯ сессии) |
| `doc_editor_save_document(object_guid, file_blob_id, is_virtual_document, type_id, new_object_guid_after_save_virtual_document, confirm)` | Сохраняет открытый в редакторе документ (МУТАЦИЯ сессии) |
| `doc_editor_save_font(body, Any] | None, confirm)` | Сохраняет (регистрирует) шрифт в подсистеме редактора документов (МУТАЦИЯ) |
| `doc_editor_text_modal_setting_preview(body, Any] | None)` | Возвращает предпросмотр текста по настройкам модального окна редактора |

</details>

<details>
<summary><b><code>samples</code></b> — Демо-API сообщений и значений: CRUD, выборки, файловые значения <b>(13)</b></summary>

| Метод | Назначение |
|---|---|
| `add_sample_message(message, Any], confirm)` | Добавляет демо-сообщение в учебный раздел ``samples`` (мутация, ``confirm``) |
| `clear_message_updates(confirm)` | Очищает все демо-сообщения учебного раздела ``samples`` (МАССОВАЯ операция) |
| `delete_message(message_id, confirm)` | Удаляет демо-сообщение учебного раздела ``samples`` (РАЗРУШАЮЩАЯ операция) |
| `message_by_id(message_id)` | Возвращает одно демо-сообщение учебного раздела ``samples`` по идентификатору |
| `messages()` | Возвращает все демо-сообщения учебного раздела ``samples`` |
| `messages_by_filter(contains_text, from_time, to_time)` | Возвращает демо-сообщения, отфильтрованные по подстроке текста и интервалу дат |
| `sample_value_as_content(file_name)` | Возвращает содержимое демо-файла как контент (учебный раздел, БАЙТЫ) |
| `sample_value_as_file(file_name)` | Возвращает содержимое демо-файла как файл (учебный раздел, БАЙТЫ) |
| `sample_value_as_long(value)` | Возвращает переданное число (round-trip ``long``) учебного раздела |
| `sample_values()` | Возвращает демо-приветствие для текущего пользователя (учебный раздел) |
| `update_message(message_id, message, Any], confirm)` | Полностью обновляет демо-сообщение учебного раздела ``samples`` (мутация) |
| `update_message_last_write_time(message_id, last_write_time, confirm)` | Обновляет время последнего изменения демо-сообщения ``samples`` (мутация) |
| `update_message_text(message_id, text, confirm)` | Обновляет только текст демо-сообщения учебного раздела ``samples`` (мутация) |

</details>

<details>
<summary><b><code>object_types</code></b> — Экземпляры объектов по типу и определения типов (контроллер objectTypes) <b>(12)</b></summary>

| Метод | Назначение |
|---|---|
| `object_type_all_child_guids(object_type_guid)` | Возвращает GUID всех дочерних ТИПОВ заданного типа объекта |
| `object_type_composition(object_type_id, params, Any] | None)` | Возвращает состав ОБЪЕКТОВ заданного типа (объекты + их под-состав) |
| `object_type_definition(object_type_id)` | Возвращает определение типа объекта (``ObjectTypeDto``) по идентификатору |
| `object_type_definition_by_guid(object_type_guid)` | Возвращает определение типа объекта (``ObjectTypeDto``) по его GUID |
| `object_type_definition_by_name(object_type_name)` | Возвращает определение типа объекта (``ObjectTypeDto``) по его имени |
| `object_type_icons(object_type_ids)` | Возвращает иконки типов объектов по списку id типов (для UI) |
| `object_type_object_ids(object_type_id)` | Возвращает идентификаторы всех РЕАЛЬНЫХ объектов (экземпляров) заданного типа |
| `object_type_objects(object_type_id)` | Возвращает краткие сведения обо всех РЕАЛЬНЫХ объектах (экземплярах) типа |
| `object_type_objects_info(object_type_id)` | Возвращает сводку (счётчики) по РЕАЛЬНЫМ объектам (экземплярам) заданного типа |
| `object_type_quick_info(object_type_id)` | Возвращает краткую информацию о ТИПЕ объекта по идентификатору |
| `object_type_quick_info_by_guid(object_type_guid)` | Возвращает краткую информацию о ТИПЕ объекта по его GUID |
| `object_types_tree(object_type_ids)` | Возвращает дерево (иерархию родитель→потомок) типов объектов |

</details>

<details>
<summary><b><code>graph_signs</code></b> — Настройки штампов ЭЦП (ранги/архивы/уровни и шаги ЖЦ): чтение и запись <b>(11)</b></summary>

| Метод | Назначение |
|---|---|
| `archive_sign_settings(archive_id)` | Возвращает настройки графических подписей (штампов ЭЦП), назначенных архиву |
| `lifecycle_level_sign_settings(lifecycle_level_id)` | Возвращает настройки графических подписей (штампов ЭЦП) уровня жизненного цикла |
| `lifecycle_step_sign_settings(lifecycle_step_id)` | Возвращает настройки графических подписей (штампов ЭЦП) шага жизненного цикла |
| `object_type_lifecycle_step_sign_settings(object_type_id, lifecycle_level_id)` | Возвращает настройки графических подписей шага ЖЦ для конкретного ТИПА объекта |
| `rank_graph_sign_object_types()` | Возвращает id типов объектов, доступных для добавления в настройки подписей ранга |
| `rank_graph_signs(rank_id)` | Возвращает настройки графических подписей ранга, сгруппированные по типу объекта |
| `save_rank_graph_signs(rank_id, signs, Any]], confirm)` | Записывает настройки графических подписей ранга (МУТАЦИЯ, ``confirm``) |
| `update_archive_sign_settings(archive_id, groups, Any]], confirm)` | Записывает настройки графических подписей (штампов ЭЦП) архива (МУТАЦИЯ, ``confirm``) |
| `update_lifecycle_level_sign_settings(lifecycle_level_id, groups, Any]], confirm)` | Записывает настройки графических подписей уровня ЖЦ (МУТАЦИЯ, ``confirm``) |
| `update_lifecycle_step_sign_settings(lifecycle_step_id, groups, Any]], confirm)` | Записывает настройки графических подписей шага ЖЦ (МУТАЦИЯ, ``confirm``) |
| `update_object_type_lifecycle_step_sign_settings(object_type_id, lifecycle_level_id, groups, Any]], confirm)` | Записывает настройки графических подписей шага ЖЦ для ТИПА объекта (МУТАЦИЯ) |

</details>

<details>
<summary><b><code>briefcase</code></b> — Портфель: статус, проверка метаданных, экспорт/импорт объектов <b>(10)</b></summary>

| Метод | Назначение |
|---|---|
| `briefcase_cancel_export()` | Отменяет текущую операцию экспорта Портфеля |
| `briefcase_cancel_import()` | Отменяет текущую операцию импорта Портфеля |
| `briefcase_check_metadata_cancel()` | Отменяет текущую проверку совместимости метаданных Портфеля |
| `briefcase_check_metadata_only_start(briefcase_id, briefcase_path, system_only, confirm)` | Запускает проверку метаданных Портфеля без чтения данных (МУТИРУЮЩАЯ, ``confirm``) |
| `briefcase_check_metadata_result()` | Возвращает результат фоновой проверки совместимости метаданных Портфеля |
| `briefcase_check_metadata_start(request, Any], confirm)` | Запускает полную проверку метаданных Портфеля по запросу импорта (МУТИРУЮЩАЯ) |
| `briefcase_export_progress()` | Возвращает прогресс текущей операции экспорта Портфеля |
| `briefcase_start_export(request, Any], confirm)` | Запускает экспорт объектов в Портфель (СОЗДАЁТ артефакт, ``confirm``) |
| `briefcase_start_import(request, Any], confirm)` | Запускает импорт объектов из Портфеля в базу (РАЗРУШАЮЩАЯ/НЕОБРАТИМАЯ, ``confirm``) |
| `briefcase_status()` | Возвращает статус текущей фоновой задачи Портфеля (экспорта/импорта) |

</details>

<details>
<summary><b><code>calendars</code></b> — Производственные и пользовательские календари, фильтры, запись <b>(10)</b></summary>

| Метод | Назначение |
|---|---|
| `base_calendar_filter()` | Возвращает базовый (общесистемный) фильтр особых дней календаря |
| `calendar_settings(calendar_id)` | Возвращает полные настройки календаря по его идентификатору |
| `calendars()` | Возвращает список всех календарей IPS (id + имя) |
| `set_base_calendar(object_id, base_calendar_id, confirm)` | Назначает объекту базовый производственный календарь (МУТИРУЮЩАЯ, ``confirm``) |
| `unit_calendar_for_user(user_id)` | Возвращает календарь подразделения, к которому относится пользователь |
| `unit_calendar_settings(unit_id)` | Возвращает настройки календаря организационного подразделения (unit) |
| `update_calendar_settings(calendar, Any], confirm)` | Записывает настройки производственного календаря (МУТИРУЮЩАЯ, ``confirm``) |
| `update_user_calendar_settings(calendar, Any], confirm)` | Записывает настройки ПОЛЬЗОВАТЕЛЬСКОГО календаря (МУТИРУЮЩАЯ, ``confirm``) |
| `user_calendar_filter()` | Возвращает персональный фильтр особых дней календаря текущего пользователя |
| `user_calendar_settings(user_id)` | Возвращает личный (пользовательский) календарь по идентификатору пользователя |

</details>

<details>
<summary><b><code>workflow</code></b> — Процессы: переменные, вложения активности (создание/прикрепление) <b>(9)</b></summary>

| Метод | Назначение |
|---|---|
| `wf_add_attachments(activity_id, attachment_ids)` | Прикрепляет объекты к активности (задаче) процесса как вложения |
| `wf_attach_files(activity_id, file_data, file_name, confirm)` | Прикрепляет файл к активности (задаче) процесса как вложение (МУТИРУЮЩАЯ) |
| `wf_attachment_allowed_types(activity_id)` | Возвращает идентификаторы типов объектов, допустимых как вложения активности |
| `wf_attachments(activity_id)` | Возвращает список объектов, прикреплённых к активности процесса как вложения |
| `wf_attachments_data(attachment_ids)` | Возвращает данные вложений процесса по их идентификаторам |
| `wf_create_attach_files(file_data, file_name, confirm)` | Создаёт объект-вложение «Файл во вложении» из загружаемого файла (МУТИРУЮЩАЯ) |
| `wf_remove_attachments(activity_id, attachment_ids, confirm)` | Открепляет вложения от активности процесса (необратимо, защищено ``confirm``) |
| `wf_save_variables(activity_id, variables)` | Сохраняет (записывает) переменные процесса на активности (задаче) workflow |
| `wf_variables(activity_id, is_global_variable)` | Возвращает переменные процесса, доступные на активности (задаче) workflow |

</details>

<details>
<summary><b><code>discussions</code></b> — Обсуждения объектов: чтение и запись сообщений, изображения <b>(8)</b></summary>

| Метод | Назначение |
|---|---|
| `add_discussion_image(file_data, file_name, discussion_version_id, object_version_id, confirm)` | Загружает изображение в обсуждение и возвращает ссылку на него (МУТИРУЮЩАЯ) |
| `add_message(object_version_id, caption, text)` | Добавляет новое сообщение в обсуждение версии объекта (МУТИРУЮЩАЯ операция) |
| `can_discuss(object_version_id)` | Проверяет, допускает ли версия объекта ведение обсуждения |
| `edit_message(message_id, caption, text)` | Редактирует существующее сообщение обсуждения (МУТИРУЮЩАЯ операция) |
| `find_messages(object_version_id, all_object_versions)` | Возвращает сообщения обсуждений, относящиеся к версии объекта |
| `get_messages(message_ids)` | Возвращает сообщения обсуждений по списку их идентификаторов |
| `get_messages_by_id(discussion_version_id)` | Возвращает все сообщения одного обсуждения по идентификатору его версии |
| `remove_message(message_id, confirm)` | Удаляет сообщение обсуждения (РАЗРУШАЮЩАЯ операция, защищена ``confirm``) |

</details>

<details>
<summary><b><code>docs</code></b> — Типы/суффиксы документов, настройки, наследование <b>(8)</b></summary>

| Метод | Назначение |
|---|---|
| `doc_settings(document_type)` | Возвращает настройки заданного типа документа (``DocumentTypeSettingsDto``) |
| `doc_settings_list(document_type_ids)` | Возвращает настройки для перечня типов документов одним запросом (чтение) |
| `doc_suffixes()` | Возвращает список суффиксов документов, известных серверу (чтение) |
| `document_types_by_file_ext(file_ext)` | Возвращает типы документов, допускающие файл с заданным расширением (чтение) |
| `document_types_by_output_object_types(object_type_ids, root_document_object_type)` | Возвращает типы документов по их выходным типам объектов (чтение) |
| `inherited_from_constructor_documents(document_type)` | Сообщает, наследует ли тип документа от КОНСТРУКТОРСКИХ документов (чтение) |
| `inherited_from_documents(document_type)` | Сообщает, наследует ли тип документа от базового типа ДОКУМЕНТОВ (чтение) |
| `set_doc_settings(settings, Any], document_type, confirm)` | Записывает настройки заданного типа документа (МУТАЦИЯ) |

</details>

<details>
<summary><b><code>selection_classificators</code></b> — Классификаторы выбора: чтение и включение/исключение объектов <b>(8)</b></summary>

| Метод | Назначение |
|---|---|
| `classificator_attributes(classificator_id, object_id)` | Возвращает значения атрибута объекта, ограниченные классификатором выбора |
| `classifiers_for_object_type(object_type_id)` | Возвращает идентификаторы классификаторов выбора, заданных для типа объекта |
| `classify_object(object_id, classificator_object_ids)` | Классифицирует объект по указанным классификаторам выбора (мутирующая) |
| `exclude_object_from_classificators(object_id, classificator_object_ids, confirm)` | Исключает один объект из нескольких классификаторов выбора (мутирующая, защищена) |
| `exclude_objects_from_classificator(classificator_id, object_ids, confirm)` | Исключает несколько объектов из одного классификатора выбора (мутирующая, защищена) |
| `include_object_in_classificators(object_id, classificator_object_ids)` | Включает один объект сразу в несколько классификаторов выбора (мутирующая) |
| `include_objects_in_classificator(classificator_id, object_ids)` | Включает несколько объектов в один классификатор выбора (мутирующая) |
| `is_multi_select_classifier()` | Возвращает глобальную настройку: допускают ли классификаторы множественный выбор |

</details>

<details>
<summary><b><code>config</code></b> — Чтение параметров конфигурации сервера <b>(7)</b></summary>

| Метод | Назначение |
|---|---|
| `config_read_bool(module_name, section_id, param_name, default_value, config_mode)` | Читает булев параметр конфигурации сервера IPS |
| `config_read_date_time(module_name, section_id, param_name, default_value, config_mode)` | Читает параметр-дату/время конфигурации сервера IPS |
| `config_read_double(module_name, section_id, param_name, default_value, config_mode)` | Читает вещественный (double) параметр конфигурации сервера IPS |
| `config_read_integer(module_name, section_id, param_name, default_value, config_mode)` | Читает целочисленный параметр конфигурации сервера IPS |
| `config_read_string(module_name, section_id, param_name, default_value, config_mode)` | Читает строковый параметр конфигурации сервера IPS |
| `config_read_string_no_cache(module_name, section_id, param_name, is_global_param)` | Читает строковый параметр конфигурации сервера IPS в обход кэша |
| `server_os_platform()` | Возвращает платформу операционной системы, на которой работает сервер IPS |

</details>

<details>
<summary><b><code>settings</code></b> — Настройки и права пользователя, настройки просмотра/печати, данные безопасности <b>(7)</b></summary>

| Метод | Назначение |
|---|---|
| `add_or_update_security_data(data, Any], confirm)` | Создаёт или обновляет данные безопасности пользователя (МУТАЦИЯ) |
| `remove_security_data(user_id, confirm)` | Удаляет данные безопасности пользователя (РАЗРУШАЮЩАЯ операция) |
| `security_data()` | Возвращает данные безопасности пользователей: связки ``userId`` ↔ группа |
| `set_view_print_settings(object_type_id, settings, Any], confirm)` | Записывает настройки внедрения данных при просмотре/печати типа объекта (``confirm``) |
| `user_group()` | Возвращает группу безопасности инструментов ТЕКУЩЕГО пользователя |
| `user_rights()` | Возвращает уровень прав ТЕКУЩЕГО пользователя на изменение настроек |
| `view_print_settings(object_type_id)` | Возвращает настройки внедрения данных при просмотре/печати для типа объекта |

</details>

<details>
<summary><b><code>documents</code></b> — Прототипы и настройки документов <b>(6)</b></summary>

| Метод | Назначение |
|---|---|
| `create_document_prototypes(object_type_id, confirm)` | Создаёт прототип документа для указанного типа объекта (МУТАЦИЯ) |
| `document_prototypes_common()` | Возвращает общие (доступные всем типам) прототипы документов |
| `document_prototypes_private()` | Возвращает приватные (привязанные к типам) прототипы документов |
| `document_settings(object_type_id)` | Возвращает настройки документов для заданного типа объекта |
| `save_document_settings(object_type_id, settings, Any], confirm)` | Записывает настройки документов для ТИПА объекта (МУТИРУЮЩАЯ, ``confirm``) |
| `update_document_prototypes(prototype_id, confirm)` | Обновляет прототип документа по его идентификатору (МУТАЦИЯ) |

</details>

<details>
<summary><b><code>crypto_signing</code></b> — ЭЦП: настройки, сведения о подписях, хэш, создание подписей <b>(5)</b></summary>

| Метод | Назначение |
|---|---|
| `create_crypto_sign(request, Any], eds_as_string, confirm)` | Создаёт криптографическую подпись (ЭЦП) объекта (МУТИРУЮЩАЯ, ``confirm``) |
| `create_separated_crypto_sign(object_id, request, Any], eds_as_string, confirm)` | Создаёт отделённую (separated) ЭЦП объекта (МУТИРУЮЩАЯ, ``confirm``) |
| `object_encoded_hash(object_id, graph, alg_id, crypto_provider)` | Возвращает кодированный хэш объекта — исходные данные для формирования ЭЦП |
| `sign_info_stream(object_id, graph)` | Возвращает поток сведений об электронных подписях объекта |
| `signing_settings()` | Возвращает глобальные настройки подсистемы ЭЦП IPS |

</details>

<details>
<summary><b><code>file_systems</code></b> — Локальные диски и каталоги сервера <b>(5)</b></summary>

| Метод | Назначение |
|---|---|
| `create_directory(path, confirm)` | Создаёт каталог по указанному пути на файловой системе СЕРВЕРА IPS (МУТАЦИЯ) |
| `find_directories(params)` | Ищет каталоги в файловой системе сервера IPS по заданным параметрам |
| `find_files(params)` | Ищет файлы в файловой системе сервера IPS по заданным параметрам |
| `is_directory_exists(path)` | Проверяет существование каталога в файловой системе сервера IPS |
| `local_drives()` | Возвращает список локальных дисков (имён томов) файловой системы сервера IPS |

</details>

<details>
<summary><b><code>auth</code></b> — Авторизация: опции входа, токены (authenticate/refresh/clone) <b>(4)</b></summary>

| Метод | Назначение |
|---|---|
| `authenticate(request, Any])` | Аутентифицирует пользователя IPS и возвращает пару токенов сессии |
| `clone_tokens(request, Any])` | Клонирует пару токенов сессии IPS, выдавая первичную и вторичную пары |
| `login_options(login_name)` | Возвращает роли и уровни доступа, доступные пользователю при входе |
| `refresh_tokens(request, Any])` | Обновляет пару токенов сессии IPS, обменивая текущую пару на новую |

</details>

<details>
<summary><b><code>imviewer</code></b> — Данные 3D-просмотрщика (сетка/сборка/инфо/состав) <b>(4)</b></summary>

| Метод | Назначение |
|---|---|
| `imviewer_assembly(object_id, blob_id, config_name)` | Возвращает данные сборки (assembly) для 3D-просмотра модели |
| `imviewer_assembly_composition(node)` | Разрешает дерево сборочного состава в imv-данные для 3D-просмотрщика |
| `imviewer_mesh(object_id, blob_id, config_name)` | Возвращает триангуляционную сетку (mesh) детали для 3D-просмотра модели |
| `imviewer_object_info(object_id, blob_id)` | Возвращает краткую информацию о 3D-объекте в blob (деталь или сборка) |

</details>

<details>
<summary><b><code>relation_queries</code></b> — Запросы состава и вхождения объекта <b>(4)</b></summary>

| Метод | Назначение |
|---|---|
| `classifier_objects(classifier_object_id)` | Возвращает идентификаторы объектов, отнесённых к узлу классификатора |
| `consist_from(object_id, recure, relation_type_id, object_type_id)` | Возвращает состав объекта — связи к объектам, из которых он состоит |
| `enters_in_version(object_id, recure, relation_type_id)` | Возвращает вхождения объекта — связи к объектам, в состав которых он входит |
| `relation_queries_relation_types()` | Возвращает справочник типов связей, определённых в IPS |

</details>

<details>
<summary><b><code>signs</code></b> — Метаданные ЭЦП: графы, ранги, параметры вывода штампа <b>(4)</b></summary>

| Метод | Назначение |
|---|---|
| `additional_sign_output_params()` | Возвращает дополнительные параметры вывода подписи (штампа ЭЦП на документе) |
| `additional_user_output_params()` | Возвращает дополнительные параметры вывода сведений о пользователе (подписанте) |
| `sign_graphs()` | Возвращает коллекцию графов подписания (схем согласования/подписания ЭЦП) |
| `sign_ranks()` | Возвращает коллекцию рангов подписи (уровней/категорий подписанта ЭЦП) |

</details>

<details>
<summary><b><code>snapshots</code></b> — Снимки состава: чтение, создание, обновление, удаление <b>(4)</b></summary>

| Метод | Назначение |
|---|---|
| `create_snapshot(snapshot, object_id)` | Создаёт новый снимок состава объекта и возвращает его идентификатор |
| `delete_snapshot(snapshot_id, confirm)` | Удаляет снимок состава объекта (РАЗРУШАЮЩАЯ операция, защищена ``confirm``) |
| `snapshot_composition(snapshot_id)` | Возвращает состав снимка объекта — список id версий вошедших в него элементов |
| `update_snapshot(snapshot_id, snapshot)` | Обновляет существующий снимок состава объекта (мутирующая операция) |

</details>

<details>
<summary><b><code>table_report</code></b> — Шаблоны и содержимое табличных отчётов <b>(4)</b></summary>

| Метод | Назначение |
|---|---|
| `report_content(object_id, params)` | Генерирует содержимое табличного отчёта для объекта IPS |
| `table_report(object_id)` | Возвращает шаблон табличного отчёта, настроенный для объекта |
| `table_report_math_total(math_total)` | Возвращает строковый итог табличного отчёта по математическому выражению |
| `update_report_template(template, Any], confirm)` | Создаёт или обновляет шаблон табличного отчёта объекта (МУТАЦИЯ) |

</details>

<details>
<summary><b><code>editing_contexts</code></b> — Контексты редактирования <b>(3)</b></summary>

| Метод | Назначение |
|---|---|
| `add_objects_to_editing_context(editing_context_id, body)` | Добавляет версии объектов в контекст редактирования (МУТИРУЮЩАЯ операция) |
| `replace_version_in_editing_context(editing_context_id, body)` | Заменяет версию объекта в контексте редактирования (МУТИРУЮЩАЯ операция) |
| `update_editing_context_objects(editing_context_id, body)` | Обновляет версии объектов в контексте редактирования (МУТИРУЮЩАЯ операция) |

</details>

<details>
<summary><b><code>search_schemes</code></b> — Схемы поиска/выборки и структура условий, правка <b>(3)</b></summary>

| Метод | Назначение |
|---|---|
| `condition_structure_info(selection_id)` | Возвращает атрибуты, по которым выборка строит условия фильтрации |
| `edit_search_scheme(object_id, request, Any], confirm)` | Перезаписывает сохранённую поисковую схему (выборку) по идентификатору объекта (МУТАЦИЯ) |
| `search_scheme(object_id)` | Возвращает сохранённую поисковую схему (выборку) по идентификатору её объекта |

</details>

<details>
<summary><b><code>attribute_history</code></b> — История значений атрибутов (чтение/удаление) <b>(2)</b></summary>

| Метод | Назначение |
|---|---|
| `attribute_history(request)` | Возвращает историю изменений значения атрибута (кто/когда/какое значение) |
| `delete_attribute_history(request, confirm)` | Удаляет историю изменений значения атрибута (РАЗРУШАЮЩАЯ операция) |

</details>

<details>
<summary><b><code>licenses</code></b> — Лицензирование: идентификатор клиента, шифрование <b>(2)</b></summary>

| Метод | Назначение |
|---|---|
| `generate_client_id()` | Генерирует на сервере новый идентификатор клиента для лицензирования IPS |
| `licenses_encrypt(data)` | Шифрует лицензионные данные на сервере и возвращает зашифрованную строку |

</details>

<details>
<summary><b><code>mail_agent</code></b> — Почтовый агент: настройки и счётчики непрочитанного <b>(2)</b></summary>

| Метод | Назначение |
|---|---|
| `mail_agent_settings()` | Возвращает текущие настройки почтового агента IPS |
| `unread_mail()` | Возвращает сводку по непрочитанным письмам почтового ящика пользователя |

</details>

<details>
<summary><b><code>measure_units</code></b> — Единицы измерения <b>(2)</b></summary>

| Метод | Назначение |
|---|---|
| `measure_unit_quantity_guids()` | Возвращает список GUID физических величин, имеющих единицы измерения |
| `measure_units()` | Возвращает полный справочник единиц измерения, определённых в IPS |

</details>

<details>
<summary><b><code>relation_types</code></b> — Связи по типу связи <b>(2)</b></summary>

| Метод | Назначение |
|---|---|
| `relation_type_relation_ids(relation_type_id)` | Возвращает идентификаторы всех связей заданного типа |
| `relation_type_relations(relation_type_id)` | Возвращает все связи заданного типа в краткой форме |

</details>

<details>
<summary><b><code>sso</code></b> — Опции и аутентификация Kerberos <b>(2)</b></summary>

| Метод | Назначение |
|---|---|
| `kerberos_auth_options()` | Возвращает опции аутентификации текущего пользователя по SPNEGO/Kerberos |
| `sso_krb5_authenticate(request, Any])` | Аутентифицирует пользователя по Kerberos/SSO и возвращает токены сессии |

</details>

<details>
<summary><b><code>users</code></b> — Текущий пользователь сессии <b>(2)</b></summary>

| Метод | Назначение |
|---|---|
| `id_helper()` | Возвращает справочник системных идентификаторов IPS для текущей сессии |
| `user_info()` | Возвращает сведения о пользователе текущей авторизованной сессии |

</details>

<details>
<summary><b><code>archives</code></b> — Архивы документов: применимость настроек <b>(1)</b></summary>

| Метод | Назначение |
|---|---|
| `archive_can_apply_settings(archive_id, body, Any])` | Проверяет, применимы ли заданные настройки типов документов к архиву (чтение) |

</details>

<details>
<summary><b><code>notify</code></b> — Уведомления <b>(1)</b></summary>

| Метод | Назначение |
|---|---|
| `send_notification(notification)` | Отправляет уведомление пользователю IPS (МУТИРУЮЩАЯ операция) |

</details>

<details>
<summary><b><code>visibilities</code></b> — Настройки видимости <b>(1)</b></summary>

| Метод | Назначение |
|---|---|
| `default_visibility_settings()` | Возвращает список дефолтных настроек видимости объектов IPS |

</details>


## Архитектура

Клиент собирается множественным наследованием mixin-классов разделов в единый `IPSClient`
(проверенный паттерн масштабируемой обёртки над API). Слои:

```
src/aioips/
├── core/            # ядро: config, exceptions, sessions, auth, request engine
├── methods/<раздел>/<метод>.py   # публичные методы-обёртки (mixin'ы)
├── schemas/<раздел>/<метод>.py   # pydantic-схемы запросов/ответов
├── common/enumerations/          # перечисления доменных значений
├── infrastructure/logging/       # структурное логирование
└── client.py        # сборка IPSClient
```

Подробнее — в Obsidian-vault: [`vault/`](vault/) (ADR, архитектура, журнал, знания).

## Разработка

Гейт качества (должен быть зелёным перед коммитом):

```bash
ruff check .
ruff format --check .
mypy src
pytest --cov=aioips --cov-branch --cov-fail-under=80
```

Юнит-тесты не ходят в сеть: HTTP-слой проверяется на локальном поддельном сервере
(`tests/conftest.py::FakeIPS`).

Стандарты разработки и процесс — в [руководстве для участников](docs/contributing.md).

## Лицензия

[MIT](LICENSE).
