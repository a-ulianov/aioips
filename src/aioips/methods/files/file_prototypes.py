"""Метод получения файлов-прототипов для объекта."""

from ...core import APIManager
from ...schemas.files import PrototypeInfo


class FilePrototypesMixin(APIManager):
    """Реализует ``GET /core/api/files/getFilesProptotypes/{objectId}``.

    operationId ``Files_GetFilesPrototypes``.
    """

    async def file_prototypes(
        self: "FilePrototypesMixin",
        object_id: int,
    ) -> list[PrototypeInfo]:
        """Возвращает список файлов-прототипов (шаблонов), доступных для объекта.

        Прототип — это «болванка» файла, которую можно подставить в файловый
        атрибут (``ftFile``) объекта. Метод применяют перед заполнением файлового
        атрибута, чтобы узнать, какие шаблоны доступны и к какому атрибуту они
        привязаны. Для получения уже хранящихся в объекте файловых атрибутов и
        их файлов используйте :meth:`file_attributes`.

        Предусловие по id-пространству: ``object_id`` — это идентификатор ОБЪЕКТА
        (``ObjectID`` / F_OBJECT_ID), общий для всех версий, а не идентификатор
        версии (``id`` / F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``ObjectID`` / F_OBJECT_ID), для
                которого запрашиваются прототипы. Не идентификатор версии.

        Returns:
            Список прототипов по схеме :class:`PrototypeInfo`. Пустой список
            означает, что для объекта не определено ни одного файла-прототипа.
            Значимые поля: ``prototype_id`` — id прототипа, ``name`` — имя,
            ``attribute_id`` — id файлового атрибута (или ``None``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                prototypes = await ips.file_prototypes(102550)  # 102550 = ObjectID
                for proto in prototypes:
                    print(proto.prototype_id, proto.name, proto.attribute_id)

        Notes:
            operationId ``Files_GetFilesPrototypes``; путь содержит написание
            ``getFilesProptotypes`` как в IPS Web API. Ответ — массив
            ``PrototypeInfoDto``. См. объектной модели IPS (раздел про файлы).
        """
        data = await self._request("get", f"/core/api/files/getFilesProptotypes/{object_id}")
        return [PrototypeInfo.model_validate(item) for item in data]
