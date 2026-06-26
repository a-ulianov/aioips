"""Регенерирует секцию «## Реализованные методы» в README.md из кода.

Запускать ПОСЛЕ КАЖДОГО раунда добавления методов (вместе с ``gen_reference.py``):

    python scripts/gen_readme.py

Особенности парсера (важные грабли):
- захватывает ВСЕ ``async def`` в файле (а не только первый) — файлы с 2 методами
  (``objects_select_request.py`` и т.п.) иначе теряют второй;
- учитывает raw-docstrings ``r\"\"\"`` (префикс ``r?``) — иначе методы с экранами в
  docstring (``imbase_rtf_*``) пропускаются.
Без аргументов; печатает итоговое число методов/разделов.
"""

import glob
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)

DESC = {
    "auth": "Авторизация: опции входа, токены (authenticate/refresh/clone)",
    "users": "Текущий пользователь сессии",
    "objects": "Объекты: чтение, поиск, запись, жизненный цикл, состав, версии",
    "object_types": "Экземпляры объектов по типу и определения типов (контроллер objectTypes)",
    "metadata": "Метамодель: типы/атрибуты/связи, применяемость, ЖЦ, дерево типов",
    "relations": "Связи: чтение, атрибуты, создание/удаление, расширенный поиск",
    "relation_queries": "Запросы состава и вхождения объекта",
    "relation_types": "Связи по типу связи",
    "security": "Права доступа: чтение, проверки, восстановление доступа админа, запись прав",
    "forms": "Формы и виджеты, пользователи и группы, цвета, предметные области, find*",
    "files": "Файловые атрибуты: загрузка/прикрепление/удаление, таблицы, прототипы",
    "documents": "Прототипы и настройки документов",
    "document_editor": "Редактор документов: буфер, свойства, шрифты, содержимое, формулы",
    "calendars": "Производственные и пользовательские календари, фильтры, запись",
    "improjects": "Проекты и задачи (Gantt): чтение + создание/правка/удаление/исполнение",
    "imbase": "Справочная система: каталоги, индексы, поиск, избранное, конвертеры",
    "imviewer": "Данные 3D-просмотрщика (сетка/сборка/инфо/состав)",
    "discussions": "Обсуждения объектов: чтение и запись сообщений, изображения",
    "crypto_signing": "ЭЦП: настройки, сведения о подписях, хэш, создание подписей",
    "signs": "Метаданные ЭЦП: графы, ранги, параметры вывода штампа",
    "graph_signs": "Настройки штампов ЭЦП (ранги/архивы/уровни и шаги ЖЦ): чтение и запись",
    "snapshots": "Снимки состава: чтение, создание, обновление, удаление",
    "selection_classificators": "Классификаторы выбора: чтение и включение/исключение объектов",
    "search_schemes": "Схемы поиска/выборки и структура условий, правка",
    "config": "Чтение параметров конфигурации сервера",
    "settings": "Настройки и права пользователя, настройки просмотра/печати, данные безопасности",
    "attribute_history": "История значений атрибутов (чтение/удаление)",
    "briefcase": "Портфель: статус, проверка метаданных, экспорт/импорт объектов",
    "bridge": "Клиентский мост: настройки, плагины, действия запуска, temp-файлы, загрузки",
    "workflow": "Процессы: переменные, вложения активности (создание/прикрепление)",
    "table_report": "Шаблоны и содержимое табличных отчётов",
    "visibilities": "Настройки видимости",
    "file_systems": "Локальные диски и каталоги сервера",
    "licenses": "Лицензирование: идентификатор клиента, шифрование",
    "mail_agent": "Почтовый агент: настройки и счётчики непрочитанного",
    "measure_units": "Единицы измерения",
    "sso": "Опции и аутентификация Kerberos",
    "archives": "Архивы документов: применимость настроек",
    "docs": "Типы/суффиксы документов, настройки, наследование",
    "samples": "Демо-API сообщений и значений: CRUD, выборки, файловые значения",
    "editing_contexts": "Контексты редактирования",
    "notify": "Уведомления",
}

METHOD_RE = re.compile(
    r'async def ([a-z][a-z0-9_]*)\((.*?)\)\s*->.*?:\s*\n\s*r?"""(.*?)(?:\n|""")',
    re.S,
)


def params_of(raw: str) -> str:
    parts = [p.strip().split(":")[0].split("=")[0].strip() for p in raw.split(",")]
    return ", ".join(p for p in parts if p and p not in ("self", "*"))


def collect() -> dict[str, list[tuple[str, str, str]]]:
    sec_methods: dict[str, list[tuple[str, str, str]]] = {}
    for f in sorted(glob.glob("src/aioips/methods/**/*.py", recursive=True)):
        if os.path.basename(f).startswith(("__init__", "_")):
            continue
        txt = open(f, encoding="utf-8").read()
        sec = f.split("methods" + os.sep)[1].split(os.sep)[0]
        for name, raw, doc in METHOD_RE.findall(txt):
            summ = re.sub(r"\s+", " ", doc.strip()).rstrip(".")
            sec_methods.setdefault(sec, []).append((name, params_of(raw), summ))
    return sec_methods


def main() -> None:
    sec_methods = collect()
    total = sum(len(set(v)) for v in sec_methods.values())
    order = sorted(sec_methods, key=lambda s: -len(sec_methods[s]))

    out = ["## Реализованные методы", ""]
    out.append(
        f"Клиент покрывает **{total} методов** в **{len(sec_methods)} разделах** IPS Server "
        "Web API. Каждый метод снабжён MCP-grade docstring и (где применимо) прод-проверен на "
        "боевом сервере."
    )
    out.append("")
    out.append(
        "Имена выводятся из адреса эндпоинта (см. "
        "[конвенцию имён](docs/contributing.md)); разрушающие операции "
        "защищены гейтом `confirm=True`. Полный плоский список — "
        "[docs/reference/all-methods.md](docs/reference/all-methods.md). Разделы свёрнуты:"
    )
    out.append("")
    for sec in order:
        methods = sorted(set(sec_methods[sec]))
        out.append("<details>")
        out.append(
            f"<summary><b><code>{sec}</code></b> — {DESC.get(sec, '')} "
            f"<b>({len(methods)})</b></summary>"
        )
        out.append("")
        out.append("| Метод | Назначение |")
        out.append("|---|---|")
        for name, params, summ in methods:
            out.append(f"| `{name}({params})` | {summ} |")
        out.append("")
        out.append("</details>")
        out.append("")

    new_section = "\n".join(out)
    readme = open("README.md", encoding="utf-8").read()
    m = re.search(r"## Реализованные методы.*?(?=\n## )", readme, re.S)
    readme = readme[: m.start()] + new_section + "\n" + readme[m.end() :]
    open("README.md", "w", encoding="utf-8", newline="\n").write(readme)
    print("OK methods:", total, "sections:", len(sec_methods))


if __name__ == "__main__":
    main()
