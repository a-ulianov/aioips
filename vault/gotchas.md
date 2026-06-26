# Gotchas — грабли и неочевидные факты

Бегущий список. Каждый пункт: дата, факт, источник/доказательство. Без PII.

- **⚠️ swagger ≠ реальный ответ: `selectionClassificators/.../attributeValues` отдаёт МАССИВ**
  (2026-06-24). Свагер описывает ответ как одиночный `AttributeValuesDto`, но боевой сервер
  возвращает **`array<AttributeValuesDto>`** (на проде — `[]`). Метод исправлен на
  `list[AttributeValues]`. Урок: тип ответа сверять E2E на проде, не доверять `responses.200` свагера.
- **⚠️ `Config/Read*` требует ВСЕ три координаты, иначе 500 NRE** (2026-06-24). `config_read_*`
  возвращают значение только при заданных `moduleName` + `sectionID` + `paramName` (для неизвестного
  параметра отдаётся `defaultValue`). При неполном наборе сервер падает в `Object reference not set`
  (HTTP 500), а не возвращает дефолт. `GetServerOsPlatform` — без параметров, работает всегда.
  *Доказательство:* `config_read_string('Kernel', 0, 'X', default_value='def')`→'def'; без sectionID→500.

## 2026-06-24

- **Реальные ответы IPS богаче/беднее OpenAPI-схемы.** У `metadata/objectTypes` поля
  `lifetimeReserve` и `classifyType` присутствуют не у всех типов (например, отсутствуют у
  типа id=1127), хотя в swagger помечены обязательными. Вывод: в схемах ответов поля, кроме
  идентичности (`id`, `guid`, имена), делаем необязательными. *Доказательство:* живой запрос
  к серверу при первичной отладке (`ValidationError: lifetimeReserve/classifyType missing`).
  См. `schemas/metadata/object_types.py`.

- **Описания (`summary`/`description`) в `swagger.json` приходят с битой кириллицей** (`�`,
  испорчены генератором на сервере). На работу API не влияет — данные отдаются корректным
  UTF-8. Имена путей/полей англоязычны, на них и опираемся.

- **`aioresponses` несовместим с aiohttp 3.14.** `ClientResponse.__init__` получил
  обязательный kwarg `stream_writer`, которого aioresponses 0.7.9 не передаёт →
  `TypeError`. Решение: HTTP-слой тестируем настоящим локальным aiohttp-сервером
  (`tests/conftest.py::FakeIPS`), а не mock-библиотекой. *Доказательство:* трейс
  `aioresponses/core.py:197 TypeError: ... missing ... 'stream_writer'`.

- **Путь OpenAPI-спеки нестандартный:** `/swagger/1.0/swagger.json` (не `/swagger/v1/...`).
  Swagger UI: `/swagger/index.html`.

- **Кириллица в docstrings ⇒ ruff RUF001/002/003 шумят.** Отключены в `pyproject.toml`
  (проект документируется на русском — это норма, не опечатки).

- **`str, Enum` → ruff UP042.** На Python 3.13 используем `enum.StrEnum`.

- **Авторизация ≠ пользователь СУБД.** Пароль PostgreSQL-пользователя БД IPS к Web API не
  подходит — нужен пароль прикладного пользователя IPS (отдельная сущность).

- **`operationId` — надёжный источник назначения метода** (вид `Category_Action`,
  английский), т.к. `summary`/`description` повреждены. Пример: `Objects_CreateObjectVersion`.

- **Есть эндпоинт с кириллицей в самом пути:**
  `POST /core/api/objects/{objectId}/СanSetNextLCStep` — первая буква `С` кириллическая
  (operationId `Objects_CanSetNextLCStep`). При обёртке вызывать ровно этот путь (с кириллицей),
  иначе 404. Баг сервера, не опечатка спеки.

- **Чтение объектов возвращает result-обёртку** `...NullableResultDto {entity, isEntityPresent}`.
  Разворачиваем в методе → наружу `Schema | None` (см. [[ADR-0003-naming-convention]]).
  `POST /objects/collection` принимает `list[int]` (id версий) и возвращает `list[ObjectDto]`.

- **IPS отдаёт `null` вместо `[]` для пустых коллекций.** Например, `attributesValues`
  возвращает `descriptions: null`. Списочные поля схем, которые могут прийти `null`, надо
  оборачивать в `Annotated[list[X], EmptyListIfNone]` (валидатор в `schemas/base.py`),
  иначе `ValidationError: Input should be a valid list`. *Доказательство:* живой ответ
  `/objects/4/attributesValues`.

