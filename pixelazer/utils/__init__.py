# Utilites

from .messages import *
from .other import *
from .entity import *
from .pixelazer import *
from .platform import *
from .git import *
from .args import *
from .network import *
from .placeholders import *

def getBlockedStr() -> str:
    return {
        "critical": [
            {"command": "DeleteAccountRequest", "perms": "delete account"},
            {"command": "edit_2fa", "perms": "change 2FA password"},
            {"command": "disconnect", "perms": "disconnect account"},
            {"command": "log_out", "perms": "disconnect account"},
            {"command": "ResetAuthorizationRequest", "perms": "kill account sessions"},
            {"command": "GetAuthorizationsRequest", "perms": "get telegram api_id and api_hash"},
            {"command": "AddRequest", "perms": "get telegram api_id and api_hash"},
            {"command": "pyarmor", "perms": "all(obfuscated script)"},
            {"command": "pyrogram", "perms": "another tg client"},
            {"command": "system", "perms": "presumably eval commands"},
            {"command": "eval", "perms": "presumably eval python code"},
            {"command": "exec", "perms": "presumably exec python code"},
            {"command": ".sessions", "perms": "get all sessions data"},
            {"command": "subprocess", "perms": "eval commands"},
            {"command": "torpy", "perms": "download viruses"},
            {"command": "httpimport", "perms": "import malicious scripts"},
            {"command": "\".session\"", "perms": "attempt to get session file"},
            {"command": ".endswith(\".session\"):", "perms": "attempt to get session file"},
        ],
        "warn": [
            {"command": "list_sessions", "perms": "get all account sessions"},
            {"command": "LeaveChannelRequest", "perms": "leave channel and chats"},
            {"command": "JoinChannelRequest", "perms": "join channel and chats"},
            {"command": "ChannelAdminRights", "perms": "edit channel and chats users perms"},
            {"command": "EditBannedRequest", "perms": "kick and ban users"},
            {"command": "rmdir", "perms": "presumably remove dirs"},
            {"command": "get_response", "perms": "get telegram messages"},
            {"command": "CustomTelegramClient", "perms": "attempt to create another client"},
        ],
        "council": [
            {"command": "requests", "perms": "send requests"},
            {"command": "get_entity", "perms": "get entities"},
            {"command": "get_dialogs", "perms": "get dialogs"},
            {"command": "import", "perms": "import modules"},
            {"command": "client", "perms": "all client functions"},
            {"command": "send_message", "perms": "send messages"},
            {"command": "send_file", "perms": "send files"},
            {"command": "TelegramClient", "perms": "create new session"},
            {"command": "download_file", "perms": "download telegram files"},
            {"command": "ModuleConfig", "perms": "create configs"},
        ],
    } # thx @vsecoder_m

async def check_m(args):
    string = args
    results = {
        "critical": {},
        "warn": {},
        "council": {}
    }

    crts = getBlockedStr()

    for category in results.keys():
        for command in crts.get(category, []):
            if re.search(command["command"], string) is not None:
                results[category][command["command"]] = command["perms"]

    return {
        "critical": results["critical"],
        "warn": results["warn"],
        "council": results["council"],
        "args": args,
        "unsafe": bool(results["critical"]),
        "unsafe_warn": bool(results["warn"])
    }