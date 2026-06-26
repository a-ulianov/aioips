# Объектная модель IPS (для разработчика aioips)

- Дата: 2026-06-24
- Источник: «Руководство программиста IPS» (`<IPS-install>\Doc\IPS. Руководство программиста.pdf`,
  381 стр.) + `whatsnew_api.txt`. Документирует **.NET-ядро** (Intermech.Interfaces/Kernel),
  REST `/core/api` там НЕ описан — но REST это тонкая обёртка над тем же ядром, поэтому имена
  полей/типов ниже = лучший справочник для маппинга REST-ответов. Enum-значения сверены со
  `swagger.json` (авторитетно для REST). См. [[ips-web-api-overview]], [[gotchas]].

## Идентичность: объект ≠ версия (КЛЮЧЕВОЕ)
В IPS два уровня идентичности; их путаница — главный источник багов. **Проверено
эмпирически на проде** (object_get + сверка с БД `ims_objects`):
- **Объект:** `ObjectID` (=`F_OBJECT_ID`, BIGINT, общий для всех версий). В REST DTO это
  поле **`objectID`** (в aioips — `ObjectDto.object_id`), и GUID объекта — `objectGUID`.
  **Именно `objectID` принимают методы `object_get`/`objects_collection`/`object_info`** (путь
  `/objects/{objectId}`). Проверка: `object_get(4)` где 4=F_OBJECT_ID → объект; `object_get(5)`
  где 5=F_ID (версия) → `None`.
- **Версия объекта:** `ID` (=`F_ID`, уникален per-version) и `GUID` (GUID версии). В REST DTO —
  поле **`id`** (`ObjectDto.id`) и `guid`. По `id`/F_ID объект через `object_get` НЕ достаётся.
- `VersionID` (`F_VERSION_ID`) — порядковый номер версии (0 у базовой).
- В связях: `ProjID` родителя = его `ObjectID` (F_OBJECT_ID), `PartID` потомка = его `ID`
  (F_ID, версия) — разные пространства, см. ниже.
- ⚠️ Грабли: `relation.part_id` (F_ID/версия) НЕЛЬЗЯ напрямую подать в `object_get` (тот ждёт
  `objectID`/F_OBJECT_ID). Имена в REST местами вводят в заблуждение (напр. `projectVersionId`
  в пути composition фактически принимает ObjectID родителя).
- `IsBaseVersion` (`F_BASE_VERSION`) — базовая (актуальная) версия. `ParentVersionID` — версия-родитель.
- `ObjectVerType` (`F_OBJECT_VER_TYPE`): -1 рабочая копия / 0 обычная / 1 версия web-клиента.

Получение: `GetObject(id|guid)`, `GetObjectActualCopy`, `GetObjectBaseVersionByID`,
`GetObjectByVersionRule(id, FiltrationSettings)`. В нашей обёртке — `object_get`/`object_get_by_guid`.

## Атрибуты
Носят значения характеристик; хранятся в `IMS_OBJECT_ATTRS` (связи — `IMS_RELATION_ATTRS`):
`F_ATTRIBUTE_ID`, `F_INLIST_ID`(индекс мн.значения), `F_INTEGER_VALUE`, `F_STRING_VALUE`(NVARCHAR 450),
`F_DOUBLE_VALUE`, `F_DATE_VALUE`(UTC).

**Типы данных `FieldTypes`** (сверено со swagger, 18 значений):
`ftUnknown, ftString` (≤450), `ftInteger`(Int64), `ftDouble, ftDateTime`(хранится UTC),
`ftShortBlob, ftFile`(внешнее хранилище/vault), `ftExternalLink, ftObjectLink`(ссылка на объект),
`ftPassword`(хэш), `ftMemo`(длинный текст), `ftBlob, ftBoolean, ftMeasured`(величина+ед.изм.),
`ftAutoInc, ftSystem`(системный обяз.), `ftGuid, ftObjectLinkByID`.

- **Ссылка на объект (`ftObjectLink`/`ftObjectLinkByID`):** значение = **id объекта-цели**.
  Читать `AsInteger`/GUID (дёшево), НЕ `Value` (грузит весь объект). Так устроена ссылка
  «документ → Архив» (см. ниже).
- **Множественность `MultiValueModes`:** `singleValue, multiValues, singleValueFromList,
  multiValuesFromList`. У `…FromList` значения ограничены `GetPossibleValues()`.
- **Вычисляемость `ComputeValueModes`:** `notComputableValue, storedValue, jitValue, indexValue`.
- **Мастер-атрибут** (`MasterAttributeID`): для атрибута-ссылки — атрибут связанного объекта,
  чьё значение «подтягивается» в текущий.
- Время в **UTC**; `AsDateTime` отдаёт локальное — учитывать при сравнении.

Пакетное чтение: `GetAttributesValues(modes)` → `AttributeValues[]` (поля: AttributeID, Guid,
Name, Alias, Type, Values[], Descriptions, ReadOnly, ComputeMode). Флаги `GetAttributeValuesModes`
(IncludeName/Guid/Alias/Blobs/Descriptions/CheckWriteAccess/CheckVisibility/…).
В обёртке — `object_attributes`, `object_attributes_values`.

