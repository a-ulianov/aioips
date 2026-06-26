"""Метод получения допустимых типов вложений задач проектов (Improject)."""

from ...core import APIManager


class TaskAttachmentsAllowedTypesMixin(APIManager):
    """Реализует ``GET /core/api/improjects/tasks/attachments/allowed-types``.

    ``operationId`` ``ImProject_GetTaskAttachmentsAllowedType``.
    """

    async def task_attachments_allowed_types(
        self: "TaskAttachmentsAllowedTypesMixin",
    ) -> list[int]:
        """Возвращает id типов объектов, допустимых как вложения задач проектов Improject.

        Назначение: определить, объекты каких типов разрешено прикреплять к
        задачам проекта управления проектами. Применяйте перед добавлением
        вложения, чтобы предложить или провалидировать выбор типа; текущие
        вложения конкретной задачи даёт :meth:`task_attachments`. Метод общий и
        не требует идентификатора задачи.

        Предусловие: модуль Improject (управление проектами) должен быть
        лицензирован. Возвращаемые значения — идентификаторы ТИПОВ объектов
        (не идентификаторы объектов и не id версий).

        Returns:
            Список числовых идентификаторов типов объектов, допустимых как
            вложения задач. Пустой список означает, что прикреплять вложения
            нельзя (нет разрешённых типов).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                allowed = await ips.task_attachments_allowed_types()
                if 1037 in allowed:
                    print("тип 1037 можно прикреплять к задаче")

        Notes:
            ``operationId``: ``ImProject_GetTaskAttachmentsAllowedType``; путь
            ``GET /core/api/improjects/tasks/attachments/allowed-types``
            (голый массив int). Связанные методы: :meth:`task_attachments`.
        """
        path = "/core/api/improjects/tasks/attachments/allowed-types"
        data = await self._request("get", path)
        return [int(item) for item in data]
