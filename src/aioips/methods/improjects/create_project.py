"""Метод создания проекта управления проектами (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class CreateProjectMixin(APIManager):
    """Реализует ``POST /core/api/improjects/project`` (``ImProject_CreateProject``)."""

    async def create_project(
        self: "CreateProjectMixin",
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Создаёт новый проект Improject (план-график / диаграмму Ганта) (МУТАЦИЯ).

        Назначение: завести в системе новый проект управления проектами. Проект —
        это объект IPS (со своим ``objectID``), внутрь которого затем добавляют
        задачи (:meth:`create_task`) и зависимости (:meth:`create_dependency`).
        Применяйте как первый шаг сценария Gantt-планирования. Загрузить готовый
        проект целиком — :meth:`project`.

        Предусловие: модуль Improject (управление проектами) должен быть
        лицензирован. Тело ``request`` соответствует DTO ``CreateProjectDto``
        (ключи ``camelCase``): ``objectTypeId`` — тип объекта проекта,
        ``name`` — наименование, ``prototypeId`` — id прототипа (опционально),
        ``outRelations`` — исходящие связи (опционально).

        Обратимость: ОТДЕЛЬНОГО метода удаления проекта в API НЕТ. Созданный
        проект удаляется как обычный объект IPS — :meth:`object_delete` по его
        ``objectID`` (поле ``objectId`` в ответе) с ``confirm=True``.

        Защита: создаёт объект на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            request: Тело запроса ``CreateProjectDto`` в виде словаря с ключами
                ``camelCase`` (``objectTypeId``, ``name``, ``prototypeId``,
                ``outRelations``).
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``CreateProjectResult``. Значимый ключ
            ``objectId`` — ``objectID`` созданного проекта (используйте его для
            :meth:`project` и :meth:`object_delete`).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                res = await ips.create_project(
                    {"objectTypeId": 4, "name": "Новый проект"},
                    confirm=True,
                )
                project_id = res["objectId"]

        Notes:
            ``operationId``: ``ImProject_CreateProject``; путь
            ``POST /core/api/improjects/project`` (тело ``CreateProjectDto``,
            ответ ``CreateProjectResult``). Связанные методы: :meth:`create_task`,
            :meth:`create_dependency`, :meth:`project`, :meth:`object_delete`.
        """
        if confirm is not True:
            raise ValueError(
                "create_project создаёт проект (объект IPS); передайте confirm=True",
            )
        data = await self._request("post", "/core/api/improjects/project", json=request)
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