## Редактирование (ОБЯЗАТЕЛЬНАЯ последовательность)
Менять атрибуты можно только в правильном режиме. `ObjectModifyModes` (зависит от типа И
**текущего шага ЖЦ**): `inBase` (правка прямо в базе), `checkout` (через взятие), `createVersion`
(с созданием версии), `cantModify` (запрещено).
- **CheckOut-цикл:** `CheckOut()` → править атрибуты на рабочей копии → `CheckIn()`.
  Откат — `CancelChanges()`. Сохранить без снятия чек-аута — `SaveChanges()`. Проверка — `CheckEdit()`.
- `CheckoutBy` (0 = свободен). `ReadOnly` = правка невозможна.
- **Создание:** `GetObjectCollection(typeId)` → `Create([prototype])` → заполнить (объект в
  `IsCreationMode`) → **`CommitCreation(deleteOnException[, autoCheckOut])`** (без коммита объект
  «не существует»). Новая версия — `CreateVersion(objectID)`.
- **Удаление:** `Delete(deleteMode)`; анализ зависимостей — `IObjectsDeleteAnalyzerService`.

→ Для S3/S4 обёртки: set-атрибутов и edit требуют checkout/checkin; create требует commitCreation.

## Связи и состав
`IDBRelation`: `ProjID`(=ObjectID родителя) → `PartID`(=ID версии потомка), `RelationType`,
`PartObjectID`(ObjectID потомка, 0 если связь не по версии), собственные атрибуты связи.
**`RelationID` нестабилен** — меняется после CheckOut/CheckIn родителя; ключ = GUID связи или
тройка (ProjID, PartID, RelationType). Применяемость = тройка (тип-родителя, тип-связи, тип-потомка).
Состав — `ICompositionLoadService.LoadComposition(projID, columns, rule, childObjectTypes)`.
⚠️ В REST `composition` нужны `relationTypeId` + `partTypeIds` (см. [[gotchas]]).

## Поиск (`objects/select` ← `IDBRecords.Select`)
Условие `ConditionStructure`: `Attribute`(id/guid/системный/`""`=Caption), `AttributeSource`
(`AttributeSourceTypes`: auto/object/relation/events/history/fileStorage/snapshot/other),
`RelationalOperator`, `Value`/`Value2`, `LogicalOperator` (none/or/and/not), `GroupID` (скобки),
`Content` (`ColumnContents`: text/id/date/value/string), `TypeID`, `CaseSensitive`.
- `ColumnContents.id` — сравнивать по id (для ftObjectLink = id связанного объекта). **Так ищем
  документы архива:** тип 1742 + `attributeId=1029, equal, value=<id архива>, content=id`.
- Операторы (выборка): equal, notEqual, substring, startString, between, `entersIn`(в состав),
  `consistFrom`(состоит из), `in`/`notIn`, `inSelection`(в именованной выборке), `stringTemplate`
  (`?`/`*`), attributeExists, empty/notEmpty, lastNDays… (полный список — enum `RelationalOperator`).
- Колонки результата/пагинация — keyset: `MaxRows` + (`lastKeyValue`,`lastOrderValue`),
  признак конца `ExtendedProperties["Eof"]` (не offset!).
- **Контекст версий:** один запрос вернёт разные версии по `VersionsRule`/`FiltrationSettings`;
  `ObjectFiltrationState` в результатах. Для воспроизводимости фиксировать правило.

## Жизненный цикл
Шаги (`IMS_LC_STEPS`: `F_LC_STEP`, `F_LC_NAME`, `F_MODIFY_MODE`=режим правки на шаге, `F_FIRST`) +
переходы (`IMS_LC_LINKS`: from→to, `F_ROUTE_ID` маршрут). Текущий шаг — `IDBObject.LCStep` (get/set).
История — `GetLCHistory()`. **Разрешённость правки атрибутов зависит от режима текущего шага.**

## Файлы / архивы
Файлы — значения атрибутов: `ftFile` (внешнее файловое хранилище/vault, диск X:), `ftBlob`
(в БД), `ftShortBlob` (≤~128 КБ в `IMS_BLOBS`). Метаданные — `BlobInformation` (FileName, FileType,
BlobID, RealFileSize, ArcMethod, Author). Потоково — `IBlobReader`/`IBlobWriter`. Хэш — `GetHashFile`.
Поиск по файловым атрибутам — `AttributeSource=fileStorage`.
**Привязка «документ→Архив»** — НЕ состав/связь, а **атрибут-ссылка** на объект архива (в этой БД
атрибут «Архив» = id 1029, `ftObjectLink`). См. [[ips-web-api-overview]] и память task570.
PDM «документ↔изделие» — `IArticleService.FindArticles/FindMainDocument`.

## Подводные камни (для API-клиента)
1. Различать ID(версия)/ObjectID(объект) и GUID/ObjectGUID. Связи — по ObjectID.
2. Правка только в верном режиме (checkout→checkin), зависит от шага ЖЦ; нельзя если ReadOnly/занят.
3. Объект не существует без `CommitCreation`; при ошибке — удалять.
4. `RelationID` нестабилен — не кэшировать.
5. Ссылки читать как id, не как объект (дорого).
6. Даты в UTC.
7. Контекст версий меняет результат поиска — фиксировать правило.
8. Пагинация keyset, не offset.
9. Права/видимость влияют на состав возвращаемых атрибутов (ReadOnly).
10. ftFile требует доступного vault (X:/iSCSI); большие данные — потоком.
11. Док прямо предупреждает: «не злоупотребляйте API», сначала тест на тестовой БД.
