"""Метод проверки возможности включения таблицы справочника в состав типа объекта."""

from typing import Any

from ...core import APIManager


class ImBaseTableCheckCompositionMixin(APIManager):
    """Реализует ``GET .../table/{tableId}/checkComposition/{parentObjectTypeId}``.

    operationId ``ImBase_CheckTableCompositionPossibility``.
    """

    async def imbase_table_check_composition(
        self: "ImBaseTableCheckCompositionMixin",
        table_id: int,
        parent_object_type_id: int,
    ) -> dict[str, Any]:
        """Проверяет возможность включения таблицы справочника в состав типа объекта.

        Перед тем как добавить табличную часть справочника в состав объектов некоторого
        ТИПА, нужно убедиться, что это допустимо. Метод выполняет такую проверку и
        возвращает её результат (возможность и, при наличии, причины запрета).

        Когда применять: на этапе конфигурирования состава — до фактического добавления
        таблицы в тип объекта. Предусловий нет (операция чтения/проверки, без побочных
        эффектов).

        Args:
            table_id: Идентификатор таблицы справочника (``tableId``).
            parent_object_type_id: Идентификатор ТИПА объекта-родителя
                (``parentObjectTypeId``, ``ObjectTypeID`` — id-пространство ТИПОВ
                объектов, не id объекта/версии), в состав которого проверяется включение.

        Returns:
            Опаковая структура результата проверки как ``dict[str, Any]`` по DTO
            ``TableCompositionCheckResultDto`` (флаг возможности и сопутствующие сведения).
            Структура неоднородная, детально не типизируется. Пустой ``dict`` — если
            сервер вернул не-объект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.imbase_table_check_composition(204, 1742)
                print(result)

        Notes:
            operationId ``ImBase_CheckTableCompositionPossibility``; путь
            ``GET /core/api/imbase/table/{tableId}/checkComposition/{parentObjectTypeId}``
            (``TableCompositionCheckResultDto``, без result-обёртки).
        """
        data = await self._request(
            "get",
            f"/core/api/imbase/table/{table_id}/checkComposition/{parent_object_type_id}",
        )
        return data if isinstance(data, dict) else {}
