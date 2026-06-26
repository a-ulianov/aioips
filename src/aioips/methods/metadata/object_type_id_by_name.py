"""Метод получения идентификатора типа объекта по его имени."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeIdByNameMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/byName/{objectTypeName}/id``."""

    async def object_type_id_by_name(
        self: "ObjectTypeIdByNameMixin",
        object_type_name: str,
    ) -> int:
        """Возвращает идентификатор типа объекта по его имени.

        Удобно, когда известно человекочитаемое имя типа объекта, но нужен числовой
        идентификатор (``ObjectTypeID``) для последующих запросов (например, для
        :meth:`objects_by_object_type`, :meth:`object_type_life_cycle_steps` или
        условий поиска). Имя кодируется в URL, поэтому допускаются пробелы и кириллица.
        Ответ сервера — целое число (идентификатор), а не объект-обёртка.

        Когда применять: как мост «имя → id» перед вызовами, требующими
        ``objectTypeId``. Полное метаописание по полученному id — :meth:`object_type`.

        Args:
            object_type_name: Имя типа объекта точно как в метаданных IPS (регистр и
                пробелы значимы); кодируется в URL, кириллица допускается.

        Returns:
            Числовой идентификатор типа объекта (``ObjectTypeID`` — id-пространство
            ТИПОВ объектов). Сервер не возвращает ``None``: при отсутствии имени —
            ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если тип с таким
                именем не найден).

        Example:
            async with IPSClient(config=config) as ips:
                type_id = await ips.object_type_id_by_name("Документ")
                print(type_id)

        Notes:
            operationId ``Metadata_GetObjectTypeIdByName``; путь
            ``GET /core/api/metadata/objectTypes/byName/{objectTypeName}/id``.
            Связанный метод (полное описание по id) — :meth:`object_type`.
        """
        encoded_name = quote(object_type_name, safe="")
        path = f"/core/api/metadata/objectTypes/byName/{encoded_name}/id"
        data = await self._request("get", path)
        return int(data)
