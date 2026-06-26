"""Схема настроек просмотра/печати для типа объекта IPS.

References:
    ``POST /core/api/settings/view/{objectTypeId}/getSettings`` —
    ``ViewObjectTypeSettingsDto``.
"""

from typing import Any

from pydantic import Field

from ..base import IPSModel


class ViewObjectTypeSettings(IPSModel):
    """Настройки внедрения данных при просмотре/печати документов типа объекта.

    Описывает, какие сведения добавляются в результат просмотра/печати документов
    указанного типа объекта: подписи, контрольную сумму файла и набор внедряемых
    атрибутов. Возвращается методом :meth:`~aioips.IPSClient.view_print_settings`
    по идентификатору ТИПА объекта (``objectTypeId``), а не конкретного объекта.

    Семантика тристейта: булевы признаки могут быть ``None`` («значение не задано»),
    и тогда применяется унаследованная настройка вышестоящего типа. ``True``/``False``
    задают признак явно.

    Attributes:
        inject_signs: Внедрять ли подписи в результат просмотра/печати; ``None`` —
            наследовать от вышестоящего типа.
        inject_file_checksum: Внедрять ли контрольную сумму файла; ``None`` —
            наследовать от вышестоящего типа.
        injected_attributes: Описание набора внедряемых атрибутов
            (``GuidEnabledArrayDtoNullableResultDto``); структура передаётся как
            ``dict`` без распаковки. ``None`` — набор не задан (наследуется).
    """

    inject_signs: bool | None = Field(
        default=None, description="Внедрять подписи в результат просмотра/печати"
    )
    inject_file_checksum: bool | None = Field(
        default=None, description="Внедрять контрольную сумму файла"
    )
    injected_attributes: dict[str, Any] | None = Field(
        default=None, description="Набор внедряемых атрибутов (вложенный DTO)"
    )
