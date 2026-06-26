"""Метод запуска импорта объектов из Портфеля (разрушающая операция)."""

from typing import Any

from ...core import APIManager


class BriefcaseStartImportMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/StartImport`` (``Briefcase_StartImport``)."""

    async def briefcase_start_import(
        self: "BriefcaseStartImportMixin",
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Запускает импорт объектов из Портфеля в базу (РАЗРУШАЮЩАЯ/НЕОБРАТИМАЯ, ``confirm``).

        Портфель — это пакет экспорта/импорта объектов IPS. Метод стартует серверную
        фоновую задачу импорта объектов из портфеля В БАЗУ ДАННЫХ. Это РАЗРУШАЮЩАЯ и
        фактически НЕОБРАТИМАЯ операция: импорт создаёт и/или перезаписывает объекты
        рабочей базы и может затронуть большой объём данных. Поэтому она строго
        защищена ``confirm``: без ``confirm=True`` поднимается :class:`ValueError` ещё
        ДО запроса. ОБЯЗАТЕЛЬНО заранее проверьте совместимость метаданных через
        :meth:`briefcase_check_metadata_start` (или
        :meth:`briefcase_check_metadata_only_start`) и сделайте резервную копию базы;
        статус задачи — :meth:`briefcase_status`, отмена —
        :meth:`briefcase_cancel_import`.

        Тело ``request`` (``ImportRequestDTO``) описывает источник и режим импорта:
        ``id``/``path``/``location``, ``importObjectsOnly``, ``ignoreErrors``,
        ``createOnly`` (только создавать, не обновлять), ``synchronizeIMS_CONFIGS``,
        ``newOwnerId``. Параметр ``createOnly`` снижает риск перезаписи существующих
        объектов.

        Args:
            request: Тело запроса ``ImportRequestDTO`` в виде словаря; отправляется
                как JSON-тело.
            confirm: Подтверждение РАЗРУШАЮЩЕЙ операции. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``. Метод лишь запускает импорт; исход/статус читаются отдельно
            (:meth:`briefcase_status`).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.briefcase_check_metadata_start({"path": p}, confirm=True)
                # ... убедиться, что результат проверки чистый, есть бэкап базы ...
                await ips.briefcase_start_import(
                    {"path": p, "createOnly": True, "ignoreErrors": False},
                    confirm=True,
                )

        Notes:
            РАЗРУШАЮЩАЯ операция: импортирует данные в рабочую базу, перезапись
            необратима. operationId ``Briefcase_StartImport``; путь
            ``POST /core/api/briefcase/StartImport`` (тело ``ImportRequestDTO``).
            Связанные: :meth:`briefcase_check_metadata_start`,
            :meth:`briefcase_cancel_import`, :meth:`briefcase_status`.
        """
        if confirm is not True:
            raise ValueError(
                "Импорт Портфеля РАЗРУШАЮЩИЙ и необратимый (запись в базу): передайте confirm=True"
            )
        await self._request(
            "post",
            "/core/api/briefcase/StartImport",
            json=request,
        )
