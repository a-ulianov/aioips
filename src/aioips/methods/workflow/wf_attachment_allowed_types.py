"""Метод получения допустимых типов вложений активности процесса."""

from ...core import APIManager


class WFAttachmentAllowedTypesMixin(APIManager):
    """Реализует ``GET /core/api/wfAttachments/{activityId}/allowedtypes``.

    operationId ``WFAttachments_Allowedtypes``.
    """

    async def wf_attachment_allowed_types(
        self: "WFAttachmentAllowedTypesMixin",
        activity_id: int,
    ) -> list[int]:
        """Возвращает идентификаторы типов объектов, допустимых как вложения активности.

        Определяет, объекты каких типов разрешено прикреплять к данной активности
        (задаче) процесса. Применяйте перед добавлением вложения, чтобы предложить или
        провалидировать выбор типа; текущие вложения активности даёт
        :meth:`wf_attachments`.

        Предусловие по id-пространству: ``activity_id`` — идентификатор АКТИВНОСТИ
        (задачи) экземпляра процесса, а не объекта или версии. Возвращаемые значения —
        идентификаторы ТИПОВ объектов (а не идентификаторы объектов).

        Args:
            activity_id: Идентификатор активности (задачи) экземпляра процесса workflow.

        Returns:
            Список числовых идентификаторов типов объектов, допустимых как вложения.
            Пустой список означает, что прикреплять вложения к активности нельзя
            (нет разрешённых типов).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                allowed = await ips.wf_attachment_allowed_types(48210)
                if 1037 in allowed:
                    print("тип 1037 можно прикреплять")

        Notes:
            operationId ``WFAttachments_Allowedtypes``; путь
            ``GET /core/api/wfAttachments/{activityId}/allowedtypes`` (голый массив int).
        """
        path = f"/core/api/wfAttachments/{activity_id}/allowedtypes"
        data = await self._request("get", path)
        return [int(item) for item in data]
