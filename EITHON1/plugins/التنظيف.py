# ฮ๐๐ง๐๐ข๐กโข module for purging unneeded messages(usually spam or ot).
import re
from asyncio import sleep

from telethon.errors import rpcbaseerrors
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterEmpty,
    InputMessagesFilterGeo,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
    InputMessagesFilterRoundVideo,
    InputMessagesFilterUrl,
    InputMessagesFilterVideo,
    InputMessagesFilterVoice,
)

from EITHON1 import EITHON1

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"


purgelist = {}

purgetype = {
    "ุจ": InputMessagesFilterVoice,
    "ู": InputMessagesFilterDocument,
    "ุญ": InputMessagesFilterGif,
    "ุต": InputMessagesFilterPhotos,
    "l": InputMessagesFilterGeo,
    "ุบ": InputMessagesFilterMusic,
    "r": InputMessagesFilterRoundVideo,
    "ู": InputMessagesFilterEmpty,
    "ุฑ": InputMessagesFilterUrl,
    "ู": InputMessagesFilterVideo,
    # "ู": search
}


@EITHON1.ar_cmd(
    pattern="ูุณุญ(\s*| \d+)$",
    command=("ูุณุญ", plugin_category),
    info={
        "header": "To delete replied message.",
        "description": "Deletes the message you replied to in x(count) seconds if count is not used then deletes immediately",
        "usage": ["{tr}del <time in seconds>", "{tr}del"],
        "examples": "{tr}del 2",
    },
)
async def delete_it(event):
    "To delete replied message."
    input_str = event.pattern_match.group(1).strip()
    msg_src = await event.get_reply_message()
    if msg_src:
        if input_str and input_str.isnumeric():
            await event.delete()
            await sleep(int(input_str))
            try:
                await msg_src.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#ุงูููุณูุญ \n โฏ๏ธุชูู ุญูุฐู ุงููุฑุณุงูุฉ ุจููุฌุงุญ"
                    )
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "โฏ๏ธูุง ููููููู ุงููุญุฐู ุงุญูุชุงุฌ ุตูุงุญููุงุช ุงูุงุฏููู",
                    )
        elif input_str:
            if not input_str.startswith("var"):
                await edit_or_reply(event, "โฏ๏ธุนูุฐุฑุง ุงููุฑุณุงูุฉ ุบููุฑ ููุฌููุฏุฉ")
        else:
            try:
                await msg_src.delete()
                await event.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#ุงูููุณูุญ \n โฏ๏ธุชูู ุญูุฐู ุงููุฑุณุงูุฉ ุจููุฌุงุญ"
                    )
            except rpcbaseerrors.BadRequestError:
                await edit_or_reply(event, "โฏ๏ธุนูุฐุฑุง ุงููุฑุณุงูุฉ ูุง ุงุณุชูุทูุน ุญูุฐููุง")
    elif not input_str:
        await event.delete()


@EITHON1.ar_cmd(
    pattern="ุญุฐู ุฑุณุงุฆูู$",
    command=("ุญุฐู ุฑุณุงุฆูู", plugin_category),
    info={
        "header": "To purge your latest messages.",
        "description": "Deletes x(count) amount of your latest messages.",
        "usage": "{tr}purgeme <count>",
        "examples": "{tr}purgeme 2",
    },
)
async def purgeme(event):
    "To purge your latest messages."
    message = event.text
    count = int(message[9:])
    i = 1
    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        "**โฏ๏ธุฃูุชููู ุงูุชููุธูู ** ุชูู ุญูุฐู  " + str(count) + " ูู ุงููุฑุณุงุฆูู",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "**โฏ๏ธุฃูุชููู ุงูุชููุธูู ** ุชูู ุญูุฐู  " + str(count) + " ูู ุงููุฑุณุงุฆูู",
    )
    await sleep(5)
    await smsg.delete()


