# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ Codrago, 2024-2030
# This file is a part of Pixelazer Userbot
# 🌐 https://github.com/coddrago/Pixelazer
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ GardenYab, 2026-2030
# This file is a part of Pixelazer Userbot
# 🌐 https://github.com/gardenyab/Pixelazer
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import getpass
import logging
import platform as lib_platform
import random
import time
import typing

from pixelazertl.tl.types import Message
from pixelazertl.types import InputMediaWebPage

from .. import loader, main, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

@loader.tds
class Ping(loader.Module):
    """Ping module for Pixelazer"""

    strings = {
        "name": "Ping",
    }
    
    def __init__(self):
        self._memory = {}
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                """<blockquote><tg-emoji emoji-id=5190648194043755386>🚀</tg-emoji> <b>Ping {ping}ms</b>
————
<tg-emoji emoji-id=5204072642608381541>🧩</tg-emoji> <b>Uptime {uptime}</b></blockquote>""",
                lambda: (
                    self.strings["configping"]
                    + (
                        "\n"
                        + self.strings["configpingph"].format(
                            "\n" + utils.config_placeholders()
                        )
                        if utils.config_placeholders()
                        else ""
                    )
                ),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "hints",
                None,
                lambda: self.strings["hint"],
                validator=loader.validators.RandomString(),
            ),
            loader.ConfigValue(
                "always_show_hint",
                False,
                lambda: self.strings["always_show_hint"],
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ping_emoji",
                "🍓",
                lambda: self.strings["ping_emoji"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "banner_url",
                None,
                lambda: self.strings["banner_url"],
                validator=loader.validators.RandomLink(),
            ),
            loader.ConfigValue(
                "quote_media",
                False,
                lambda: self.strings["quote_media"],
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "invert_media",
                False,
                lambda: self.strings["invert_media"],
                validator=loader.validators.Boolean(),
            ),
        )
    
    @staticmethod
    def _get_config_obj_type(instance: typing.Any) -> bool | str:
        if isinstance(instance, loader.Library):
            return "library"
        return instance.__origin__.startswith("<core")
    
    def _resolve_configurable(
            self,
            query: str,
        ) -> tuple[str | None, typing.Any, bool | str | None]:
            if (instance := self.lookup(query)) and hasattr(instance, "config"):
                return query, instance, self._get_config_obj_type(instance)
        
            fuzzy_name, _ = self._fuzzy_lookup_configurable(query)
            if fuzzy_name and (instance := self.lookup(fuzzy_name)):
                if hasattr(instance, "config") and instance.config:
                    return fuzzy_name, instance, self._get_config_obj_type(instance)
        
            return None, None, None
    
    
    @loader.command()
    async def suspend(self, message: Message):
        try:
            time_sleep = float(utils.get_args_raw(message))
            if time_sleep > 86400 * 365 * 100:
                await utils.answer(message, self.strings["suspend_invalid_time"])
            else:
                await utils.answer(
                    message,
                    self.strings["suspended"].format(time_sleep),
                )
                time.sleep(time_sleep)
        except ValueError:
            await utils.answer(message, self.strings["suspend_invalid_time"])

    @loader.command()
    async def ping(self, message: Message):
        """- Find out your userbot ping"""
        start = time.perf_counter_ns()
        message = await utils.answer(message, self.config["ping_emoji"])
        banner = str(self.config["banner_url"])

        if self.config["banner_url"] and self.config["quote_media"] is True:
            banner = InputMediaWebPage(str(self.config["banner_url"]), optional=True)

        elif not self.config["banner_url"]:
            banner = None
        hint = ""
        if self.config["always_show_hint"] and self.config["hints"]: hint = str(self.config["hints"])
        elif self.config["hints"]: 
            if random.choice([0, 0, 1]) == 1:
                hint = str(self.config["hints"])
        data = {
            "ping": round((time.perf_counter_ns() - start) / 10**6, 3),
            "uptime": utils.formatted_uptime(),
            "hint": hint,
            "hostname": lib_platform.node(),
            "user": getpass.getuser(),
            "platform": utils.get_platform_name(),
        }
        data = await utils.get_placeholders(data, self.config["custom_message"])
        try:
            placeholders_msg = self.config["custom_message"].format(**data)
        except KeyError:
            logger.exception("Missing placeholder in custom_message")
            placeholders_msg = "<tg-emoji emoji-id=5210952531676504517>🚫</tg-emoji>"
        await utils.answer(
            message,
            placeholders_msg,
            file=banner,
            invert_media=self.config["invert_media"],
        )

    @loader.command()
    async def setping(self, message: Message):
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings["no_text"])
            return
        mod_name, instance, obj_type = self._resolve_configurable(self.strings["name"])
        instance.config["custom_message"] = text
        await utils.answer(message, self.strings["ping_set"])

    async def client_ready(self):
        self._content_channel_id = await utils.wait_for_content_channel(self._db)
        self.logchat = int(f"-100{self._content_channel_id}")
        logging.getLogger().handlers[0].install_tg_log(self)
        logger.debug("Bot logging installed for %s", self.logchat)