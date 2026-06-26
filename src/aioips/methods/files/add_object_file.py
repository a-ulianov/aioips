"""Метод прямого прикрепления файла к файловому атрибуту объекта."""

from datetime import datetime
from typing import Any

from ...common.enumerations import FileTypes
from ...core import APIManager
from ...schemas.files.object_with_file_attributes import BlobFileAttributeInfo


class AddObjectFileMixin(APIManager):
    """Реализует ``POST /core/api/files/objects/{objectId}/files`` (multipart).

    operationId ``Files_AddObjectFile``.
    """

    async def add_object_file(
        self: "AddObjectFileMixin",
        object_id: int,
        attribute_id: int,
        file_data: bytes,
        file_name: str,
        file_type: FileTypes | str,
        modify_date_time: datetime,
        *,
        real_file_size: int | None = None,
    ) -> BlobFileAttributeInfo:
        """Прикрепляет НОВЫЙ файл прямо к файловому атрибуту объекта (МУТИРУЮЩАЯ).

        Прямой однопроходный способ добавить файл в атрибут типа ``ftFile``:
        содержимое отправляется как ``multipart/form-data`` сразу к объекту, без
        промежуточного временного хранилища. Это альтернатива двухшаговому
        сценарию :meth:`upload_temp_file` + :meth:`attach_temp_files`; применяйте
        прямой способ, когда байты файла уже есть в памяти и не нужна отдельная
        стадия временного хранилища. Парный обратный метод —
        :meth:`delete_object_file`: цикл add → delete ОБРАТИМ (добавленный файл
        удаляется тем же ``attribute_id`` и ``blob_id`` из ответа). Заменить
        содержимое уже прикреплённого файла — :meth:`update_object_file`; править
        только имя/комментарий — :meth:`update_object_file_info`.

        Предусловия (ОБЯЗАТЕЛЬНО, проверено на проде): объект должен быть взят на
        изменение (``object_check_out``), а в ``object_id`` нужно передавать
        идентификатор РАБОЧЕЙ КОПИИ — то, что вернул :meth:`object_check_out`
        (это id версии-черновика, на проде он ОТРИЦАТЕЛЬНЫЙ), НЕ базовый
        ``ObjectID``. При передаче базового id объекта сервер отвечает 400
        «выполните команду checkOut». После правки — ``object_check_in`` либо
        ``object_cancel_changes`` (см. ``ObjectModifyModes`` в [[ips-object-model]]).

        ``attribute_id`` — идентификатор ТИПА файлового атрибута (``ftFile``), куда
        кладётся файл.

        Args:
            object_id: Идентификатор РАБОЧЕЙ КОПИИ объекта (результат
                :meth:`object_check_out`; на проде отрицательный), НЕ базовый
                ``ObjectID``. Уходит в путь ``{objectId}``.
            attribute_id: Идентификатор файлового атрибута (``ftFile``);
                отправляется строкой в поле формы ``attributeId``.
            file_data: Содержимое файла (``bytes``); поле ``fileData`` формы с
                ``filename=file_name`` и ``content_type=application/octet-stream``.
            file_name: Имя файла; поле формы ``fileName``.
            file_type: Тип файла — строковое значение перечисления ``FileTypes``:
                ``ftNormal`` (файл объекта), ``ftNotContent`` (не относится к
                контенту), ``ftOTD`` (файл ОТД), ``ftRedlining`` (файл редактуры),
                ``ftAuthentical`` (аутентичный файл), ``ftUnknown`` (неизвестный
                тип); поле формы ``fileType``.
            modify_date_time: Дата модификации файла (``datetime``); отправляется
                ISO-строкой (``.isoformat()``) в поле формы ``modifyDateTime``.
            real_file_size: Реальный (распакованный) размер файла в байтах;
                необязательный query-параметр ``realFileSize``. ``None`` — не
                передаётся (сервер вычислит сам).

        Returns:
            :class:`BlobFileAttributeInfo` — метаданные созданной BLOB-записи;
            поле ``blob_id`` идентифицирует добавленный файл и используется в
            :meth:`update_object_file`, :meth:`update_object_file_info` и
            :meth:`delete_object_file`.

        Raises:
            IPSError: При ошибочном ответе сервера (например, объект не взят на
                изменение, атрибут только для чтения, неверный ``file_type``).

        Example:
            from datetime import datetime, timezone

            async with IPSClient(config=config) as ips:
                wc = await ips.object_check_out(102550)  # id рабочей копии (отриц.)
                try:
                    info = await ips.add_object_file(
                        object_id=wc,  # РАБОЧАЯ КОПИЯ, не базовый ObjectID
                        attribute_id=1031,
                        file_data=b"%PDF-1.4 ...",
                        file_name="schema.pdf",
                        file_type="ftNormal",
                        modify_date_time=datetime.now(timezone.utc),
                    )
                    await ips.delete_object_file(
                        wc, attribute_id=1031, blob_id=info.blob_id, confirm=True
                    )
                finally:
                    await ips.object_check_in(102550)

        Notes:
            operationId ``Files_AddObjectFile``; путь ``POST
            /core/api/files/objects/{objectId}/files`` (тело
            ``multipart/form-data``). Файлы хранятся во внешнем файловом
            хранилище (vault, диск X:). Связанные: :meth:`update_object_file`,
            :meth:`update_object_file_info`, :meth:`delete_object_file`,
            :meth:`attach_temp_files`. См. [[ips-object-model]].
        """
        multipart: list[dict[str, Any]] = [
            {"name": "attributeId", "value": str(attribute_id)},
            {"name": "fileName", "value": file_name},
            {"name": "fileType", "value": file_type},
            {"name": "modifyDateTime", "value": modify_date_time.isoformat()},
            {
                "name": "fileData",
                "value": file_data,
                "filename": file_name,
                "content_type": "application/octet-stream",
            },
        ]
        params: dict[str, Any] | None = None
        if real_file_size is not None:
            params = {"realFileSize": int(real_file_size)}
        path = f"/core/api/files/objects/{object_id}/files"
        data = await self._request("post", path, params=params, multipart=multipart)
        return BlobFileAttributeInfo.model_validate(data)
