"""Метод подготовки файловых атрибутов при создании объекта по прототипу."""

from typing import Any

from ...core import APIManager
from ...schemas.files.object_with_file_attributes import ObjectWithFileAttributes
from ...schemas.files.prototype_info import PrototypeInfo


class HandleFileAttributesForObjectCreationMixin(APIManager):
    """Реализует ``POST /core/api/files/objectCreation/{objectId}`` (json).

    operationId ``Files_HandleFileAttributesForObjectCreation``.
    """

    async def handle_file_attributes_for_object_creation(
        self: "HandleFileAttributesForObjectCreationMixin",
        object_id: int,
        prototype: PrototypeInfo,
    ) -> ObjectWithFileAttributes:
        """Готовит файловые атрибуты создаваемого объекта по прототипу (подготовка).

        По описанию прототипа (:class:`PrototypeInfo`) формирует и возвращает
        набор файловых атрибутов (``ftFile``), которые должны быть у создаваемого
        объекта: сервер «разворачивает» болванки-прототипы в структуру файловых
        атрибутов и отдаёт её клиенту. Это ПОДГОТОВИТЕЛЬНЫЙ, НЕ разрушающий шаг
        сценария создания объекта по прототипу — он не удаляет данные и не меняет
        порядок файлов, поэтому ``confirm`` не требуется. Применяйте при создании
        объекта по прототипу, чтобы заранее узнать состав его файловых атрибутов;
        фактическое назначение прототипа уже существующему объекту —
        :meth:`set_prototype` / :meth:`set_file_attr_prototype`.

        Args:
            object_id: Идентификатор создаваемого объекта (его версии/рабочей
                копии в процессе создания); уходит в путь ``{objectId}``.
            prototype: :class:`PrototypeInfo` — описание прототипа, по которому
                готовятся файловые атрибуты: ``prototype_id`` и ``name``
                (обязательны), ``attribute_id`` (опционально). Сериализуется
                JSON-телом
                (``model_dump(mode="json", by_alias=True, exclude_none=True)``).

        Returns:
            :class:`ObjectWithFileAttributes` — объект (его версия) вместе с
            подготовленными файловыми атрибутами: ``object_version_id``,
            ``object_type``, ``read_only`` и список ``attributes``
            (:class:`FileAttribute`) с вложенными файлами. Пустой список
            ``attributes`` означает, что прототип не добавляет файловых атрибутов.

        Raises:
            IPSError: При ошибке сервера (прототип не найден, объект недоступен
                для подготовки).

        Example:
            from aioips.schemas.files.prototype_info import PrototypeInfo

            async with IPSClient(config=config) as ips:
                result = await ips.handle_file_attributes_for_object_creation(
                    102550,
                    PrototypeInfo(prototype_id=42, name="Чертёж PDF", attribute_id=1031),
                )
                for attr in result.attributes:
                    print(attr.attribute_id, attr.is_multiple)

        Notes:
            operationId ``Files_HandleFileAttributesForObjectCreation``; путь
            ``POST /core/api/files/objectCreation/{objectId}`` (тело
            ``PrototypeInfo``). Связанные: :meth:`set_prototype`,
            :meth:`set_file_attr_prototype`, :meth:`file_prototypes`,
            :meth:`file_attributes`. См. объектной модели IPS.
        """
        payload: dict[str, Any] = prototype.model_dump(
            mode="json", by_alias=True, exclude_none=True
        )
        path = f"/core/api/files/objectCreation/{object_id}"
        data = await self._request("post", path, json=payload)
        return ObjectWithFileAttributes.model_validate(data)
