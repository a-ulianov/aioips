"""Метод сохранения шаблона табличного отчёта IPS (мутация)."""

from typing import Any

from ...core import APIManager


class UpdateReportTemplateMixin(APIManager):
    """Реализует ``POST /core/api/tableReport/create``.

    operationId ``TableReport_UpdateReportTemplate``.
    """

    async def update_report_template(
        self: "UpdateReportTemplateMixin",
        template: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Создаёт или обновляет шаблон табличного отчёта объекта (МУТАЦИЯ).

        Записывает конфигурацию табличного отчёта (``TableReportDto``): привязку шаблона
        и отчёта, состав и порядок колонок, правила нумерации строк и набор итоговых
        элементов (итоговая строка, количество позиций, дата печати, номера страниц).
        Несмотря на путь ``/create``, операция выполняет upsert — отсюда имя метода
        «update». Это операция ЗАПИСИ, изменяющая серверное состояние.

        Когда применять: при программной настройке табличного отчёта для объекта —
        задании или изменении выводимых колонок и итогов. Прочитать текущий шаблон можно
        методом :meth:`table_report` по идентификатору объекта.

        Обратимость: операция ОБРАТИМА по схеме write-same-back — прочитайте текущий
        шаблон через :meth:`table_report`, сохраните его и для отката запишите обратно
        этим же методом. Рекомендуется сделать резервную копию исходного ``TableReportDto``.

        Защита: меняет настройку отчёта на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к серверу.

        Args:
            template: Тело шаблона — словарь ``TableReportDto`` (ключи ``camelCase`` с
                акронимами ``templateID``/``reportID``, как их отдаёт :meth:`table_report`).
                Передаётся телом запроса (``json=template``) без преобразований.
            confirm: Подтверждение операции записи. Без ``True`` запрос НЕ выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.table_report(102550)  # objectID
                body = current.model_dump(by_alias=True)
                await ips.update_report_template(body, confirm=True)

        Notes:
            operationId ``TableReport_UpdateReportTemplate``; путь
            ``POST /core/api/tableReport/create``. Тело — ``TableReportDto``
            (``json=template``); query не требуется. Ответ — void (None).
        """
        if confirm is not True:
            raise ValueError(
                "update_report_template сохраняет шаблон табличного отчёта (меняет настройку); "
                "передайте confirm=True",
            )
        await self._request("post", "/core/api/tableReport/create", json=template)
        return None
