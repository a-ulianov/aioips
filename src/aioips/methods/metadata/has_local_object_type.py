"""Метод проверки наличия локального типа среди набора типов."""

from ...core import APIManager


class HasLocalObjectTypeMixin(APIManager):
    """Реализует ``POST /core/api/metadata/objectTypes/hasLocal``."""

    async def has_local_object_type(
        self: "HasLocalObjectTypeMixin",
        object_type_ids: list[int],
    ) -> bool:
        """Проверяет, есть ли среди переданных типов хотя бы один ЛОКАЛЬНЫЙ.

        Возвращает признак того, что в наборе типов присутствует хотя бы один тип,
        определённый ЛОКАЛЬНО в текущей базе (а не унаследованный из родительской/общей
        метамодели). Операция ЧТЕНИЯ метамодели: ничего не изменяет, POST используется лишь
        для передачи списка id телом.

        Когда применять: при ветвлении логики, зависящей от наличия локальных расширений
        метамодели в выбранном наборе типов (например, перед операциями, доступными только
        для локальных типов). Проверка локальности одного типа — :meth:`object_type_is_local`.

        Args:
            object_type_ids: Список id ТИПОВ объектов (``ObjectTypeID``; локальные).
                Передаётся телом запроса (JSON-массив).

        Returns:
            ``True``, если среди переданных типов есть хотя бы один локальный, иначе
            ``False`` (в т.ч. при пустом входном списке или ``null`` от сервера).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.has_local_object_type([1742, 1801]):
                    print("в наборе есть локальный тип")

        Notes:
            operationId ``Metadata_HasLocalObjectType``; путь
            ``POST /core/api/metadata/objectTypes/hasLocal`` (тело — ``list[int]``; ответ —
            ``boolean``). См. [[ips-object-model]]. Связанные методы:
            :meth:`object_type_is_local`.
        """
        data = await self._request(
            "post", "/core/api/metadata/objectTypes/hasLocal", json=object_type_ids
        )
        return bool(data)