- **Создание объекта (для S4, проверено на проде raw-API):**
  - `POST /core/api/objects` (CreateObjectDto `{objectType, attributes:[AttributeDto], contextRule, currentProjectDto}`)
    возвращает полный `ObjectDto` с **отрицательным временным `objectID`** и `isCreationMode=true`.
  - Объект не существует «по-настоящему», пока не вызван `POST /objects/{id}/commitCreation`
    (`{deleteOnException, autoCheckout, contextRule, relatedObjectIds}`).
  - **commitCreation учитывает обязательного родителя:** типы с ограничением применяемости
    (напр. «Папка рабочего стола») требуют размещения в допустимом родителе (через
    `relatedObjectIds`/контекст) — иначе 500 «должен обязательно входить в один из объектов типов…».
  - `deleteOnException=true` сам удаляет временный объект при ошибке коммита → мусор не остаётся
    (проверено: после неудачного commit `object_get(tempId)` → None). Незакоммиченные temp'ы не персистятся.
  - Цикл правки существующего: `checkOut` → set-атрибуты → `checkIn`/`saveChanges`, откат — `cancelChanges`
    (полностью обратим — безопасный способ тестировать запись без создания/удаления).
  - Удаление: `POST /objects/{id}/delete?deleteMode=0` (НЕ DELETE-метод; шли тело — иначе 415).
  - ⚠️ **POST checkOut/checkIn/saveChanges/delete требуют тело** (хотя бы `{}`): без тела → 415
    Unsupported Media Type. В обёртке слать `json={}`.
  - ⚠️ **checkOut возвращает id РАБОЧЕЙ КОПИИ** (`result` в `Int64ProcessResultWithLogInfoDto`,
    отрицательный id). Запись атрибутов (`object_set_attribute_values` и пр.) надо вызывать на
    **id рабочей копии**, НЕ на id базового объекта — иначе 400 «Для изменения объекта … нужна
    рабочая копия». Полный цикл (проверено на проде, write-метод подтверждён):
    `create → commitCreation(result.objectId — новый положительный id) → checkOut(→ working_copy)
    → object_set_attribute_values(working_copy, …) → checkIn(working_copy)` → значение сохраняется.
  - Тип **1116 «Комментарий»** — root-creatable (коммитится без родителя), удобен как одноразовый
    тест-объект. `commitCreation` возвращает новый положительный id в `result.objectId` (строчная!).

- **Политика тестирования на проде:** операции **чтения** проверяем прямо на боевом сервере
  (через env-креды, не в репо). Для **записи** — допускается создать временный объект,
  поэкспериментировать и **обязательно удалить** его (не оставлять мусор). По договорённости с владельцем.

- **⚠️ Непоследовательный casing ключей JSON.** IPS сериализует имена .NET-свойств политикой
  camelCase (строчная только первая буква), из-за чего акронимы-суффиксы остаются заглавными:
  `objectID`, `versionID`, `ownerID`, `objectGUID`, `projectID`, `siteID`. Но **между разными
  DTO casing разный**: `currentUsers/userInfo` отдаёт `userVersionId` (строчная), а `ObjectDto`
  — `versionID` (заглавная); `QuickObjectInfo` — `objectTypeID`, но `versionGuid`.
  Поэтому генератор `to_camel` (`object_id`→`objectId`) для таких полей **молча теряет данные**
  (поле уедет в `extra=ignore`, останется `None`). **Правило: на каждое поле с акронимом-ID/GUID
  ставим явный `alias`, равный точному ключу JSON из спеки.** Проверять casing по `swagger.json`
  для каждого DTO, не доверять генератору. *Доказательство:* `ValidationError: object_id missing`
  при чтении объекта, пока не проставили `alias="objectID"`.

- **⚠️ «GET с телом» в IPS Web API — swagger обязателен, метод HTTP не показателен** (2026-06-24).
  Часть GET-эндпоинтов на самом деле требует **тело запроса** и/или обязательные query-параметры, а
  без них сервер отвечает **415 Unsupported Media Type** (нет тела) или **400** (нет обязательного
  query). Подтверждено на проде (Round 6):
  - `cryptoSigning/objectEncodedHash` (GET) — тело `CryptoProviderInfoDTO` + обязательные
    `graph`,`algId`. Без тела → 415; с телом → корректная валидация query.
  - `cryptoSigning/signInfoStream` (GET) — `graph` ОБЯЗАТЕЛЕН (без него 400; с ним 200, тело может
    быть `null` → возвращаем `''`, а не строку `"None"`).
  - `discussions/getMessages` (GET) — тело `array[MessageIdDto]` (дозагрузка сообщений по id-листу),
    а не безаргументная лента. Без тела → 415.
  **Правило: перед реализацией метода сверять в `swagger.json` НЕ только `parameters`, но и наличие
  `requestBody` и `required:true` у query — даже для GET.** Субагенту явно указывать проверять оба.

