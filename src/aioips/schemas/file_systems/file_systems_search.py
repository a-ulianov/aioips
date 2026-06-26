"""Схема параметров поиска по файловой системе сервера IPS.

References:
    ``POST /core/api/fileSystems/directories`` и ``POST /core/api/fileSystems/files`` —
    ``FilesSystemsSearchParametersDto``.
"""

from typing import Any

from pydantic import Field

from ..base import IPSModel


class FileSystemsSearchParameters(IPSModel):
    """Параметры поиска каталогов или файлов в файловой системе сервера IPS.

    Описывает запрос на перечисление содержимого каталога на стороне сервера
    (``Directory.EnumerateDirectories`` / ``Directory.EnumerateFiles``): корневой путь,
    шаблон имён и опции перечисления. Используется методами :meth:`find_directories`
    и :meth:`find_files`. Путь и шаблон трактуются в терминах ОС хоста IPS Server
    (например, разделители путей и буквы дисков Windows), а не машины клиента.

    Все поля необязательны: при ``None`` сервер применяет значения по умолчанию
    (например, текущий рабочий каталог и шаблон ``*``).

    Attributes:
        path: Путь к каталогу, содержимое которого перечисляется (корень поиска).
            Указывается в терминах файловой системы сервера. ``None`` — серверный
            каталог по умолчанию.
        search_pattern: Шаблон поиска имён (например, ``*.pdf`` или ``Чертёж*``).
            ``None`` — без ограничения по шаблону (эквивалент ``*``).
        options: Дополнительные опции перечисления, соответствующие
            ``System.IO.EnumerationOptions`` (например, ``RecurseSubdirectories``,
            ``MatchCasing``). Значения — строки (результат ``ToString()``). ``None`` —
            опции по умолчанию.
    """

    path: str | None = Field(default=None, description="Путь к каталогу — корень поиска")
    search_pattern: str | None = Field(
        default=None, description="Шаблон поиска имён (например, ``*.pdf``)"
    )
    options: dict[str, Any] | None = Field(
        default=None, description="Опции перечисления (System.IO.EnumerationOptions)"
    )
