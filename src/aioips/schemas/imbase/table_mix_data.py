"""Схема смешанных табличных данных объекта IMBASE (таблица составного объекта).

References:
    ``POST /core/api/imbase/tableMix/{objectId}/data`` — ``TableMixDataDto``
    (без result-обёртки); записи рецептур — ``TableMixEntryDto``.
"""

from typing import Annotated, Any

from pydantic import BeforeValidator, Field

from ..base import IPSModel


def _none_to_dict(value: Any) -> Any:
    """Преобразует ``None`` в пустой словарь (IPS отдаёт ``null`` вместо ``{}``)."""
    return {} if value is None else value


_EmptyDictIfNone = BeforeValidator(_none_to_dict)


class TableMixEntryDto(IPSModel):
    """Запись (строка) рецептуры в смешанной таблице составного объекта IMBASE.

    Элемент колонки рецептуры: ключ записи, заголовок и отображаемое значение.
    Используется как элемент списков внутри :class:`TableMixDataDto.components`.

    Attributes:
        key_id: Ключ (идентификатор) записи рецептуры. По умолчанию ``""``.
        title: Заголовок (название) записи рецептуры. По умолчанию ``""``.
        displayed_value: Значение записи рецептуры в виде, готовом к показу.
            По умолчанию ``""``.
    """

    key_id: str = Field(default="", description="Ключ записи рецептуры")
    title: str = Field(default="", description="Заголовок записи рецептуры")
    displayed_value: str = Field(default="", description="Отображаемое значение записи")


class TableMixDataDto(IPSModel):
    """Смешанные (микс) табличные данные составного объекта IMBASE.

    «Таблица составного объекта» (table mix) сводит вместе рецептуры и их
    компоненты для одного объекта IMBASE. Метод-источник —
    :meth:`imbase_table_mix_data`. Структура двухуровневая:
    ``receptures`` — плоский словарь «id рецептуры → название», а
    ``components`` — словарь «id рецептуры → список входящих в неё записей»
    (каждая запись — :class:`TableMixEntryDto`). Ключи обоих словарей — строки,
    одинаковые id рецептур связывают название и состав.

    Когда применять: для отображения сводной таблицы рецептур/компонентов
    объекта-справочника. Операция чтения, объект не мутируется.

    Attributes:
        receptures: Словарь «id рецептуры (строка) → отображаемое название».
            По умолчанию пустой словарь.
        components: Словарь «id рецептуры (строка) → список записей-компонентов»
            (:class:`TableMixEntryDto`). По умолчанию пустой словарь.
    """

    receptures: Annotated[dict[str, str], _EmptyDictIfNone] = Field(
        default_factory=dict,
        description="id рецептуры → название",
    )
    components: Annotated[
        dict[str, list[TableMixEntryDto]],
        _EmptyDictIfNone,
    ] = Field(
        default_factory=dict,
        description="id рецептуры → список записей-компонентов",
    )