- **`str(data)` на строково-возвращающих методах: коэрсить `None`→`''`** (2026-06-24). Если IPS на
  200 отдаёт пустое (`null`) тело, наивный `return str(data)` даёт литерал `"None"`. Для строковых
  ответов (`signInfoStream`, `objectEncodedHash`) — `"" if data is None else str(data)`.

## Кампания полного покрытия (2026-06-25..26)

- **No-body POST без `json` → 415 Unsupported Media Type** (проверено на проде многократно:
  favorites add/remove, tableMix, set_base_calendar, briefcase). ASP.NET ждёт Content-Type даже при
  пустом теле. **Правило: для POST-эндпоинтов без requestBody всегда слать `json={}`** (НЕ вызывать
  `_request` без `json`). DELETE без тела — обычно ОК без json.

- **Сервер отдаёт `null` вопреки swagger** (2026-06-25). `imbase/favorites/.../add` по swagger
  возвращает `FavoriteFolderDto`, а прод — `null` → `ValidationError`. **Правило: для DTO-возвратов
  делать `Schema | None` / `if not isinstance(data, dict): return None`**, не доверять swagger о
  непустоте ответа. Аналогично `objects_select_by_id` — стабильный серверный 500 при идентичном теле
  с рабочим `objects_select_request` (серверная особенность билда, не баг обёртки).

- **★ Файловые/атрибутные МУТАЦИИ требуют id РАБОЧЕЙ КОПИИ, не базовый ObjectID** (2026-06-25,
  ключевая находка). `add_object_file`/`update_object_file`/`delete_object_file`/`swap_object_files`:
  объект должен быть на `object_check_out`, и в `object_id` передаётся РЕЗУЛЬТАТ checkout (id рабочей
  копии, на проде **ОТРИЦАТЕЛЬНЫЙ**), НЕ базовый ObjectID. На базовый id → 400 «выполните checkOut».
  *Доказано:* `add(base=1381324)`→400, `add(working_copy=-1381324)`→blob_id=189965. Общий паттерн
  правки атрибутов через REST.

- **Тип объекта для тестов файлов: 1742, не 1116** (2026-06-25). Тип 1116 (Комментарий) НЕ имеет
  файловых атрибутов; тип **1742** (Чертёж PDF) имеет ftFile-атрибуты **1002/18104/17911** и создаётся
  standalone. Для безопасных read/lifecycle тестов — 1116; для файлов — 1742. Реальный объект с
  данными для выборок: `1311983`.

- **bool в query → yarl/aiohttp падает** (2026-06-26). `params={"withFile": True}` →
  `TypeError: value should be str, int or float, got bool`. **Правило: bool в query сериализовать
  `str(x).lower()` → "true"/"false"** (как делают существующие методы для `isNeedToLog...`).

- **`ObjectSelectRequest.attributes` — ТОЛЬКО значения enum `ObligatoryObjectAttributes`** (2026-06-25).
  69 значений (`f_OBJECT_NAME`, `f_OWNER_CAPTION`, `f_VERSIONS_COUNT`…). Произвольное имя (напр.
  `"caption"`) → 400. `f_OBJECT_NAME` валиден, `caption` — НЕТ (есть `f_OWNER_CAPTION`).

- **Серверный 500 NRE на пустом/stateless вводе** (2026-06-25). `object_type_composition` требует
  НЕПУСТОЙ `attribute_ids` (пустой → 500 «Value cannot be null»); `metadata_select` — валидное имя
  таблицы метаданных; visibility/checkout-сервисы — предзагрузку состояния. Машинерия обёртки верна;
  500 — серверная бизнес-логика. Документировать в Notes метода.

- **Sign-settings и documents: путь `/api`, НЕ `/core/api`** (2026-06-25). `graph_signs` (штампы ЭЦП)
  и раздел `documents` бьют по `/api/...`. Сверять префикс по существующим методам раздела, не
  предполагать `/core/api`. Запись sign-settings СТРОГО валидирует id шага ЖЦ (шаг 5 → 400), тогда
  как чтение ЛОЯЛЬНО (отдаёт `[]` на невалидный id) — для write-теста брать реальный lifecycle id.

