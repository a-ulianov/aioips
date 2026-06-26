"""Сборка публичного клиента IPS из методов-разделов."""

from .methods import (
    ArchivesAPI,
    AttributeHistoryAPI,
    AuthAPI,
    BridgeAPI,
    BriefcaseAPI,
    CalendarsAPI,
    ConfigAPI,
    CryptoSigningAPI,
    DiscussionsAPI,
    DocsAPI,
    DocumentEditorAPI,
    DocumentsAPI,
    EditingContextsAPI,
    FilesAPI,
    FileSystemsAPI,
    FormsAPI,
    GraphSignsAPI,
    ImBaseAPI,
    ImProjectsAPI,
    ImViewerAPI,
    LicensesAPI,
    MailAgentAPI,
    MeasureUnitsAPI,
    MetadataAPI,
    NotifyAPI,
    ObjectsAPI,
    ObjectTypesAPI,
    RelationQueriesAPI,
    RelationsAPI,
    RelationTypesAPI,
    SamplesAPI,
    SearchSchemesAPI,
    SecurityAPI,
    SelectionClassificatorsAPI,
    SettingsAPI,
    SignsAPI,
    SnapshotsAPI,
    SsoAPI,
    TableReportAPI,
    UsersAPI,
    VisibilitiesAPI,
    WorkflowAPI,
)


class IPSClient(
    ArchivesAPI,
    AttributeHistoryAPI,
    AuthAPI,
    BridgeAPI,
    BriefcaseAPI,
    CalendarsAPI,
    ConfigAPI,
    CryptoSigningAPI,
    DiscussionsAPI,
    DocsAPI,
    DocumentEditorAPI,
    DocumentsAPI,
    EditingContextsAPI,
    FilesAPI,
    FileSystemsAPI,
    FormsAPI,
    GraphSignsAPI,
    ImBaseAPI,
    ImProjectsAPI,
    ImViewerAPI,
    LicensesAPI,
    MailAgentAPI,
    MeasureUnitsAPI,
    MetadataAPI,
    NotifyAPI,
    ObjectsAPI,
    ObjectTypesAPI,
    RelationQueriesAPI,
    RelationsAPI,
    RelationTypesAPI,
    SamplesAPI,
    SearchSchemesAPI,
    SecurityAPI,
    SelectionClassificatorsAPI,
    SettingsAPI,
    SignsAPI,
    SnapshotsAPI,
    SsoAPI,
    TableReportAPI,
    UsersAPI,
    VisibilitiesAPI,
    WorkflowAPI,
):
    """Основной асинхронный клиент IPS Server Web API.

    Единая точка входа библиотеки: объединяет все реализованные разделы API
    (auth, metadata, objects, relations, users, единицы измерения и др.) в один
    интерфейс через множественное наследование mixin-классов. Получение и
    обновление JWT-токена, повторы при транзиентных ошибках и маппинг ответов в
    исключения берёт на себя ядро (см. :class:`aioips.core.APIManager`).

    Создавайте через ``IPSConfig`` или параметры-ярлыки конструктора и
    используйте как асинхронный контекстный менеджер (``async with``), чтобы
    гарантированно закрыть HTTP-сессию. Каждый публичный метод-раздел
    документирован отдельно и пригоден как описание MCP-инструмента.

    Notes:
        Реальные адрес сервера, логин и пароль должны приходить из окружения
        (``.env``/env-переменные ``IPS_*``), не из исходного кода.

    Examples:
        import asyncio

        from aioips import IPSClient, IPSConfig

        async def main() -> None:
            config = IPSConfig(
                base_url="http://your-ips-host:8080",
                login_name="your-login",
                password="...",
                role_name="Администратор",
            )
            async with IPSClient(config=config) as ips:
                me = await ips.user_info()
                types = await ips.object_types()
                print(me.login_name, len(types))

        if __name__ == "__main__":
            asyncio.run(main())
    """
