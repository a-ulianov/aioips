"""Метод добавления демо-сообщения (samples)."""

from typing import Any

from ...core import APIManager


class AddMessageSampleMixin(APIManager):
    """Реализует ``POST /core/api/samples/messages`` (``Messages_Add``)."""

    async def add_sample_message(
        self: "AddMessageSampleMixin",
        message: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Добавляет демо-сообщение в учебный раздел ``samples`` (мутация, ``confirm``).

        Раздел ``samples`` — демонстрационный (учебный) API сообщений; на доменные
        объекты IPS не влияет. Операция изменяет состояние сервера, поэтому защищена
        гейтом: без ``confirm=True`` метод не делает запрос и поднимает
        :class:`ValueError`. Обратима: добавленное сообщение удаляется методом
        :meth:`delete_message` по его ``id`` из ответа.

        Args:
            message: Тело запроса ``AddMessageDTO`` как ``dict`` с ключами ``id`` и
                ``text``. ``id = 0`` означает, что сервер присвоит идентификатор
                автоматически. Типизированно сформировать тело можно через
                :class:`aioips.schemas.samples.AddMessage`
                (``model_dump(by_alias=True)``).
            confirm: Подтверждение мутации. Без ``True`` запрос не выполняется
                (защитный гейт).

        Returns:
            Созданное сообщение (``FullMessageDTO``) как ``dict[str, Any]`` с ключами
            ``id``, ``createTime``, ``lastWriteTime``, ``text``. Поле ``id`` используйте
            для последующего :meth:`delete_message` / :meth:`update_message`.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                created = await ips.add_sample_message(
                    {"id": 0, "text": "привет"}, confirm=True
                )
                await ips.delete_message(created["id"], confirm=True)  # откат

        Notes:
            operationId ``Messages_Add``; путь ``POST /core/api/samples/messages``
            (тело ``AddMessageDTO``, ответ ``FullMessageDTO``). Обратный метод:
            :meth:`delete_message`.
        """
        if confirm is not True:
            raise ValueError("Добавление демо-сообщения меняет состояние: передайте confirm=True")
        data = await self._request("post", "/core/api/samples/messages", json=message)
        return dict(data)
