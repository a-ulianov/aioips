"""Генерирует полный справочник всех методов -> docs/reference/all-methods.md.

Запускать ПОСЛЕ КАЖДОГО раунда (вместе с ``gen_readme.py``):

    python scripts/gen_reference.py

Гарантирует, что документация сайта (MkDocs) не отстаёт от реализации: страница
пересобирается из кода. Якоря разделов — с подчёркиваниями (MkDocs: ``## attribute_history``
-> ``#attribute_history``, НЕ ``-history``).
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_readme import DESC, collect  # noqa: E402


def main() -> None:
    sec_methods = collect()
    total = sum(len(set(v)) for v in sec_methods.values())
    order = sorted(sec_methods)

    out = ["# Полный справочник методов", ""]
    out.append(
        f"Автогенерируемый перечень всех **{total} методов** клиента `aioips` в "
        f"**{len(sec_methods)} разделах**. Страница пересобирается из кода "
        "(`python scripts/gen_reference.py`), поэтому всегда соответствует реализации. "
        "Подробные описания «что/когда/как» — в docstring каждого метода (MCP-grade)."
    )
    out.append("")
    out.append('!!! note "Соглашения"')
    out.append(
        "    Имена выводятся из адреса эндпоинта "
        "([ADR-0003](../architecture.md)). Разрушающие операции защищены `confirm=True`. "
        "`object_id` в файловых/атрибутных мутациях — id рабочей копии из "
        "`object_check_out` (см. docstring)."
    )
    out.append("")
    out.append("| Раздел | Методов |")
    out.append("|---|---|")
    for sec in order:
        out.append(f"| [`{sec}`](#{sec}) | {len(set(sec_methods[sec]))} |")
    out.append("")
    for sec in order:
        methods = sorted(set(sec_methods[sec]))
        out.append(f"## {sec}")
        out.append("")
        if DESC.get(sec):
            out.append(f"*{DESC[sec]}.*")
            out.append("")
        out.append("| Метод | Назначение |")
        out.append("|---|---|")
        for name, params, summ in methods:
            out.append(f"| `{name}({params})` | {summ} |")
        out.append("")

    os.makedirs("docs/reference", exist_ok=True)
    open("docs/reference/all-methods.md", "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("wrote docs/reference/all-methods.md:", total, "methods,", len(sec_methods), "sections")


if __name__ == "__main__":
    main()
