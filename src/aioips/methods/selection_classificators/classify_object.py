"""Метод классификации объекта по классификаторам выбора."""

from ...core import APIManager


class ClassifyObjectMixin(APIManager):
    """Реализует ``POST /core/api/selectionClassificators/сlassifyObject``.

    operationId ``SelectionClassificators_ClassifyObject``.

    ВНИМАНИЕ: первая буква сегмента ``сlassifyObject`` в URL — КИРИЛЛИЧЕСКАЯ ``с``
    (U+0441), а не латинская ``c`` (баг IPS API). Путь воспроизводится дословно.
    """

    async def classify_object(
        self: "ClassifyObjectMixin",
        object_id: int,
        classificator_object_ids: list[int],
    ) -> None:
        """Классифицирует объект по указанным классификаторам выбора (мутирующая).

        Выполняет классификацию объекта: привязывает его к перечисленным
        объектам-классификаторам, фиксируя его принадлежность к ним. По смыслу близко к
        :meth:`include_object_in_classificators`, но это отдельная операция API
        классификации (``ClassifyObject``).

        Когда применять: когда нужно классифицировать объект сразу по набору классификаторов
        выбора. Предусловий по жизненному циклу нет — операция применяется к объекту целиком,
        не требует checkout.

        Args:
            object_id: Идентификатор классифицируемого объекта (F_OBJECT_ID, id ОБЪЕКТА, а не
                id версии F_ID). Передаётся в теле как ``objectId``.
            classificator_object_ids: Идентификаторы объектов-классификаторов (F_OBJECT_ID
                объектов, представляющих классификаторы выбора), по которым классифицируется
                объект. Передаются в теле как ``classificatorObjectIds``.

        Returns:
            ``None`` — сервер возвращает ``void``; успехом считается отсутствие ошибки.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.classify_object(102550, [204, 205])

        Notes:
            operationId ``SelectionClassificators_ClassifyObject``; путь
            ``POST /core/api/selectionClassificators/сlassifyObject``; тело —
            ``{"objectId": ..., "classificatorObjectIds": [...]}``.
            БАГ IPS: сегмент ``сlassifyObject`` начинается с КИРИЛЛИЧЕСКОЙ ``с`` (U+0441),
            не латинской ``c``; путь передаётся серверу дословно. Связанный метод —
            :meth:`include_object_in_classificators`. См. [[ips-object-model]].
        """
        await self._request(
            "post",
            "/core/api/selectionClassificators/сlassifyObject",
            json={"objectId": object_id, "classificatorObjectIds": classificator_object_ids},
        )
        return None
