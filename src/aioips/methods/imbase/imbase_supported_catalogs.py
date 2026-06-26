"""Метод подбора каталогов IMBASE по типу объекта и типу атрибута."""

from typing import Any

from ...core import APIManager


class ImBaseSupportedCatalogsMixin(APIManager):
    """Реализует ``GET /core/api/imbase/catalogs/supported`` (``ImBase_GetSupportedCatalogs``)."""

    async def imbase_supported_catalogs(
        self: "ImBaseSupportedCatalogsMixin",
        object_type_id: int = -1,
        attribute_type_id: int = 0,
    ) -> list[int]:
        """Возвращает каталоги IMBASE, применимые для типа объекта и типа атрибута.

        Подбирает каталоги справочной системы, из которых допустимо выбирать значение
        для атрибута заданного типа у объекта заданного типа. В отличие от
        :meth:`imbase_catalogs` (все каталоги), этот метод фильтрует по применимости.

        Когда применять: при заполнении атрибута-ссылки на запись IMBASE — чтобы
        предложить пользователю только подходящие каталоги. Предусловий нет (чтение).

        Args:
            object_type_id: Идентификатор типа объекта (``objectTypeId``), для которого
                подбираются каталоги. По умолчанию ``-1`` (без ограничения по типу
                объекта — серверный дефолт).
            attribute_type_id: Идентификатор типа атрибута (``attributeTypeId``).
                По умолчанию ``0`` (серверный дефолт).

        Returns:
            Список идентификаторов применимых каталогов (``list[int]``). Пустой список
            означает, что подходящих каталогов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                catalogs = await ips.imbase_supported_catalogs(
                    object_type_id=1742, attribute_type_id=1029
                )
                print(catalogs)

        Notes:
            operationId ``ImBase_GetSupportedCatalogs``; путь
            ``GET /core/api/imbase/catalogs/supported`` с query-параметрами
            ``objectTypeId`` и ``attributeTypeId``. Ответ — прямой массив ``int64``
            (без result-обёртки). См. [[ips-object-model]].
        """
        params: dict[str, Any] = {
            "objectTypeId": object_type_id,
            "attributeTypeId": attribute_type_id,
        }
        data = await self._request("get", "/core/api/imbase/catalogs/supported", params=params)
        return [int(item) for item in data]
