"""Метод сохранения масштаба диаграммы Ганта проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.improjects import ScaleType


class SaveProjectZoomLevelMixin(APIManager):
    """Реализует ``POST /core/api/improjects/{projectId}/saveZoomLevel``.

    ``operationId``: ``ImProject_SaveProjectZoomLevel``.
    """

    async def save_project_zoom_level(
        self: "SaveProjectZoomLevelMixin",
        project_id: int,
        *,
        scale_type: ScaleType | str | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Сохраняет масштаб (zoom) шкалы времени диаграммы Ганта проекта (МУТАЦИЯ).

        Назначение: запомнить выбранный пользователем масштаб отображения
        план-графика (дни/недели/месяцы/кварталы/годы). Это настройка
        представления, не данные проекта. Применяйте при сохранении вида
        диаграммы Ганта на клиенте.

        Предусловие: проект ``project_id`` существует; модуль Improject
        лицензирован.

        Обратимость: ОБРАТИМА — повторным :meth:`save_project_zoom_level` с
        прежним масштабом.

        Защита: меняет настройку на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            project_id: Числовой идентификатор проекта (``projectId`` в пути).
            scale_type: Масштаб шкалы времени (query ``scaleType``): член
                :class:`ScaleType` (``days``/``weeks``/``months``/``quarters``/
                ``years``) или строка. ``None`` — не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``GanttOperationResult`` (значимый ключ
            ``action`` — описание операции Ганта).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.improjects import ScaleType
            async with IPSClient(config=config) as ips:
                await ips.save_project_zoom_level(
                    1500, scale_type=ScaleType.MONTHS, confirm=True
                )

        Notes:
            ``operationId``: ``ImProject_SaveProjectZoomLevel``; путь
            ``POST /core/api/improjects/{projectId}/saveZoomLevel`` (query
            ``scaleType`` — enum ``ScaleType``; тело ``{}`` против 415; ответ
            ``GanttOperationResult``).
        """
        if confirm is not True:
            raise ValueError(
                "save_project_zoom_level меняет настройку отображения; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if scale_type is not None:
            params["scaleType"] = str(scale_type)
        data = await self._request(
            "post",
            f"/core/api/improjects/{project_id}/saveZoomLevel",
            params=params,
            json={},
        )
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
