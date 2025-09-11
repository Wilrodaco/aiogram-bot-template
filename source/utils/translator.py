from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator
from fluentogram import TranslatorHub
from loguru import logger
from pathlib import Path

from source.services import UserService


class I18n:
    def __init__(self, hub: TranslatorHub, user_service: UserService):
        self.hub = hub
        self.user_service = user_service

    async def __call__(self, user_id: int, key: str, **kwargs) -> str:
        db_user = await self.user_service.get_user(user_id)

        lang_code = db_user.language_code if db_user else self.hub.root_locale

        translator = self.hub.get_translator_by_locale(lang_code)

        return translator.get(key, **kwargs)


def create_translator_hub() -> TranslatorHub:
    locales_path = Path("source/locales")

    if not locales_path.exists() or not locales_path.is_dir():
        logger.warning(
            f"Locales directory not found at '{locales_path}'. Translations might not work."
        )
        return TranslatorHub({}, [], root_locale="ru")

    return TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en", "ru"),
        },
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    "ru-RU",
                    filenames=[
                        str(p) for p in locales_path.joinpath("ru").glob("*.ftl")
                    ],
                ),
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    "en-US",
                    filenames=[
                        str(p) for p in locales_path.joinpath("en").glob("*.ftl")
                    ],
                ),
            ),
        ],
        root_locale="ru",
    )