# TODO: only sticker messages.
@EITHON1.ar_cmd(
    pattern="ุชูุธูู(?:\s|$)([\s\S]*)",
    command=("ุชูุธูู", plugin_category),
    info={
        "header": "ููุญุฐู ุงููุฑุณุงุฆู .",
        "description": "โข  Deletes the x(count) amount of messages from the replied message\
        \nโข  If you don't use count then deletes all messages from the replied messages\
        \nโข  If you haven't replied to any message and used count then deletes recent x messages.\
        \nโข  If you haven't replied to any message or havent mentioned any flag or count then doesnt do anything\
        \nโข  If flag is used then selects that type of messages else will select all types\
        \nโข  You can use multiple flags like -gi 10 (It will delete 10 images and 10 gifs but not 10 messages of combination images and gifs.)\
        ",
        "ุงูุงุถุงูู": {
            "ุงูุจุตูุงุช": "ูุญูุฐู ุงูุฑุณุงุฆู ุงููุตูุชูุฉ.",
            "ุงููููุงุช": "ูุญูุฐู ุงููููุงุช.",
            "ุงููุชุญุฑูู": "ูุญูุฐู ุงููุชุญูุฑูู.",
            "ุงูุตูุฑ": "ูุญูุฐู ุงููุตูุฑ",
            "ุงูุงุบุงูู": "ูุญูุฐู ุงูุงุบุงูู",
            "ุงูููุตูุงุช": "ูุญูุฐู ุงููููุตูุงุช",
            "ุงูุฑูุงุจุท": "ูุญูุฐู ุงููุฑูุงุจุท",
            "ุงููุฏูููุงุช": "ูุญูุฐู ุงููููุฏููููุงุช",
            "ูููู": " ูุญุฐู ุฌููุน ุงููุตูุต ุงูุชู ุชุญุชูู ูุฐู ุงููููู ูู ุงููุฑูุจ",
        },
        "ุงุงุณุชุฎุฏุงู": [
            "{tr}ุชูุธูู <ุงูุงุถุงูู(optional)> <count(x)> <reply> - to delete x flagged messages after reply",
            "{tr}ุชูุธูู <ุงูุงุถุงูู> <ุฑูู> - ูุญุฐู ุฑุณุงุฆู ุงูุงุถุงูู",
        ],
        "examples": [
            "{tr}ุชูุธูู 40",
            "{tr}ุชูุธูู -ุงููุชุญุฑูู 40",
            "{tr}ุชูุธูู -ูููู ุฌููุจุซูู",
        ],
    },
)
async def fastpurger(event):  # sourcery no-metrics
    "To purge messages from the replied message"
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    ptype = re.findall(r"-\w+", input_str)
    try:
        p_type = ptype[0].replace("-", "")
        input_str = input_str.replace(ptype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await event.delete()
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            if p_type is not None:
                for ty in p_type:
                    if ty in purgetype:
                        async for msg in event.client.iter_messages(
                            event.chat_id,
                            limit=int(input_str),
                            offset_id=reply.id - 1,
                            reverse=True,
                            filter=purgetype[ty],
                        ):
                            count += 1
                            msgs.append(msg)
                            if len(msgs) == 50:
                                await event.client.delete_messages(chat, msgs)
                                msgs = []
                        if msgs:
                            await event.client.delete_messages(chat, msgs)
                    elif ty == "ูููู":
                        error += f"\nโฏ๏ธุงูุงุถุงูู ุฎูุทุฃ"
                    else:
                        error += f"\n\nโฏ๏ธ`{ty}`  : ููุฐู ุฃุถุงููุฉ ุฎุงุทุฆูุฉ "
            else:
                count += 1
                async for msg in event.client.iter_messages(
                    event.chat_id,
                    limit=(int(input_str) - 1),
                    offset_id=reply.id,
                    reverse=True,
                ):
                    msgs.append(msg)
                    count += 1
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
        elif input_str and p_type is not None:
            if p_type == "ูููู":
                try:
                    cont, inputstr = input_str.split(" ")
                except ValueError:
                    cont = "error"
                    inputstr = input_str
                cont = cont.strip()
                inputstr = inputstr.strip()
                if cont.isnumeric():
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        limit=int(cont),
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=inputstr,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                else:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=input_str,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            else:
                error += f"\nโฏ๏ธ`{ty}`  : ููุฐู ุฃุถุงููุฉ ุฎุงุทุฆูุฉ "
        elif input_str:
            error += f"\nโฏ๏ธ`.ุชูุธูู {input_str}` ุงูุงููุฑ ุฎูุทุฃ ููุฑุฌู ุงููุชุงุจุฉ ุจูุดูู ุตุญูุญ"
        elif p_type is not None:
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        min_id=event.reply_to_msg_id - 1,
                        filter=purgetype[ty],
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                else:
                    error += f"\nโฏ๏ธ`{ty}`  : ููุฐู ุฃุถุงููุฉ ุฎุงุทุฆูุฉ"
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id - 1
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
    elif p_type is not None and input_str:
        if p_type != "ูููู" and input_str.isnumeric():
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id, limit=int(input_str), filter=purgetype[ty]
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                elif ty == "ุงููุชุงุจู":
                    error += f"\nโฏ๏ธูุง ุชุณุชุทููุน ุงุณุชูุฎุฏุงู ุงูุฑ ุงูุชูุธูู ุนุจุฑ ุงูุจุญุซ ูุน ุงูุงุถุงูู"
                else:
                    error += f"\nโฏ๏ธ`{ty}`  : ููุฐู ุฃุถุงููุฉ ุฎุงุทุฆูุฉ "
        elif p_type == "ูููู":
            try:
                cont, inputstr = input_str.split(" ")
            except ValueError:
                cont = "error"
                inputstr = input_str
            cont = cont.strip()
            inputstr = inputstr.strip()
            if cont.isnumeric():
                async for msg in event.client.iter_messages(
                    event.chat_id, limit=int(cont), search=inputstr
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            else:
                async for msg in event.client.iter_messages(
                    event.chat_id, search=input_str
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
        else:
            error += f"\nโฏ๏ธ`{ty}`  : ููุฐู ุฃุถุงููุฉ ุฎุงุทุฆูุฉ "
    elif p_type is not None:
        for ty in p_type:
            if ty in purgetype:
                async for msg in event.client.iter_messages(
                    event.chat_id, filter=purgetype[ty]
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            elif ty == "ูููู":
                error += f"\nโฏ๏ธูุง ุชุณุชุทููุน ุงุณุชูุฎุฏุงู ุงูุฑ ุงูุชูุธูู ุนุจุฑ ุงูุจุญุซ ูุน ุงูุงุถุงูู"
            else:
                error += f"\nโฏ๏ธ`{ty}`  : ููุฐู ุฃุถุงููุฉ ุฎุงุทุฆูุฉ "
    elif input_str.isnumeric():
        async for msg in event.client.iter_messages(chat, limit=int(input_str) + 1):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await event.client.delete_messages(chat, msgs)
    else:
        error += "\nโฏ๏ธูู ูุชูู ุชุญูุฏูุฏ ุงุถุงููุฉ ูุฑุฌู ุงุฑุณุงู  (`.ุงูุงูุฑ ุงูุชูุธูู`) ู ุฑุคูุฉ ุงูุงูุฑ ุงูุชูุธูู"
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "โฏ๏ธุงููุชูู ุงููุชูุธูู ุงูุณูุฑูุน\nโฏ๏ธุชูู ุญูุฐูใค" +  str(count)  + "ใคูู ุงููุฑุณุงุฆู"
    if error != "":
        result += f"\n\n**ุฎูุทุฃ:**{error}"
    if result == "":
        result += "โฏ๏ธูุง ุชููุฌุฏ ุฑุณูุงุฆู ููุชูุธูููุง"
    hi = await event.client.send_message(event.chat_id, result)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#ุงูุชููุธูู \n{result}",
        )
    await sleep(5)
    await hi.delete()
