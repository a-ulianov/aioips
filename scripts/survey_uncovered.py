"""Точный поиск НЕпокрытых эндпоинтов IPS Web API (по operationId).

    python scripts/survey_uncovered.py [--swagger PATH] [--writes-only] [SECTION ...]

ВАЖНО (грабли, см. vault/gotchas.md): поиск непокрытого по НОРМАЛИЗОВАННЫМ ПУТЯМ даёт
массовые false-positive/negative — многопараметрические f-string пути
(``/objectTypes/{}/lifecycleSchemeSteps/{}/...``) не матчатся регуляркой, а operationId
в коде обычно не пишется буквально. Поэтому этот скрипт сверяет ДВУМЯ способами и считает
эндпоинт покрытым, если совпал ХОТЯ БЫ ОДИН: (1) нормализованный путь как строковый литерал
в коде, ИЛИ (2) operationId присутствует в коде/docstring. Это убирает ложные «непокрытые».

Swagger НЕ в репозитории (большой, внешний). По умолчанию ищется в ``../api/ips_swagger.json``
(соседний проектный каталог) или в ``$IPS_SWAGGER``.
"""

import glob
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)


def find_swagger() -> Path:
    if "--swagger" in sys.argv:
        return Path(sys.argv[sys.argv.index("--swagger") + 1])
    env = os.environ.get("IPS_SWAGGER")
    if env:
        return Path(env)
    for cand in (ROOT.parent / "api" / "ips_swagger.json", ROOT / "ips_swagger.json"):
        if cand.exists():
            return cand
    sys.exit("swagger не найден: укажите --swagger PATH или IPS_SWAGGER env")


def norm(p: str) -> str:
    return re.sub(r"\{[^}]+\}", "*", p).rstrip("/")


def main() -> None:
    writes_only = "--writes-only" in sys.argv
    sections = [a for a in sys.argv[1:] if not a.startswith("--") and a != find_swagger().name]
    spec = json.loads(find_swagger().read_text(encoding="utf-8"))
    code = "".join(
        open(f, encoding="utf-8").read()
        for f in glob.glob("src/aioips/methods/**/*.py", recursive=True)
    )

    lit = set()
    for m in re.finditer(r"""['"`](/(?:core/)?api/[^'"`]+)""", code):
        n = norm(m.group(1))
        lit.add(n)
        lit.add(n.replace("/core/api", "/api"))

    methods = ("post", "put", "delete") if writes_only else ("get", "post", "put", "delete")
    g: dict[str, list[str]] = defaultdict(list)
    for path, ops in spec["paths"].items():
        sec = re.sub(r"^/(core/)?api/", "", path).split("/")[0]
        if sections and sec not in sections:
            continue
        for meth in methods:
            if meth not in ops:
                continue
            n = norm(path)
            op = ops[meth].get("operationId") or ""
            covered = ({n, n.replace("/core/api", "/api")} & lit) or (op and op in code)
            if covered:
                continue
            g[sec].append(f"{meth.upper()} {path.split('/api/')[-1]}  | {op}")

    total = sum(len(v) for v in g.values())
    for sec in sorted(g, key=lambda k: -len(g[k])):
        print(f"=== {sec} ({len(g[sec])}) ===")
        for e in g[sec]:
            print("  " + e)
    print(f"\nИТОГО непокрыто (operationId+path): {total}")
    print("(оставшееся — обычно бинарные потоки/демо; сверяйте operationId вручную)")


if __name__ == "__main__":
    main()
