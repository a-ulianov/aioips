"""Метод прикрепления файла к активности процесса."""

from typing import Any

from ...core import APIManager


class WFAttachFilesMixin(APIManager):
    """Реализует ``POST /core/api/wfAttachments/{activityId}/attachFiles``.

    operationId ``WFAttachments_AttachFile``.
    """

    async def wf_attach_files(
        self: "WFAttachFilesMixin",
        activity_id: int,
        file_data: bytes,
        file_name: str,
        *,
        confirm: bool = False,
    ) -> dict[str, Any] | None:
        """Прикрепляет файл к активности (задаче) процесса как вложение (МУТИРУЮЩАЯ).

        Загружает содержимое файла (``multipart/form-data``, поле ``fileData``) и
        прикрепляет его как вложение к указанной активности процесса workflow за один
        вызов. Это мутирующая операция (новое вложение у задачи), поэтому защищена
        ``confirm``: без ``confirm=True`` поднимается :class:`ValueError` ещё ДО запроса.
        Текущий состав вложений активности читает :meth:`wf_attachments`, удаляет —
        :meth:`wf_remove_attachments`; альтернатива в два шага — создать объект через
        :meth:`wf_create_attach_files` и прикрепить :meth:`wf_add_attachments`.

        Предусловие по id-пространству: ``activity_id`` — идентификатор АКТИВНОСТИ
        (задачи) экземпляра процесса, а не объекта/версии.

        Args:
            activity_id: Идентификатор активности (задачи) экземпляра процесса
                (path-параметр ``activityId``, ``int64``).
            file_data: Содержимое файла в виде байтов (``bytes``); отправляется как
                поле ``fileData`` формы.
            file_name: Имя файла; задаёт ``filename`` части multipart.
            confirm: Подтверждение прикрепления. Без ``True`` метод не делает запрос и
                поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``dict[str, Any]`` с данными созданного вложения (``AttachmentDTO``:
            ``objectId``, ``caption``, ``objectType`` и др.), если сервер вернул сущность
            (``isEntityPresent=true``); иначе ``None`` (вложение не возвращено).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                att = await ips.wf_attach_files(
                    48210, b"%PDF-1.4 ...", "act.pdf", confirm=True
                )  # 48210 = activityId
                if att is not None:
                    print(att["objectId"], att.get("caption"))

        Notes:
            operationId ``WFAttachments_AttachFile``; путь
            ``POST /core/api/wfAttachments/{activityId}/attachFiles`` (тело
            ``multipart/form-data``: поле ``fileData``; ответ
            ``AttachmentDTONullableResultDto`` — разворачивается в ``entity`` или
            ``None``). Связанные: :meth:`wf_attachments`, :meth:`wf_add_attachments`,
            :meth:`wf_create_attach_files`. См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "Прикрепление файла к активности изменяет данные на сервере: передайте confirm=True"
            )
        multipart: list[dict[str, Any]] = [
            {
                "name": "fileData",
                "value": file_data,
                "filename": file_name,
                "content_type": "application/octet-stream",
            }
        ]
        path = f"/core/api/wfAttachments/{activity_id}/attachFiles"
        data = await self._request("post", path, multipart=multipart)
        if not isinstance(data, dict) or not data.get("isEntityPresent"):
            return None
        entity = data.get("entity")
        return entity if isinstance(entity, dict) else None
