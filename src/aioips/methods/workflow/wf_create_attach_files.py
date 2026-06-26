"""Метод создания объекта-вложения типа «Файл во вложении» процесса."""

from typing import Any

from ...core import APIManager


class WFCreateAttachFilesMixin(APIManager):
    """Реализует ``POST /core/api/wfAttachments/createAttachFiles``.

    operationId ``WFAttachments_CreateAttachFile``.
    """

    async def wf_create_attach_files(
        self: "WFCreateAttachFilesMixin",
        file_data: bytes,
        file_name: str,
        *,
        confirm: bool = False,
    ) -> int:
        """Создаёт объект-вложение «Файл во вложении» из загружаемого файла (МУТИРУЮЩАЯ).

        Загружает содержимое файла (``multipart/form-data``, поле ``fileData``) и
        создаёт на сервере объект IPS типа «Файл во вложении», который затем можно
        прикрепить к активности процесса. Это создающая операция (новый объект на
        сервере), поэтому защищена ``confirm``: без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО запроса. Возвращает идентификатор созданного объекта;
        прикрепить его к задаче процесса можно методом :meth:`wf_add_attachments`
        (передав id в списке), а сам файл к активности — :meth:`wf_attach_files`.

        Args:
            file_data: Содержимое файла в виде байтов (``bytes``); отправляется как
                поле ``fileData`` формы.
            file_name: Имя файла; используется как имя части формы. Не передаётся
                отдельным полем (API принимает только ``fileData``), но задаёт
                ``filename`` в multipart.
            confirm: Подтверждение создания объекта. Без ``True`` метод не делает запрос
                и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            Идентификатор созданного объекта-вложения (``int``). ``0`` — если сервер
            не вернул значение.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                obj_id = await ips.wf_create_attach_files(
                    b"%PDF-1.4 ...", "act.pdf", confirm=True
                )
                await ips.wf_add_attachments(48210, [obj_id])  # 48210 = activityId

        Notes:
            operationId ``WFAttachments_CreateAttachFile``; путь
            ``POST /core/api/wfAttachments/createAttachFiles`` (тело
            ``multipart/form-data``: поле ``fileData``; ответ — ``int``). Связанные:
            :meth:`wf_attach_files`, :meth:`wf_add_attachments`. См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "Создание объекта-вложения изменяет данные на сервере: передайте confirm=True"
            )
        multipart: list[dict[str, Any]] = [
            {
                "name": "fileData",
                "value": file_data,
                "filename": file_name,
                "content_type": "application/octet-stream",
            }
        ]
        data = await self._request(
            "post",
            "/core/api/wfAttachments/createAttachFiles",
            multipart=multipart,
        )
        return int(data) if data is not None else 0
