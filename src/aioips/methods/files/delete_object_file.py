"""Метод удаления файла из файлового атрибута объекта."""

from typing import Any

from ...core import APIManager


class DeleteObjectFileMixin(APIManager):
    """Реализует ``DELETE /core/api/files/objects/{objectId}/files``.

    operationId ``Files_DeleteObjectFile``.
    """

    async def delete_object_file(
        self: "DeleteObjectFileMixin",
        object_id: int,
        *,
        attribute_id: int,
        blob_id: int,
        confirm: bool = False,
    ) -> None:
        """Удаляет файл из файлового атрибута объекта (РАЗРУШАЮЩАЯ, ``confirm``).

        Открепляет и удаляет конкретный файл (адресуемый ``blob_id``) из
        файлового атрибута объекта. Это обратная операция к
        :meth:`add_object_file`: цикл add → delete ОБРАТИМ — добавленный методом
        :meth:`add_object_file` файл удаляется тем же ``attribute_id`` и
        ``blob_id`` из его ответа. Операция необратима для самого файла, поэтому
        по умолчанию метод НЕ выполняется: требуется явный ``confirm=True``,
        иначе поднимается :class:`ValueError` ещё ДО обращения к серверу
        (защитный гейт §7).

        Предусловия: удаление файла из атрибута обычно требует, чтобы объект был
        в режиме изменения (``checkOut`` → правка → ``checkIn``; см.
        ``ObjectModifyModes`` в объектной модели IPS). Файл с указанным
        ``blob_id`` должен существовать у объекта в этом атрибуте.

        Предусловие по id-пространству: ``object_id`` — идентификатор ОБЪЕКТА
        (``ObjectID`` / F_OBJECT_ID); ``attribute_id`` — идентификатор файлового
        атрибута (``ftFile``); ``blob_id`` — идентификатор удаляемой BLOB-записи.
        Параметры ``attribute_id`` и ``blob_id`` передаются в строке запроса
        (query), тело запроса отсутствует.

        Args:
            object_id: Идентификатор РАБОЧЕЙ КОПИИ объекта (результат
                :meth:`object_check_out`; на проде отрицательный), НЕ базовый
                ``ObjectID`` — объект должен быть взят на изменение, иначе сервер
                вернёт 400 «выполните checkOut».
            attribute_id: Идентификатор файлового атрибута (``ftFile``);
                query-параметр ``attributeId``.
            blob_id: Идентификатор удаляемой BLOB-записи; query-параметр
                ``blobId``.
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не
                делает запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void); успехом считается
            ответ без ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSNotFoundError: Если файл с таким ``blob_id`` у объекта не найден.
            IPSError: При иной ошибке сервера.

        Example:
            from datetime import datetime

            async with IPSClient(config=config) as ips:
                info = await ips.add_object_file(
                    object_id=102550,
                    attribute_id=1031,
                    file_data=b"%PDF-1.4 ...",
                    file_name="schema.pdf",
                    file_type="ftNormal",
                    modify_date_time=datetime.utcnow(),
                )
                # обратимый цикл: удалить только что добавленный файл
                await ips.delete_object_file(
                    102550, attribute_id=1031, blob_id=info.blob_id, confirm=True
                )

        Notes:
            operationId ``Files_DeleteObjectFile``; путь ``DELETE
            /core/api/files/objects/{objectId}/files`` (query ``attributeId``,
            ``blobId``; без тела). Связанные: :meth:`add_object_file`,
            :meth:`update_object_file`. См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "delete_object_file требует confirm=True: удаление файла объекта необратимо"
            )
        params: dict[str, Any] = {
            "attributeId": int(attribute_id),
            "blobId": int(blob_id),
        }
        path = f"/core/api/files/objects/{object_id}/files"
        await self._request("delete", path, params=params)
        return None
