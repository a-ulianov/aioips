"""Метод получения коллекции предметных областей форм."""

from ...core import APIManager
from ...schemas.forms import SubjectArea


class SubjectAreaFindCollectionMixin(APIManager):
    """Реализует ``GET /core/api/forms/subjectAreaFindCollection``.

    operationId ``Forms_SubjectAreaFindCollection``.
    """

    async def subject_area_find_collection(
        self: "SubjectAreaFindCollectionMixin",
    ) -> list[SubjectArea]:
        """Возвращает коллекцию предметных областей форм.

        Предметная область — именованная группировка форм/виджетов. Метод отдаёт полный
        перечень доступных предметных областей системы.

        Когда применять: чтобы предложить выбор предметной области (например, в
        редакторе форм) или сопоставить GUID области с её именем/символом. Параметры не
        требуются. Результат интерпретируется схемой :class:`SubjectArea`.

        Returns:
            Список предметных областей по схеме :class:`SubjectArea`. Пустой список
            означает отсутствие предметных областей.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                areas = await ips.subject_area_find_collection()
                for a in areas:
                    print(a.guid, a.name, a.symbol)

        Notes:
            operationId ``Forms_SubjectAreaFindCollection``; путь
            ``GET /core/api/forms/subjectAreaFindCollection``; ответ — массив
            ``SubjectAreaDto``.
        """
        data = await self._request("get", "/core/api/forms/subjectAreaFindCollection")
        return [SubjectArea.model_validate(item) for item in data]
