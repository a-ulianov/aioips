"""Схема результата проверки применяемости записи IMBASE.

References:
    ``GET /core/api/imbase/object/{objectVersionId}/applicability`` —
    ``ImBaseApplicabilityCheckResultDto`` (внутри обёртки ``...NullableResultDto``).
"""

from pydantic import Field

from ..base import IPSModel


class ImBaseApplicabilityCheckResult(IPSModel):
    """Результат проверки применяемости (ограничительного перечня) записи IMBASE.

    «Применяемость» IMBASE определяет, разрешено ли использовать запись справочника
    (например, материал или стандартное изделие) при формировании состава изделия.
    Метод проверки возвращает статус применяемости и вспомогательный флаг для логики
    показа предупреждения.

    Когда применять: перед добавлением записи IMBASE в состав, чтобы убедиться, что
    использование не запрещено/ограничено. Отдаётся методом
    :meth:`imbase_object_applicability` (принимает id ВЕРСИИ объекта, не id объекта).

    Значения ``applicability_status`` (enum ``ApplicabilityStatusEnum`` из swagger):
    ``none``, ``noLimit`` (без ограничений), ``forbiddenUse`` (запрещено),
    ``limitedUse`` (ограниченное использование), ``totalForbiddenUse`` (полностью
    запрещено). Поле типизировано как ``str``, чтобы не отвергать значения новых
    версий API.

    Attributes:
        applicability_status: Статус применяемости записи (см. перечень значений выше).
        position_in_restriction_list: Находится ли запись уже в кэше ограничительного
            перечня. Значимо только при ``applicability_status == "limitedUse"`` для
            решения о показе сообщения; иначе может быть ``None``.
    """

    applicability_status: str = Field(description="Статус применяемости записи IMBASE")
    position_in_restriction_list: bool | None = Field(
        default=None,
        description="В кэше ограничительного перечня (значимо при limitedUse)",
    )
