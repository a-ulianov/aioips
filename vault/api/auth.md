# API: авторизация IPS

- Дата: 2026-06-24

Реализация — [[ADR-0002-auth-token-lifecycle]]. Раздел `/core/api/Auth/*`.

## Эндпоинты

| Метод | Путь | Назначение |
|---|---|---|
| GET | `/core/api/Auth/logins/{loginName}/options` | Роли и уровни доступа логина (без пароля) |
| POST | `/core/api/Auth/authenticate` | Логин/пароль → пара токенов |
| POST | `/core/api/Auth/refreshTokens` | Текущая пара → новая пара |
| POST | `/core/api/sso/krb5/authenticate` | Единый вход по Kerberos (если включён) |

## Тело `authenticate` (AuthRequestDTO)

```json
{
  "loginName": "<логин>",
  "password": "<пароль>",
  "passwordType": "plainText",   // или "base64Text"
  "roleID": 10,
  "accessLevelID": 0
}
```

## Ответ (ApiTokensDTO)

```json
{ "accessToken": "<JWT>", "refreshToken": "<JWT>", "expireTime": "<ISO 8601>" }
```

`refreshTokens` принимает **весь** `ApiTokensDTO` (accessToken + refreshToken + expireTime)
и возвращает новый. Все вызовы API — с заголовком `Authorization: Bearer <accessToken>`.

## Опции входа (AuthOptionsDTO)

```json
{
  "roles":        [ { "id": 10, "name": "Администратор" }, ... ],
  "accessLevels": [ { "id": 0, "name": "Обычный" }, ... ]
}
```

Используется для резолвинга `role_name` → `roleID`, а также чтобы заранее показать
пользователю доступные роли.

## Ошибки

Ответ об ошибке — `ApiProblemDetails`: `{type, title, status, detail, instance}`. Маппинг
кода в исключение — `core/exceptions.py::exception_from_response`. `401` на защищённом
эндпоинте трактуется ядром как сигнал к обновлению токена (см. [[ADR-0002-auth-token-lifecycle]]).
