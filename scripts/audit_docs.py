"""Аудит: все ли реализованные методы попали в README и docs/reference.

    python scripts/audit_docs.py

После каждого раунда + ``gen_readme.py``/``gen_reference.py`` должно быть 0 пропущенных.
"""

import glob
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)

methods: set[str] = set()
for f in glob.glob("src/aioips/methods/**/*.py", recursive=True):
    if f.endswith("__init__.py"):
        continue
    for m in re.finditer(r"async def ([a-z][a-z0-9_]*)\(", open(f, encoding="utf-8").read()):
        if not m.group(1).startswith("_"):
            methods.add(m.group(1))

ref = "".join(open(f, encoding="utf-8").read() for f in glob.glob("docs/reference/*.md"))
readme = open("README.md", encoding="utf-8").read()
ref_names = set(re.findall(r"`([a-z][a-z0-9_]*)\(", ref))
readme_names = set(re.findall(r"`([a-z][a-z0-9_]*)\(", readme))

print(f"методов в коде: {len(methods)}")
print(f"в docs/reference: {len(methods & ref_names)}  | пропущено: {len(methods - ref_names)}")
print(f"в README: {len(methods & readme_names)}  | пропущено: {len(methods - readme_names)}")
for label, missing in (("reference", methods - ref_names), ("README", methods - readme_names)):
    if missing:
        print(f"  ОТСУТСТВУЮТ в {label}: {sorted(missing)[:40]}")
