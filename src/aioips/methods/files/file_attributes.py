"""Метод получения файловых атрибутов объекта."""

from ...core import APIManager
from ...schemas.files import ObjectWithFileAttributes


class FileAttributesMixin(APIManager):
    """Реализует ``GET /core/api/files/objects/{objectId}``.

    operationId ``Files_GetFileAttributes``.
    """

    async def file_attributes(
        self: "FileAttributesMixin",
        object_id: int,
    ) -> ObjectWithFileAttributes:
        """Возвращает объект вместе со всеми его файловыми атрибутами и файлами.

        Основной способ узнать, какие файлы прикреплены к объекту: метод отдаёт
        список файловых атрибутов (``ftFile``), а для каждого — метаданные
        хранящихся в нём файлов (имя, размеры, ``blob_id``, тип, автор, шкаф).
        Сам контент файла здесь не передаётся — его загружают отдельно по
        ``blob_id`` (:meth:`object_file_by_blob_id`) или по имени
        (:meth:`object_file_by_name`). Доступные шаблоны-прототипы — у
        :meth:`file_prototypes`.

        Предусловие по id-пространству: ``object_id`` — это идентификатор ОБЪЕКТА
        (``ObjectID`` / F_OBJECT_ID), общий для всех версий, а не идентификатор
        версии. В ответе ``object_version_id`` — это уже id ВЕРСИИ (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``ObjectID`` / F_OBJECT_ID), чьи
                файловые атрибуты нужно получить. Не идентификатор версии.

        Returns:
            Объект по схеме :class:`ObjectWithFileAttributes`. Поле
            ``attributes`` — список файловых атрибутов
            (:class:`~aioips.schemas.files.FileAttribute`); у каждого
            ``file_info_collection`` — метаданные файлов
            (:class:`~aioips.schemas.files.BlobFileAttributeInfo`). Пустой
            ``attributes`` означает, что у объекта нет файловых атрибутов.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                obj = await ips.file_attributes(102550)  # 102550 = ObjectID
                for attr in obj.attributes:
                    for info in attr.file_info_collection:
                        print(attr.attribute_id, info.file_name, info.blob_id)

        Notes:
            operationId ``Files_GetFileAttributes``; ответ —
            ``ObjectWithFileAttributesDto``. Файлы — атрибуты ``ftFile`` во
            внешнем хранилище (vault, диск X:). См. [[ips-object-model]].
        """
        data = await self._request("get", f"/core/api/files/objects/{object_id}")
        return ObjectWithFileAttributes.model_validate(data)
