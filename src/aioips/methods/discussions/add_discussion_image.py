"""Метод добавления изображения в обсуждение."""

from typing import Any

from ...core import APIManager


class AddDiscussionImageMixin(APIManager):
    """Реализует ``POST /core/api/discussions/addImage`` (``Discussions_AddImage``)."""

    async def add_discussion_image(
        self: "AddDiscussionImageMixin",
        file_data: bytes,
        file_name: str,
        *,
        discussion_version_id: int | None = None,
        object_version_id: int | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Загружает изображение в обсуждение и возвращает ссылку на него (МУТИРУЮЩАЯ).

        Загружает картинку (``multipart/form-data``, поле ``fileData``) в обсуждение
        версии объекта и создаёт на сервере объект-изображение, который затем
        встраивается в текст сообщения. Это создающая операция (новый артефакт на
        сервере), поэтому защищена ``confirm``: без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО запроса. Применяйте вместе с :meth:`add_message`
        (или :meth:`edit_message`), чтобы приложить иллюстрацию к замечанию; возможность
        обсуждения проверяет :meth:`can_discuss`.

        Предусловие по id-пространству (критично): и ``discussion_version_id``, и
        ``object_version_id`` — это идентификаторы ВЕРСИЙ (F_ID), а не объектов; они
        передаются строкой запроса. Тело — только бинарное поле ``fileData``.

        Args:
            file_data: Содержимое изображения в виде байтов (``bytes``); отправляется
                как поле ``fileData`` формы.
            file_name: Имя файла изображения; задаёт ``filename`` части multipart.
            discussion_version_id: Идентификатор ВЕРСИИ обсуждения (query
                ``discussionVersionId``, ``int64``). ``None`` — не передаётся.
            object_version_id: Идентификатор ВЕРСИИ объекта (query ``objectVersionId``,
                ``int64``). ``None`` — не передаётся.
            confirm: Подтверждение создания артефакта. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``dict[str, Any]`` по схеме ``AddImageResultDto``: ``objectVersionGuid``
            (GUID версии созданного изображения) и ``fileName`` (имя файла), по которым
            картинка вставляется в сообщение.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                png_bytes = open("shot.png", "rb").read()
                result = await ips.add_discussion_image(
                    png_bytes, "shot.png", object_version_id=102550, confirm=True
                )
                print(result["objectVersionGuid"], result["fileName"])

        Notes:
            operationId ``Discussions_AddImage``; путь
            ``POST /core/api/discussions/addImage`` (query ``discussionVersionId``,
            ``objectVersionId``; тело ``multipart/form-data``: поле ``fileData``; ответ
            ``AddImageResultDto``). Связанные: :meth:`add_message`,
            :meth:`edit_message`, :meth:`can_discuss`. См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "Загрузка изображения в обсуждение изменяет данные на сервере: "
                "передайте confirm=True"
            )
        params: dict[str, Any] = {}
        if discussion_version_id is not None:
            params["discussionVersionId"] = str(discussion_version_id)
        if object_version_id is not None:
            params["objectVersionId"] = str(object_version_id)
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
            "/core/api/discussions/addImage",
            params=params,
            multipart=multipart,
        )
        return data if isinstance(data, dict) else {}
