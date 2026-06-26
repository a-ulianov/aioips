# Слои и поток запроса

- Дата: 2026-06-24

Карта слоёв (см. [[ADR-0001-client-architecture]]):

```
IPSClient (client.py)
  └─ mixin-разделы (methods/<раздел>/<метод>.py)   ← публичные методы, возвращают схемы
       └─ APIManager._request (core/core.py)        ← авторизация + повторы + ошибки
            ├─ AuthManager (core/auth.py)           ← JWT: authenticate / refresh / 401
            ├─ SessionManager (core/sessions.py)    ← aiohttp.ClientSession
            └─ exceptions (core/exceptions.py)      ← маппинг HTTP-кода в исключение
  schemas/<раздел>/<метод>.py                       ← pydantic-модели (IPSModel + to_camel)
  common/enumerations/                              ← доменные enum'ы
  infrastructure/logging/                           ← структурное логирование
```

Поток одного вызова метода:

```mermaid
sequenceDiagram
    participant U as Пользователь
    participant M as Метод-mixin
    participant C as APIManager._request
    participant A as AuthManager
    participant S as IPS server

    U->>M: await ips.object_types()
    M->>C: _request("get", path)
    C->>A: ensure_access_token()
    alt токена нет / истёк
        A->>S: POST /authenticate (или /refreshTokens)
        S-->>A: {accessToken, refreshToken, expireTime}
    end
    A-->>C: access_token
    C->>S: GET path (Authorization: Bearer ...)
    alt 401
        C->>A: force_refresh()
        A->>S: POST /refreshTokens
        C->>S: повтор GET path
    end
    alt 5xx / 429 / сеть
        C->>C: tenacity retry (exp backoff)
    end
    S-->>C: JSON
    C-->>M: dict / list
    M-->>U: pydantic-схема
```
