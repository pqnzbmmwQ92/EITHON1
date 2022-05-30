# Copyright (C) 2021 Ξ𝗜𝗧𝗛𝗢𝗡™ TEAM

import telethon.password as pwd_mod
from telethon.tl import functions

from EITHON1 import jmthon

from ..Config import Config

plugin_category = "utils"


@jmthon.ar_cmd(
    pattern="ملكية (.*)",
    command=("ملكية", plugin_category),
    info={
        "header": "To transfer channel ownership.",
        "description": "Transfers ownership to the given username for this set this var `TG_2STEP_VERIFICATION_CODE` in heroku with your 2-step verification code.",
        "usage": "{tr}otransfer <username to whom you want to transfer>",
    },
)
# For EITHON1

async def _(event):
    "To transfer channel ownership"
    user_name = event.pattern_match.group(1)
    try:
        pwd = await event.client(functions.account.GetPasswordRequest())
        my_srp_password = pwd_mod.compute_check(pwd, Config.TG_2STEP_VERIFICATION_CODE)
        await event.client(
            functions.channels.EditCreatorRequest(
                channel=event.chat_id, user_id=user_name, password=my_srp_password
            )
        )
    except Exception as e:
        await event.edit(f"**خـطأ:**\n`{str(e)}`")
    else:
        await event.edit("⌯︙تم نقل المـلكية بنـجاح ✅")
