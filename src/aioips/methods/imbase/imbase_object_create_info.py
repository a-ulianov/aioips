"""Метод получения информации о создании объекта на основе элемента IMBASE."""

from ...core import APIManager
from ...schemas.imbase import ImBaseObjectCreateInfo


class ImBaseObjectCreateInfoMixin(APIManager):
    """Реализует ``GET /core/api/imbase/object/{baseId}/createInfo``."""

    async def imbase_object_create_info(
        self: "ImBaseObjectCreateInfoMixin",
        base_id: int,
    ) -> ImBaseObjectCreateInfo:
        """Возвращает информацию о создании объекта на основе элемента IMBASE.

        Подсказывает, как создавать объект по записи (элементу) IMBASE: создавать ли
        новый объект, какого типа, и какие объекты уже были созданы по этому же
        элементу (чтобы предложить переиспользование вместо дублирования).

        Когда применять: перед созданием объекта из записи IMBASE — для выбора типа и
        проверки уже существующих объектов. Ответ — ``ImBaseObjectCreateInfoDto`` без
        result-обёртки (всегда возвращается объект, не ``None``).

        Args:
            base_id: Идентификатор элемента (записи) IMBASE, по которому создаётся
                объект (id-пространство элементов IMBASE).

        Returns:
            Информация по схеме :class:`ImBaseObjectCreateInfo`:
            ``should_create_new_object`` (создавать ли новый), ``object_type_id`` (тип)
            и ``existing_objects`` (уже созданные объекты).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.imbase_object_create_info(555444)
                if info.should_create_new_object:
                    print("создать тип", info.object_type_id)
                else:
                    print("уже есть", info.existing_objects)

        Notes:
            operationId ``ImBase_GetObjectCreateInfo``; путь
            ``GET /core/api/imbase/object/{baseId}/createInfo``
            (``ImBaseObjectCreateInfoDto``, без result-обёртки).
        """
        data = await self._request("get", f"/core/api/imbase/object/{base_id}/createInfo")
        return ImBaseObjectCreateInfo.model_validate(data)
