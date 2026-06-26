"""Метод генерации содержимого табличного отчёта объекта IPS."""

from ...core import APIManager
from ...schemas.table_report import DocumentContent, ReportCreatorParams


class ReportContentMixin(APIManager):
    """Реализует ``POST /core/api/tableReport/{objectId}/reportContent``.

    operationId ``TableReport_GetReportContent``.
    """

    async def report_content(
        self: "ReportContentMixin", object_id: int, params: ReportCreatorParams
    ) -> DocumentContent:
        """Генерирует содержимое табличного отчёта для объекта IPS.

        Формирует документ табличного отчёта по настроенному для объекта шаблону и
        возвращает его содержимое в объектной модели IPS (дерево страниц, шаблон,
        метаданные), а не готовый бинарный файл. Состав отчёта управляется параметрами
        :class:`ReportCreatorParams` (явный список выбранных элементов, флаг «только
        выбранные», именованная выборка).

        Когда применять: чтобы получить наполнение табличного отчёта объекта для
        дальнейшей обработки или предпросмотра. Чтобы прочитать саму конфигурацию
        отчёта (колонки, итоги) без генерации содержимого, используйте
        :meth:`table_report`.

        Предусловие по id-пространству: аргумент ``object_id`` — идентификатор ОБЪЕКТА
        (``objectID`` / F_OBJECT_ID), общий для всех версий, а не идентификатор версии
        (``id`` / F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                генерируется содержимое отчёта. Не идентификатор версии.
            params: Параметры формирования (:class:`ReportCreatorParams`): ``selected_ids``,
                ``parent_type_id``, ``only_selected``, ``selection_id``. При значениях по
                умолчанию формируется отчёт по полному составу.

        Returns:
            Содержимое документа по схеме :class:`DocumentContent`: страницы
            (``doc_pages``), корень шаблона (``template_root``), имя файла (``file_name``)
            и метаданные документа.

        Raises:
            IPSError: При ошибочном ответе сервера (в т. ч. 404, если для объекта нет
                настроенного табличного отчёта).

        Example:
            from aioips.schemas.table_report import ReportCreatorParams

            async with IPSClient(config=config) as ips:
                content = await ips.report_content(
                    102550,  # 102550 = objectID
                    ReportCreatorParams(only_selected=False),
                )
                print(content.file_name, len(content.doc_pages))

        Notes:
            operationId ``TableReport_GetReportContent``; путь
            ``POST /core/api/tableReport/{objectId}/reportContent`` (ответ —
            ``DocumentContentDto``). Связанный метод: :meth:`table_report`.
        """
        payload = params.model_dump(by_alias=True, exclude_none=True)
        data = await self._request(
            "post",
            f"/core/api/tableReport/{object_id}/reportContent",
            json=payload,
        )
        return DocumentContent.model_validate(data)
