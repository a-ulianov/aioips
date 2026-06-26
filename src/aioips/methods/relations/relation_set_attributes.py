"""Метод установки набора атрибутов связи (запись)."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute


class RelationSetAttributesMixin(APIManager):
    """Реализует ``RelationAttributes_SetAttributes`` (запись набора атрибутов связи)."""

    async def relation_set_attributes(
        self: "RelationSetAttributesMixin",
        relation_id: int,
        attributes: list[Attribute],
        *,
        log_history: bool = True,
    ) -> list[Attribute]:
        """Записывает (заменяет) набор атрибутов СВЯЗИ переданным списком ``Attribute``.

        Связь в IPS — атрибутируемая сущность (``IDBAttributable``) со своими
        характеристиками (например, позиционное обозначение или количество в составе).
        Этот метод задаёт атрибуты именно связи как готовые DTO ``Attribute`` (с типом,
        значениями и метаданными). Применяйте, когда у вас уже есть собранные объекты
        :class:`Attribute` (например, прочитанные :meth:`relation_attributes` и
        изменённые). Для точечной записи значений по их спискам удобнее
        :meth:`relation_set_attribute_values`.

        ПРЕДУСЛОВИЕ (запись связи): объект-РОДИТЕЛЬ связи (``projID`` = ObjectID
        родителя) должен быть извлечён на редактирование — взят на изменение (checkout)
        в режиме, разрешающем правку на текущем шаге ЖЦ. Без активного checkout родителя
        запись атрибутов связи невозможна (сервер вернёт ошибку). Это отличает запись
        от чтения (:meth:`relation_attributes`), которому checkout не нужен.

        Отличие от записи атрибутов ОБЪЕКТА: запись объекта адресуется по ``objectID``
        и затрагивает сам объект; здесь адресация — по ``relationID`` и изменяется
        связь (её собственные атрибуты), а не её объекты-концы.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. объектной модели IPS).
            attributes: Список атрибутов связи к записи (схема :class:`Attribute`).
                Каждый сериализуется в ``AttributeDto`` через
                ``model_dump(mode="json", by_alias=True, exclude_none=True)``;
                тело запроса — голый JSON-массив этих DTO.
            log_history: Если ``True`` (по умолчанию), сервер логирует историю
                модификаций атрибутов; если ``False`` — запись без журналирования.

        Returns:
            Список атрибутов связи (схема :class:`Attribute`) после записи — поле
            ``result`` ответа ``AttributeDtoListProcessResultWithLogInfoDto``. Пустой
            список, если сервер не вернул ``result``.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если родитель связи не
                извлечён на редактирование или правка запрещена шагом ЖЦ).

        Example:
            async with IPSClient(config=config) as ips:
                # Предполагается, что родитель связи уже на checkout.
                current = await ips.relation_attributes(700123)
                current[0].values = ["A1"]
                result = await ips.relation_set_attributes(700123, current)

        Notes:
            ``operationId``: ``RelationAttributes_SetAttributes``. Тело запроса —
            JSON-массив ``AttributeDto``; ответ — обёртка с журналом модификаций
            (``...ProcessResultWithLogInfoDto``), из которой возвращается ``result``.
            См. объектной модели IPS (разделы «Редактирование», «Связи и состав»).
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        payload = [a.model_dump(mode="json", by_alias=True, exclude_none=True) for a in attributes]
        data = await self._request(
            "post",
            f"/core/api/relations/{relation_id}/attributes",
            json=payload,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        items = result if isinstance(result, list) else []
        return [Attribute.model_validate(item) for item in items]
