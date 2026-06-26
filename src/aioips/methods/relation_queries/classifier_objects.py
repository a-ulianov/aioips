"""Метод получения объектов-потомков узла классификатора."""

from typing import Any

from ...core import APIManager


class ClassifierObjectsMixin(APIManager):
    """Реализует ``GET /core/api/Relations/GetClassifierObjects``.

    operationId ``Relations_GetClassifierObjects``.
    """

    async def classifier_objects(
        self: "ClassifierObjectsMixin",
        *,
        classifier_object_id: int | None = None,
    ) -> list[int]:
        """Возвращает идентификаторы объектов, отнесённых к узлу классификатора.

        Классификатор в IPS — это дерево узлов-объектов, к которым привязаны
        прикладные объекты. Метод отдаёт идентификаторы ОБЪЕКТОВ (``objectID``),
        связанных с указанным узлом классификатора; если узел не задан, поведение
        определяется сервером (как правило — корневой/общий набор). Метод
        относится к разделу запросов состава (контроллер ``/core/api/Relations/...``
        с ЗАГЛАВНОЙ ``R``) и не совпадает с разделом ``relations`` (строчная ``r``).

        Args:
            classifier_object_id: Идентификатор ОБЪЕКТА-узла классификатора
                (``objectID``), чьи объекты запрашиваются. Передаётся в запрос
                только когда задан явно.

        Returns:
            Список идентификаторов объектов (``objectID``). Пустой список означает,
            что к узлу не отнесён ни один объект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                object_ids = await ips.classifier_objects(classifier_object_id=4200)
                for oid in object_ids:
                    print(oid)

        Notes:
            operationId ``Relations_GetClassifierObjects``; путь
            ``GET /core/api/Relations/GetClassifierObjects`` (массив ``int64``).
        """
        params: dict[str, Any] = {}
        if classifier_object_id is not None:
            params["classifierObjectId"] = classifier_object_id
        data = await self._request(
            "get", "/core/api/Relations/GetClassifierObjects", params=params or None
        )
        return [int(item) for item in data]
