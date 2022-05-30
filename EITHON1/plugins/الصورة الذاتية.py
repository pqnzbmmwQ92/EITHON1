from EITHON1 import *
from EITHON1 import jmthon
from ..Config import Config
from ..sql_helper.globals import gvarstatus

EITHON1_CMD = Config.SCPIC_CMD or "ذاتية"
@jmthon.on(admin_cmd(pattern=f"{EITHON1_CMD}"))
async def dato(event):
    if not event.is_reply:
        return await event.edit("..")
    rr9r7 = await event.get_reply_message()
    pic = await rr9r7.download_media()
    SC_TEXT = gvarstatus("SC_TEXT") or "**احااا♥**"
    await bot.send_file(
        "me",
        pic,
        caption=f"""
-تـم جـلب الصـورة بنجـاح ✅
- CH: @EITHON1
- Dev: @TTTLL0
  """,
    )
    await event.edit(" 🙂❤️ ")
