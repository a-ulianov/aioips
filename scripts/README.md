# scripts/ — служебные генераторы и аудиторы

Скрипты сопровождения проекта. Запускаются из корня репозитория интерпретатором venv
(`.venv/Scripts/python.exe scripts/<имя>.py`). Не имеют внешних зависимостей сверх stdlib.

## Документация (запускать ПОСЛЕ КАЖДОГО раунда добавления методов)

| Скрипт | Что делает |
|---|---|
| `gen_readme.py` | Регенерирует секцию «## Реализованные методы» в `README.md` из кода (свёрнутые списки по разделам). |
| `gen_reference.py` | Регенерирует `docs/reference/all-methods.md` — полный плоский справочник всех методов (для MkDocs). |
| `audit_docs.py` | Проверяет, что все реализованные методы попали в README и docs/reference. Должно быть **0 пропущенных**. |

**Рабочий цикл документации:**
```bash
.venv/Scripts/python.exe scripts/gen_readme.py
.venv/Scripts/python.exe scripts/gen_reference.py
.venv/Scripts/python.exe scripts/audit_docs.py   # ожидаем 0 пропущенных
.venv/Scripts/python.exe -m mkdocs build --strict
```

> Эти два генератора — **единственный источник правды** для списков методов. Курируемые
> страницы `docs/reference/{objects,files,...}.md` — это narrative-гайды (дополняют, не дублируют).
> Раньше доки отставали, т.к. генератор README брал только первый `async def` файла и не учитывал
> raw-docstrings `r"""` — оба бага исправлены (см. шапки скриптов).

## Покрытие API

| Скрипт | Что делает |
|---|---|
| `survey_uncovered.py` | Находит НЕпокрытые эндпоинты swagger. Сверяет ПУТЬ и operationId — иначе масса ложных «непокрытых». |

```bash
# нужен swagger (не в репо): по умолчанию ../api/ips_swagger.json или $IPS_SWAGGER
.venv/Scripts/python.exe scripts/survey_uncovered.py --writes-only          # только POST/PUT/DELETE
.venv/Scripts/python.exe scripts/survey_uncovered.py security metadata       # по разделам
```

⚠️ **Грабли (см. `vault/gotchas.md`):** поиск непокрытого ТОЛЬКО по нормализованным путям даёт
массовые false-positive/negative (многопараметрические f-string пути не матчатся; operationId не
пишется буквально). `survey_uncovered.py` сверяет ОБА признака. Перед реализацией «непокрытого»
эндпоинта **всегда** перепроверяйте grep'ом operationId/путь — несколько раундов в прошлом
реализовали дубли, которые пришлось удалять.
