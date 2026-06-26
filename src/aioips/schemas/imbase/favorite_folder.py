"""Схема папки избранного IMBASE (результат добавления объекта в избранное).

References:
    ``POST /core/api/imbase/favorites/{selectedFavoriteFolderId}/add/{objectId}`` —
    ``FavoriteFolderDto`` (без result-обёртки).
"""

from pydantic import Field

from ..base import IPSModel


class FavoriteFolderDto(IPSModel):
    """Связь объекта с папкой избранного IMBASE (личная закладка пользователя).

    Описывает результат добавления объекта в папку избранного: какой объект был
    помещён в закладки и какой идентификатор связи (закладки) при этом создан.
    Избранное — личная пользовательская навигация поверх объектов справочника;
    добавление НЕ меняет сам объект и обратимо (см.
    :meth:`imbase_remove_from_favorites`).

    Когда применять: как ответ метода :meth:`imbase_add_to_favorite_folder`, чтобы
    узнать ``relation_id`` созданной закладки. Чтобы её снять, в обратный вызов
    передают ``object_id`` (id папки берётся из исходного вызова add).

    Attributes:
        object_id: Идентификатор ОБЪЕКТА (``ObjectID`` / F_OBJECT_ID, общий для
            версий), добавленного в избранное. По умолчанию ``0``.
        relation_id: Идентификатор связи-закладки (``RelationID``) между папкой
            избранного и объектом. По умолчанию ``0``. Внимание: ``RelationID``
            нестабилен между запросами — не кэшировать долговременно.
    """

    object_id: int = Field(default=0, description="ObjectID объекта в избранном")
    relation_id: int = Field(default=0, description="RelationID связи-закладки")
