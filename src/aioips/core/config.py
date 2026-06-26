"""Конфигурация клиента IPS Web API."""

from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PasswordType = Literal["plainText", "base64Text"]


class IPSConfig(BaseSettings):
    """Конфигурация подключения и авторизации клиента IPS Web API.

    Pydantic-settings модель: значения берутся (в порядке приоритета) из явных
    аргументов конструктора, переменных окружения и файла ``.env`` в корне
    проекта. Имя переменной окружения = ``IPS_`` + имя поля в верхнем регистре
    (регистр не важен). Например: ``IPS_BASE_URL``, ``IPS_LOGIN_NAME``,
    ``IPS_PASSWORD``, ``IPS_ROLE_NAME``, ``IPS_ACCESS_TOKEN``. Неизвестные
    переменные игнорируются.

    Поддерживаются два взаимоисключающих способа авторизации (нужен ровно один
    валидный набор, иначе валидация падает):

    1. **Логин и пароль** — ``login_name`` + ``password`` (опц. ``role_name``/
       ``role_id`` и ``access_level_id``). Клиент сам получит JWT-токен и будет
       обновлять/перевыпускать его автоматически (см. жизненному циклу токена).
    2. **Готовый токен** — ``access_token``, полученный заранее. Без логина/пароля
       клиент не сможет перевыпустить истёкший токен — будет ``IPSAuthError``.

    Raises:
        pydantic.ValidationError: Если ``base_url`` без схемы ``http(s)://``,
            не задан ни один способ авторизации, либо ``retry_max_wait`` меньше
            ``retry_min_wait``.

    Examples:
        Через переменные окружения (``IPS_BASE_URL``/``IPS_LOGIN_NAME``/``IPS_PASSWORD``)::

            config = IPSConfig()  # значения подхватятся из окружения/.env

        Явно, способ «логин и пароль»::

            config = IPSConfig(
                base_url="http://your-ips-host:8080",
                login_name="your-login",
                password="...",
                role_name="Администратор",
            )

        Явно, способ «готовый токен»::

            config = IPSConfig(base_url="http://your-ips-host:8080", access_token="...")

    Attributes:
        base_url: Базовый URL сервера IPS Web API (например, ``http://host:8080``).
        login_name: Имя пользователя IPS для входа.
        password: Пароль пользователя IPS.
        password_type: Способ передачи пароля (``plainText`` или ``base64Text``).
        role_id: Числовой идентификатор роли (если известен).
        role_name: Имя роли; резолвится в идентификатор автоматически, если ``role_id`` не задан.
        access_level_id: Идентификатор уровня доступа (``0`` — обычный).
        access_token: Заранее полученный JWT access-токен (альтернатива логину/паролю).
        request_timeout: Таймаут запроса в секундах.
        max_retries: Количество повторов при транзиентных ошибках.
        retry_min_wait: Минимальная задержка между повторами в секундах.
        retry_max_wait: Максимальная задержка между повторами в секундах.
        connector_limit: Лимит одновременных HTTP-соединений.
        verify_ssl: Проверять ли TLS-сертификат сервера.
        token_refresh_skew: Запас в секундах: токен обновляется заранее до истечения.
        log_level: Уровень логирования библиотеки.
        log_json: Выводить логи в структурном JSON-формате.
    """

    base_url: str = Field(..., description="Базовый URL сервера IPS Web API")

    login_name: str | None = Field(default=None, description="Имя пользователя IPS")
    password: str | None = Field(default=None, description="Пароль пользователя IPS")
    password_type: PasswordType = Field(default="plainText", description="Способ передачи пароля")
    role_id: int | None = Field(default=None, description="Идентификатор роли")
    role_name: str | None = Field(default=None, description="Имя роли")
    access_level_id: int = Field(default=0, description="Идентификатор уровня доступа")

    access_token: str | None = Field(
        default=None, description="Заранее полученный JWT access-токен"
    )

    request_timeout: float = Field(default=30.0, gt=0, description="Таймаут запроса, сек")
    max_retries: int = Field(default=3, ge=0, le=10, description="Количество повторов")
    retry_min_wait: float = Field(default=1.0, gt=0, description="Мин. задержка повтора, сек")
    retry_max_wait: float = Field(default=10.0, gt=0, description="Макс. задержка повтора, сек")
    connector_limit: int = Field(default=100, ge=1, description="Лимит соединений")
    verify_ssl: bool = Field(default=True, description="Проверять TLS-сертификат")
    token_refresh_skew: float = Field(
        default=30.0, ge=0, description="Запас до истечения токена, сек"
    )

    log_level: str = Field(
        default="ERROR",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Уровень логирования",
    )
    log_json: bool = Field(default=False, description="Логи в формате JSON")

    model_config = SettingsConfigDict(
        env_prefix="IPS_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def _normalize_base_url(self) -> "IPSConfig":
        """Проверяет схему и убирает завершающий слеш у ``base_url``."""
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError("base_url должен начинаться с http:// или https://")
        self.base_url = self.base_url.rstrip("/")
        return self

    @model_validator(mode="after")
    def _validate_credentials(self) -> "IPSConfig":
        """Гарантирует наличие ровно одного валидного набора авторизационных данных."""
        has_token = bool(self.access_token)
        has_login = bool(self.login_name and self.password)
        if not has_token and not has_login:
            raise ValueError(
                "Не заданы авторизационные данные: укажите access_token либо login_name и password"
            )
        return self

    @model_validator(mode="after")
    def _validate_retry_bounds(self) -> "IPSConfig":
        """Проверяет, что максимальная задержка повтора не меньше минимальной."""
        if self.retry_max_wait < self.retry_min_wait:
            raise ValueError("retry_max_wait должен быть >= retry_min_wait")
        return self

    @property
    def uses_token_auth(self) -> bool:
        """Возвращает ``True``, если задан только готовый токен без логина/пароля."""
        return bool(self.access_token) and not (self.login_name and self.password)
