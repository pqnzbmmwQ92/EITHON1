# Copyright (C) 2021 ฮ๐๐ง๐๐ข๐กโข TEAM
# FILES WRITTEN BY  @RR7PP

import asyncio

from EITHON1 import EITHON1

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import ALIVE_NAME

plugin_category = "fun"


@EITHON1.ar_cmd(
    pattern="ุชูููุฑ$",
    command=("ุชูููุฑ", plugin_category),
    info={
        "header": "Fun hack animation.",
        "description": "Reply to user to show hack animation",
        "note": "This is just for fun. Not real hacking.",
        "usage": "{tr}hack",
    },
)
async def _(event):
    "Fun hack animation."
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        idd = reply_message.sender_id
        if idd == 5302507827:
            await edit_or_reply(
                event, "**โฏ๏ธุนูุฐุฑุง ูุง ุงุณุชูุทูุน ุงุฎูุชุฑุงู ููุทูุฑู ุงุนูุชุฐุฑ ุงู ุณููููู ุจุชููููุฑู**"
            )
        else:
            event = await edit_or_reply(event, "ูุชูู ุงูุงุฎุชูุฑุงู ..")
            animation_chars = [
                "โฏ๏ธุชูู ุงูุฑุจูุท ุจุณููุฑูุฑุงุช ุงููุชูููุฑ ุงูุฎูุงุตุฉ",
                "ุชูู ุชุญูุฏูุฏ ุงูุถุญููุฉ",
                "**ุชููููุฑ**... 0%\nโโโโโโโโโโโโโโโโโโโโโโโโโ ",
                "**ุชููููุฑ**... 4%\nโโโโโโโโโโโโโโโโโโโโโโโโโ ",
                "**ุชููููุฑ**... 8%\nโโโโโโโโโโโโโโโโโโโโโโโโโ ",
                "**ุชููููุฑ**... 20%\nโโโโโโโโโโโโโโโโโโโโโโโโโ ",
                "**ุชููููุฑ**... 36%\nโโโโโโโโโโโโโโโโโโโโโโโโโ ",
                "**ุชููููุฑ**... 52%\nโโโโโโโโโโโโโโโโโโโโโโโโโ ",
                "**ุชููููุฑ**... 84%\nโโโโโโโโโโโโโโโโโโโโโโโโโ ",
                "**ุชููููุฑ**... 100%\nโโโโโโโโโโโโโโโโโโโโโโโโ ",
                f"โฏ๏ธ** ุชูู ุงุฎูุชุฑุงู ุงูุถูุญูุฉ**..\n\nููู ุจุงููุฏูุน ุงูู {ALIVE_NAME} ูุนูุฏู ูุดูุฑ ูุนูููุงุชู ูุตููุฑู",
            ]
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(
            event,
            "โฏ๏ธูู ูุชูู ุงูุชุนูุฑู ุนูู ุงููุณุชูุฎุฏู",
            parse_mode=_format.parse_pre,
        )
