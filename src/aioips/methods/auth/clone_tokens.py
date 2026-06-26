"""Метод клонирования пары токенов сессии IPS."""

from typing import Any

from ...core import APIManager


class CloneTokensMixin(APIManager):
    """Реализует ``POST /core/api/Auth/cloneTokens`` (``Auth_CloneTokens``)."""

    async def clone_tokens(
        self: "CloneTokensMixin",
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """Клонирует пару токенов сессии IPS, выдавая первичную и вторичную пары.

        По текущей паре ``ApiTokensDTO`` выпускает связанную («клонированную») пару
        токенов. Применяется, когда нужно завести параллельную сессию на той же
        учётной записи — например, для отдельного фонового процесса/интеграции, не
        затрагивая исходную сессию. Это явный низкоуровневый вызов: внутреннее
        состояние клиента он не изменяет и результат не кэширует.

        Когда применять: получить вторую (вторичную) пару токенов от существующей
        сессии. В отличие от :meth:`refresh_tokens` (продление той же сессии), здесь
        возвращаются ДВЕ пары — первичная и вторичная. Предусловие: исходная пара
        токенов действительна.

        Args:
            request: Тело ``ApiTokensDTO`` как ``dict``. Ключи (camelCase):
                ``accessToken`` (str), ``refreshToken`` (str), ``expireTime``
                (ISO-8601 UTC, str). Передаётся как есть.

        Returns:
            ``ClonedApiTokensDTO`` как ``dict[str, Any]`` с двумя вложенными парами:
            ``primaryPair`` и ``secondaryPair`` (каждая — ``ApiTokensDTO`` с ключами
            ``accessToken``/``refreshToken``/``expireTime``). Возвращается как есть;
            пустой ``dict``, если сервер вернул не объект.

        Raises:
            IPSAuthError: Если исходная пара недействительна (``401``).
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cloned = await ips.clone_tokens(
                    {
                        "accessToken": access,
                        "refreshToken": refresh,
                        "expireTime": "2026-06-25T10:00:00Z",
                    }
                )
                secondary_access = cloned["secondaryPair"]["accessToken"]

        Notes:
            operationId ``Auth_CloneTokens``; путь ``POST /core/api/Auth/cloneTokens``;
            тело ``ApiTokensDTO``; ответ ``ClonedApiTokensDTO``. Связанные:
            :meth:`authenticate`, :meth:`refresh_tokens`. Домен: разделу авторизации.
        """
        data = await self._request("post", "/core/api/Auth/cloneTokens", json=request)
        return data if isinstance(data, dict) else {}
