import asyncio
import glob
import os
import sys
from datetime import timedelta
from pathlib import Path
import requests
from telethon import Button, functions, types, utils
from telethon.tl.functions.channels import JoinChannelRequest

from EITHON1 import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from ..Config import Config
from ..core.logger import logging
from ..core.session import EITHON1
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup

LOGS = logging.getLogger("EITHON1")
cmdhr = Config.COMMAND_HAND_LER

bot = EITHON1

async def setup_bot():
    """
    To set up bot for EITHON1
    """
    try:
        await EITHON1.connect()
        config = await EITHON1(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == EITHON1.session.server_address:
                if EITHON1.session.dc_id != option.id:
                    LOGS.warning(
                        f"⌯︙معرف ثابت في الجلسة من {EITHON1.session.dc_id}"
                        f"⌯︙لـ  {option.id}"
                    )
                EITHON1.session.set_dc(option.id, option.ip_address, option.port)
                EITHON1.session.save()
                break
        bot_details = await EITHON1.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await EITHON1.start(bot_token=Config.TG_BOT_USERNAME)
        EITHON1.me = await EITHON1.get_me()
        EITHON1.uid = EITHON1.tgbot.uid = utils.get_peer_id(EITHON1.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(EITHON1.me)
    except Exception as e:
        LOGS.error(f"كـود تيرمكس - {str(e)}")
        sys.exit()


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            Config.CATUBLOGO = await EITHON1.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/4ed13bf6216c070e3cc48.jpg",
                caption="⌯︙**بــوت ايــثــون يـعـمـل بـنـجـاح**  ✅ \n⌯︙**قـنـاة الـسـورس**  :  @EITHON1",
                buttons=[(Button.url("كروب ايــثــون", "https://t.me/eithonsupport"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await EITHON1.check_testcases()
            message = await EITHON1.get_messages(msg_details[0], ids=msg_details[1])
            text = (
                message.text
                + "\n\n**⌯︙اهلا وسهلا لقد قمت باعاده تشغيل بـوت ايــثــون تمت بنجاح**"
            )
            await EITHON1.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await EITHON1.send_message(
                    msg_details[0],
                    f"{cmdhr}بنك",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def mybot():
    EITHON1_USER = bot.me.first_name
    The_razan = bot.uid
    rz_ment = f"[{EITHON1_USER}](tg://user?id={The_razan})"
    f"ـ {rz_ment}"
    f"⪼ هذا هو بوت خاص بـ {rz_ment} يمكنك التواصل معه هنا"
    starkbot = await EITHON1.tgbot.get_me()
    perf = "[ ايــثــون ]"
    bot_name = starkbot.first_name
    botname = f"@{starkbot.username}"
    if bot_name.endswith("Assistant"):
        print("تم تشغيل البوت")
    else:
        try:
            await bot.send_message("@BotFather", "/setinline")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", perf)
            await asyncio.sleep(2)
        except Exception as e:
            print(e)

async def ipchange():
    """
    Just to check if ip change or not
    """
    newip = (requests.get("https://httpbin.org/ip").json())["origin"]
    if gvarstatus("ipaddress") is None:
        addgvar("ipaddress", newip)
        return None
    oldip = gvarstatus("ipaddress")
    if oldip != newip:
        delgvar("ipaddress")
        LOGS.info("Ip Change detected")
        try:
            await EITHON1.disconnect()
        except (ConnectionError, CancelledError):
            pass
        return "ip change"


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await EITHON1.tgbot.get_me()
    try:
        await EITHON1(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await EITHON1(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def load_plugins(folder):
    """
    To load plugins from the mentioned folder
    """
    path = f"EITHON1/{folder}/*.py"
    files = glob.glob(path)
    files.sort()
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            try:
                if shortname.replace(".py", "") not in Config.NO_LOAD:
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                shortname.replace(".py", ""),
                                plugin_path=f"EITHON1/{folder}",
                            )
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"EITHON1/{folder}/{shortname}.py"))
            except Exception as e:
                os.remove(Path(f"EITHON1/{folder}/{shortname}.py"))
                LOGS.info(
                    f"⌯︙غير قادر على التحميل {shortname} يوجد هناك خطا بسبب : {e}"
                )


async def saves():
    try:
        os.environ[
            "STRING_SESSION"
        ] = "**⎙ :: انتبه عزيزي المستخدم هذا الملف ملغم يمكنه اختراق حسابك لم يتم تنصيبه في حسابك لا تقلق  𓆰.**"
    except Exception as e:
        print(str(e))
    try:
        await EITHON1(JoinChannelRequest("@EITHON1"))
    except BaseException:
        pass
    try:
        await EITHON1(JoinChannelRequest("@EITHON1"))
    except BaseException:
        pass
    try:
        await EITHON1(JoinChannelRequest("@EITHON1"))
    except BaseException:
        pass


async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    flag = False
    if BOTLOG:
        try:
            entity = await EITHON1.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "⌯︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "⌯︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."
                    )
        except ValueError:
            LOGS.error("⌯︙تـأكد من فـار المجـموعة  PRIVATE_GROUP_BOT_API_ID.")
        except TypeError:
            LOGS.error(
                "⌯︙لا يمكـن العثور على فار المجموعه PRIVATE_GROUP_BOT_API_ID. تأكد من صحتها."
            )
        except Exception as e:
            LOGS.error(
                "⌯︙حدث استثناء عند محاولة التحقق من PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = "- عزيزي المستخدم هذه هي مجموعه الاشعارات يرجى عدم حذفها  - @EITHON1"
        photobt = await EITHON1.upload_file(file="EIT/razan/resources/start/EITHON1.2.jpg")
        _, groupid = await create_supergroup(
            "مجموعة اشعارات ايــثــون ", EITHON1, Config.TG_BOT_USERNAME, descript, photobt
        )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print("⌯︙تم إنشاء مجموعة المسـاعدة بنجاح وإضافتها إلى المتغيرات.")
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await EITHON1.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "⌯︙الأذونات مفقودة لإرسال رسائل لـ PM_LOGGER_GROUP_ID المحدد."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "⌯︙الأذونات مفقودة للمستخدمين الإضافيين لـ PM_LOGGER_GROUP_ID المحدد."
                    )
        except ValueError:
            LOGS.error("⌯︙لا يمكن العثور على فار  PM_LOGGER_GROUP_ID. تأكد من صحتها.")
        except TypeError:
            LOGS.error("⌯︙PM_LOGGER_GROUP_ID غير مدعوم. تأكد من صحتها.")
        except Exception as e:
            LOGS.error(
                "⌯︙حدث استثناء عند محاولة التحقق من PM_LOGGER_GROUP_ID.\n" + str(e)
            )
    else:
        descript = "⌯︙ وظيفه الكروب يحفظ رسائل الخاص اذا ما تريد الامر احذف الكروب نهائي \n  - @EITHON1"
        photobt = await EITHON1.upload_file(file="EIT/razan/resources/start/EITHON1.jpg")
        _, groupid = await create_supergroup(
            "مجموعة التخزين", EITHON1, Config.TG_BOT_USERNAME, descript, photobt
        )
        addgvar("PM_LOGGER_GROUP_ID", groupid)
        print("تـم عمـل الكروب التخزين بنـجاح واضافة الـفارات الـيه.")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "EITHON1"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)
