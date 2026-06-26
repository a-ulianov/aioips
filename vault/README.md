# Vault aioips — индекс

Проектная документация в формате Obsidian (вики-ссылки `[[...]]`, абсолютные даты, без PII).

## Architecture
- [[ADR-0001-client-architecture]] — почему mixin-клиент и слои
- [[ADR-0002-auth-token-lifecycle]] — управление JWT: lazy-auth, refresh, 401-retry
- [[ADR-0003-naming-convention]] — имена методов/схем из адреса после `/api/`
- [[layers]] — карта слоёв и поток запроса (mermaid)

## Knowledge — объектная модель
- [[ips-object-model]] — объектная модель IPS из «Руководства программиста»: идентичность
  объект/версия, атрибуты (FieldTypes), редактирование (checkout/checkin), связи, поиск, ЖЦ, файлы, грабли

## API
- [[auth]] — авторизация IPS: эндпоинты, поля, схема токенов

## Knowledge
- [[ips-web-api-overview]] — обзор IPS Server Web API (объём, структура путей, особенности)
- [[performance-baseline]] — замеры на проде: латентность, req/sec, скорость данных (2026-06-26)

## Инструменты
- `scripts/` (в корне репо) — генераторы доков (`gen_readme.py`, `gen_reference.py`), аудит
  (`audit_docs.py`), поиск непокрытого (`survey_uncovered.py`). См. `scripts/README.md`.

## Gotchas
- [[gotchas]] — бегущий список граблей и неочевидных фактов (см. раздел «Кампания полного покрытия»)
