from telethon import events
import random, re
from EITHON1.utils import admin_cmd
import asyncio 

@borg.on(admin_cmd("تنصيب السورس"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("⌁︙**اهـلا بك فـي تنصيب السورس** \n⌁︙رابط التنصيب  -[اضغط هنا](⌁︙ يرجى متابعة قناة ايــثــون الرسمي لتنصيب السورس - @EITHON1)\n⌁︙قناة السورس - @EITHON1")