- **Коллизии bare-имён методов в MRO** (2026-06-25). Все методы в одном namespace `IPSClient`. Раздел
  forms-агента назвал `forms_find_*` — поправлено на bare (`find_collection`); но `samples.add_message`
  коллидировал с `discussions.add_message` (discussions раньше в MRO → перекрыл) → переименован в
  `add_sample_message`. **Правило: grep `async def <name>\b` по всему `methods/` перед именованием;
  bare-имя должно быть уникально глобально.**

- **wfAttachments — это раздел `workflow`, не отдельный** (2026-06-25). `wfAttachments/*` эндпоинты
  кладутся в `methods/workflow/` (там уже `wf_attachments.py` и др.). Перед созданием «нового раздела»
  проверять, нет ли его методов под другим именем каталога.

- **★ Survey непокрытого по путям даёт МАССОВЫЕ false-positive/negative** (ключевая находка).
  Многопараметрические f-string пути (`f"/objectTypes/{tid}/lifecycleSchemeSteps/{sid}/..."`) не
  матчатся регуляркой нормализации; operationId в код буквально не пишется. Итог: «8 непокрытых
  writes» оказались ВСЕ в коде (operationId присутствует). **Правило: сверять покрытие ДВУМЯ
  признаками (путь-литерал ИЛИ operationId-в-коде) — см. `scripts/survey_uncovered.py`. Перед
  реализацией «непокрытого» — обязательная проверка субагентом на дубль** (несколько раундов
  реализовали дубли metadata/security, пришлось удалять).

- **`SecurityWithChildsSettingsDto` для update step-security** (2026-06-25). `update_object_type_
  lifecycle_scheme_step_security` принимает не `SecurityDto`, а надмножество с `isNeedToApplyToChilds`.
  Принимать тело как `Security | dict` — флаг передавать через dict (write-same-back пробрасывает
  сырой dict без потери полей).

- **Auth: публичные обёртки authenticate/refresh/clone — конфликта нет** (2026-06-26). `AuthManager` в
  ядре использует ПРИВАТНЫЕ `_authenticate_locked`/`_refresh_locked`; публичные имена свободны.
  Эндпоинты те же, что внутри ядра.

- **FakeIPS: ловить `UnicodeDecodeError`** (2026-06-26). Тест multipart с бинарным телом (PNG `\x89...`)
  валит `request.json()` → `UnicodeDecodeError` (не пойман) → fake-сервер 500. Добавлено в except.
  FakeIPS отдаёт bytes-тело, если `body` — `bytes` (для тестов raw_bytes-загрузок).

- **ЯДРО: режим `raw_bytes=True`** (2026-06-26). Для бинарных загрузок (Bridge/Download/App,
  samples/values/asFile, documentEditor-блобы) — `_request(..., raw_bytes=True)` возвращает `bytes`
  (без JSON-разбора при статусе <400; ошибки >=400 по-прежнему разбираются как JSON для маппинга).
  *Доказано:* `bridge_download_app('win-x64')` → 51 МБ Windows-EXE (MZ-заголовок).

- **★ Паттерн write-same-back для безопасной прод-валидации config-записей** (ключевой приём).
  Для опасных/config мутаций с парным read: прочитать СЫРОЙ ответ (`_request` GET) → записать те же
  байты обратно (метод принимает `Schema | dict`, передаём dict) → перечитать → `assert raw == raw2`.
  Нулевое изменение состояния, но POST-машинерия (сериализация/транспорт) подтверждена на проде.
  Применено: calendars, settings view/print, graph_signs, documents, **security update прав** (15971
  байт, 85 permissions, unchanged:True). Самый безопасный способ E2E мутаций.

- **`IPS_ROLE_ID=10` обязателен для authenticate** (см. [[aioips-e2e-recipe]] в памяти). Без roleID
  шаг `POST /core/api/Auth/authenticate` → 403. Креды/рецепт E2E — в памяти сессии, не в репо.

- **Генераторы доков: 2 бага парсера** (2026-06-26). (1) брал только ПЕРВЫЙ `async def` файла →
  терял 2-й метод в файлах с двумя (`objects_select_by_id`); (2) не учитывал raw-docstrings `r"""` →
  пропускал `imbase_rtf_*`. Исправлено в `scripts/gen_readme.py`/`gen_reference.py` (регулярка ловит
  все методы + `r?"""`). **Доки автогенерируются — запускать оба скрипта + `audit_docs.py` каждый раунд.**
