"""Метод прикрепления загруженных временных файлов к атрибутам объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.files import AttachTempFile


class AttachTempFilesMixin(APIManager):
    """Реализует ``POST /core/api/files/objects/{objectId}/attachTempFiles``.

    operationId ``Files_AttachTempFilesToAttributes``.
    """

    async def attach_temp_files(
        self: "AttachTempFilesMixin",
        object_id: int,
        attachments: list[AttachTempFile],
    ) -> list[Any]:
        """Прикрепляет загруженные временные файлы к файловым атрибутам объекта (МУТИРУЮЩАЯ).

        Второй шаг типового сценария прикрепления файла: сначала содержимое
        загружается во временное хранилище через :meth:`upload_temp_file` (он
        возвращает временное имя), затем этот метод связывает временные файлы с
        файловыми атрибутами (``ftFile``) объекта. Каждый элемент ``attachments``
        указывает атрибут (``attribute_id``) и временный файл
        (``temp_file_name``), а также тип/дату/размер файла (см.
        :class:`AttachTempFile`).

        ПРЕДУСЛОВИЕ (жизненный цикл): прикрепление — операция записи, поэтому
        объект должен быть извлечён на редактирование (checkout). Метод НЕ делает
        checkout сам (``CheckOut`` → прикрепить → ``CheckIn``/``CancelChanges``).
        Имена в ``temp_file_name`` должны быть ранее получены из
        :meth:`upload_temp_file`.

        Предусловие по id-пространству: ``object_id`` — это ``ObjectID``
        (F_OBJECT_ID), общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``ObjectID`` / F_OBJECT_ID), к
                которому прикрепляются файлы (path ``objectId``).
            attachments: Список описаний временных файлов для прикрепления (см.
                :class:`AttachTempFile`). Сериализуется в тело-массив запроса
                (``model_dump(by_alias=True)``).

        Returns:
            Список элементов ответа сервера (в swagger — массив
            ``BlobFileAttributeInfoDto``, описывающих созданные записи файлов).
            Структура трактуется как непрозрачная: элементы возвращаются как есть.
            Пустой список — если сервер вернул не-список.

        Raises:
            IPSConflictError: Если объект не извлечён на редактирование (конфликт ЖЦ).
            IPSForbiddenError: При отсутствии прав на запись файловых атрибутов.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.files import AttachTempFile

            async with IPSClient(config=config) as ips:
                temp_name = await ips.upload_temp_file(b"PDF-bytes", "schema.pdf")
                # Объект 102550 предварительно извлечён на редактирование (checkout).
                result = await ips.attach_temp_files(
                    102550,
                    [
                        AttachTempFile(
                            attribute_id=12,
                            temp_file_name=temp_name,
                            file_type="ftNormal",
                            modify_date_time="2026-06-24T10:00:00",
                            real_file_size=1024,
                        )
                    ],
                )

        Notes:
            operationId ``Files_AttachTempFilesToAttributes``. Тело запроса —
            голый JSON-массив ``list[AttachTempFileToAttribute]``. Связанные
            методы: :meth:`upload_temp_file` (загрузка), :meth:`delete_temp_file`
            (очистка не прикреплённых временных файлов). См. [[ips-object-model]].
        """
        body = [a.model_dump(mode="json", by_alias=True, exclude_none=True) for a in attachments]
        data = await self._request(
            "post",
            f"/core/api/files/objects/{object_id}/attachTempFiles",
            json=body,
        )
        return data if isinstance(data, list) else []
