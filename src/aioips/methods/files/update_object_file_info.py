"""Метод правки метаинформации файла объекта (имя/комментарий)."""

from typing import Any

from ...core import APIManager
from ...schemas.files.update_object_file_info import UpdateObjectFileInfo


class UpdateObjectFileInfoMixin(APIManager):
    """Реализует ``PUT /core/api/files/objects/{objectId}/files/info`` (json).

    operationId ``Files_UpdateObjectFileInfo``.
    """

    async def update_object_file_info(
        self: "UpdateObjectFileInfoMixin",
        object_id: int,
        body: UpdateObjectFileInfo,
    ) -> None:
        """Правит ИМЯ и/или КОММЕНТАРИЙ файла объекта без замены байтов (МУТИРУЮЩАЯ).

        Обновляет только метаданные конкретной BLOB-записи (имя файла и/или
        комментарий), не трогая её содержимое. В отличие от
        :meth:`update_object_file` (заменяет байты файла) здесь меняются лишь
        атрибуты записи. Файл адресуется парой ``attribute_id`` + ``blob_id``,
        задаваемой в ``body`` (см. :class:`UpdateObjectFileInfo`). Поля
        ``file_name``/``note`` со значением ``None`` не отправляются — текущее
        значение на сервере сохраняется.

        Предусловия: правка обычно требует, чтобы объект был в режиме изменения
        (``checkOut`` → правка → ``checkIn``; см. ``ObjectModifyModes`` в
        [[ips-object-model]]). Адресуемый файл должен существовать у объекта.

        Предусловие по id-пространству: ``object_id`` — идентификатор ОБЪЕКТА
        (``ObjectID`` / F_OBJECT_ID); ``body.attribute_id`` — идентификатор
        файлового атрибута (``ftFile``); ``body.blob_id`` — идентификатор
        BLOB-записи (из ответа :meth:`add_object_file` или метаданных
        :meth:`file_attributes`).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``ObjectID`` / F_OBJECT_ID); путь.
            body: :class:`UpdateObjectFileInfo` — что менять: ``blob_id`` и
                ``attribute_id`` (обязательны), ``file_name`` и/или ``note``
                (опционально; ``None`` оставляет значение без изменений).
                Сериализуется JSON-телом
                (``model_dump(mode="json", by_alias=True, exclude_none=True)``).

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void); успехом считается
            ответ без ошибки.

        Raises:
            IPSNotFoundError: Если файл (``blob_id``) у объекта не найден.
            IPSError: При иной ошибке сервера (объект не взят на изменение).

        Example:
            from aioips.schemas.files.update_object_file_info import (
                UpdateObjectFileInfo,
            )

            async with IPSClient(config=config) as ips:
                await ips.update_object_file_info(
                    102550,
                    UpdateObjectFileInfo(
                        attribute_id=1031,
                        blob_id=778899,
                        file_name="schema-rev2.pdf",
                        note="Ревизия 2",
                    ),
                )

        Notes:
            operationId ``Files_UpdateObjectFileInfo``; путь ``PUT
            /core/api/files/objects/{objectId}/files/info`` (тело
            ``UpdateObjectFileInfoDto``). Связанные: :meth:`add_object_file`,
            :meth:`update_object_file`, :meth:`delete_object_file`.
            См. [[ips-object-model]].
        """
        payload: dict[str, Any] = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        path = f"/core/api/files/objects/{object_id}/files/info"
        await self._request("put", path, json=payload)
        return None
