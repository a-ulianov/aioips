"""Метод получения настройки множественного выбора классификаторов."""

from ...core import APIManager


class IsMultiSelectClassifierMixin(APIManager):
    """Реализует ``GET /core/api/selectionClassificators/isMultiSelectClassifier``.

    operationId ``SelectionClassificators_GetMultiSelectClassifierSetting``.
    """

    async def is_multi_select_classifier(self: "IsMultiSelectClassifierMixin") -> bool:
        """Возвращает глобальную настройку: допускают ли классификаторы множественный выбор.

        Системная настройка IPS, определяющая, можно ли при работе с классификаторами выбора
        выбирать несколько значений одновременно (``True``) или допускается только одно
        значение (``False``). Настройка глобальная и не зависит от конкретного классификатора
        или объекта.

        Когда применять: чтобы корректно построить UI/логику выбора значения из классификатора
        (один или несколько вариантов) перед использованием :meth:`classificator_attributes`.
        Предусловий и параметров нет.

        Returns:
            ``True`` — классификаторы допускают множественный выбор значений; ``False`` —
            только одиночный выбор. Отсутствующий/``null`` ответ трактуется как ``False``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                multi = await ips.is_multi_select_classifier()
                print("множественный выбор" if multi else "одиночный выбор")

        Notes:
            operationId ``SelectionClassificators_GetMultiSelectClassifierSetting``; путь
            ``GET /core/api/selectionClassificators/isMultiSelectClassifier``. Ответ — голое
            булево значение без result-обёртки.
        """
        data = await self._request(
            "get",
            "/core/api/selectionClassificators/isMultiSelectClassifier",
        )
        return bool(data) if data is not None else False
