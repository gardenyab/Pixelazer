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

import getpass
import inspect
import logging
import os
import platform as lib_platform
import random
import time
from io import BytesIO

from pixelazertl.tl.types import Message
from pixelazertl.types import InputMediaWebPage

from .. import loader, main, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

DEBUG_MODS_DIR = os.path.join(utils.get_base_dir(), "debug_modules")

if not os.path.isdir(DEBUG_MODS_DIR):
    os.mkdir(DEBUG_MODS_DIR, mode=0o755)

for mod in os.scandir(DEBUG_MODS_DIR):
    os.remove(mod.path)


@loader.tds
class LoggerMod(loader.Module):
    """Perform operations based on userbot self-testing"""

    strings = {
        "name": "Logger"
    }

    def __init__(self):
        self._memory = {}
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "force_send_all",
                False,
                lambda: self.strings["cfg_force_send_all"],
                validator=loader.validators.Boolean(),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "tglog_level",
                "ERROR",
                lambda: self.strings["cfg_tglog_level"],
                validator=loader.validators.Choice(
                    ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "DISABLE"]
                ),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "ignore_common",
                True,
                lambda: self.strings["cfg_ignore_common"],
                validator=loader.validators.Boolean(),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "disable_internet_warn",
                False,
                lambda: self.strings["cfg_disable_internet_warn"],
                validator=loader.validators.Boolean(),
            )
        )

    def _pass_config_to_logger(self):
        logging.getLogger().handlers[0].force_send_all = self.config["force_send_all"]
        logging.getLogger().handlers[0].tg_level = {
            "ALL": 0,
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50,
            "DISABLE": 50000,
        }[self.config["tglog_level"]]
        logging.getLogger().handlers[0].ignore_common = self.config["ignore_common"]

    @loader.command()
    async def clearlogs(self, message: Message):
        for handler in logging.getLogger().handlers:
            handler.buffer = []
            handler.handledbuffer = []
            handler.tg_buff = ""

        await utils.answer(message, self.strings["logs_cleared"])

    @loader.command()
    async def logs(
        self,
        message: Message | InlineCall,
        force: bool = False,
        lvl: int | None = None,
    ):
        raw_args = utils.get_args_raw(message) if isinstance(message, Message) else ""
        args = raw_args.split()
        if "-f" in args or "--force" in args:
            force = True
            args = [arg for arg in args if arg not in {"-f", "--force"}]

        if not isinstance(lvl, int):
            if args:
                try:
                    try:
                        lvl = int(args[0])
                    except ValueError:
                        lvl = getattr(logging, args[0].upper(), None)
                except IndexError:
                    lvl = None
            else:
                lvl = None

        if not isinstance(lvl, int):
            if force:
                await utils.answer(message, self.strings["set_loglevel"])
                return

            try:
                if self.inline.init_complete:
                    await utils.answer(
                        message,
                        self.strings["choose_loglevel"],
                        reply_markup=utils.chunks(
                            [
                                {
                                    "text": name,
                                    "callback": self.logs,
                                    "args": (False, level),
                                }
                                for name, level in [
                                    ("🚫 Critical", 60),
                                    ("🚫 Error", 40),
                                    ("⚠️ Warning", 30),
                                    ("ℹ️ Info", 20),
                                    ("⚠️ Debug", 10),
                                    ("🧑‍💻 All", 0),
                                ]
                            ],
                            2,
                        )
                        + [[{"text": self.strings["cancel"], "action": "close"}]],
                    )
                else:
                    raise
            except Exception as e:
                await utils.answer(message, self.strings["set_loglevel"] + f"\n{e}")

            return

        logs = "\n\n".join(
            [
                "\n".join(
                    handler.dumps(lvl, client_id=self._client.tg_id)
                    if "client_id" in inspect.signature(handler.dumps).parameters
                    else handler.dumps(lvl)
                )
                for handler in logging.getLogger().handlers
            ]
        )

        named_lvl = (
            lvl
            if lvl not in logging._levelToName
            else logging._levelToName[lvl]  # skipcq: PYL-W0212
        )

        if lvl < logging.WARNING and not force:
            try:
                if not self.inline.init_complete:
                    raise

                cfg = {
                    "text": self.strings["confidential"].format(named_lvl),
                    "reply_markup": [
                        {
                            "text": self.strings["send_anyway"],
                            "callback": self.logs,
                            "args": [True, lvl],
                        },
                        {"text": self.strings["cancel"], "action": "close"},
                    ],
                }
                if isinstance(message, Message):
                    if not await self.inline.form(**cfg, message=message):
                        raise
                else:
                    await message.edit(**cfg)
            except Exception:
                await utils.answer(
                    message,
                    self.strings["confidential_text"].format(named_lvl),
                )

            return

        if len(logs) <= 2:
            await utils.answer(
                message,
                self.strings["no_logs"].format(named_lvl),
                **(
                    {}
                    if force
                    else {
                        "reply_markup": {
                            "text": self.strings["back"],
                            "callback": self.logs,
                        },
                    }
                ),
            )
            return

        logs = self.lookup("evaluator").censor(logs)

        logs = BytesIO(logs.encode("utf-8"))
        logs.name = "pixelazer-logs.txt"

        ghash = utils.get_git_hash()

        other = (
            *main.__version__,
            (
                " <a"
                f' href="https://github.com/ gardenyab/Pixelazer/commit/{ghash}">@{ghash[:8]}</a>'
                if ghash
                else ""
            ),
        )

        caption = self.strings["logs_caption"].format(named_lvl, *other)

        if isinstance(message, Message):
            await utils.answer(
                message,
                caption,
                file=logs,
            )
        else:
            await self._client.send_file(
                message.form["chat"],
                logs,
                caption=caption,
                reply_to=message.form["top_msg_id"],
            )

    async def client_ready(self):
        self._content_channel_id = await utils.wait_for_content_channel(self._db)
        self.logchat = int(f"-100{self._content_channel_id}")
        logging.getLogger().handlers[0].install_tg_log(self)
        logger.debug("Bot logging installed for %s", self.logchat)

        self._pass_config_to_logger()
