#========================#
#       ฮ๐๐ง๐๐ข๐กโข  - RR7PP  #  
# =======================#

from asyncio import sleep

from telethon import events

from EITHON1 import EITHON1
from ..Config import Config


from ..core.managers import edit_or_reply
from ..sql_helper import pmpermit_sql as pmpermit_sql
from ..sql_helper.welcomesql import (
    addwelcome_setting,
    getcurrent_welcome_settings,
    rmwelcome_setting,
)
from . import BOTLOG_CHATID

plugin_category = "utils"

welpriv = Config.PRV_ET or "ุฑุญุจ"
delwelpriv = Config.DELPRV_ET or "ุญุฐู ุฑุญุจ"

@EITHON1.on(events.ChatAction)
async def _(event):
    cws = getcurrent_welcome_settings(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = chat.title or "ููุฐู ุงููุฏุฑุฏุดูู"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws.reply:
                current_saved_welcome_message = cws.reply
        if not pmpermit_sql.is_approved(userid):
            pmpermit_sql.approve(userid, "Due to private welcome")
        await sleep(1)
        current_message = await event.client.send_message(
            userid,
            current_saved_welcome_message.format(
                mention=mention,
                title=title,
                count=count,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            ),
            file=file_media,
            parse_mode="html",
        )


@EITHON1.on(admin_cmd(pattern=f"{welpriv}(?:\s|$)([\s\S]*)"))
async def save_welcome(event):
    "To set private welcome message."
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**โฏ๏ธุงูุชูุฑุญูุจ ุงููุฎุงุต **\
                \n**โฏ๏ธุงูุฏู ุงูุฏุฑุฏุดูุฉ  :** {event.chat_id}\
                \n**โฏ๏ธุชู ุญููุธ ุงูุฑุณุงููุฉ ุงูุงุชููุฉ ููุชุฑุญููุจ ุจูุฌูุงุญ \n** {event.chat.title}, ูุง ุชููู ุจุญูุฐู ููุฐู ุงูุฑุณุงููุฉ !",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "**โฏ๏ธุญููุธ ุงููุณุงุฆูุท ูุฌูุฒุก ููู ุงูุชุฑุญููุจ ูุชุทููุจ ุชุนูููู ููุงุฑ BOTLOG_CHATID !**",
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**โฏ๏ธุชูู ุญููุธ ุงููุชุฑุญูุจ ุงููุฎุงุต ููู ููุฐู ุงููุฏุฑุฏุดูุฉ ุจููุฌุงุญ**"
    if addwelcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("saved"))
    rmwelcome_setting(event.chat_id)
    if addwelcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("updated"))
    await edit_or_reply("**โฏ๏ธุญูุฏุซ ุฎุทูุฃ ุฃุซููุงุก ุถุจูุท ุฑุณุงููุฉ ุงูุชุฑุญููุจ ูู ููุฐู ุงููุฏุฑุฏุดูุฉ ๏ธ**")


@EITHON1.on(admin_cmd(pattern=f"{delwelpriv}(?:\s|$)([\s\S]*)"))
async def del_welcome(event):
    "To turn off private welcome message"
    if rmwelcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**โฏ๏ธุชู ุญูุฐู ุงูุชุฑุญููุจ ุงููุฎุงุต ูููุฐู ุงูุฏุฑุฏุดูุฉ ุจูุฌูุงุญ **")
    else:
        await edit_or_reply(event, "**โฏ๏ธูููุณ ููุฏู ุงู ุฑุณูุงูุฉ ุชูุฑุญูุจ ุฎูุงุต ูููุง**")


@EITHON1.ar_cmd(
    pattern="ูุณุชุฉ ุงูุชุฑุญูุจ ุงูุฎุงุต$",
    command=("ูุณุชุฉ ุงูุชุฑุญูุจ ุฎุงุต", plugin_category),
    info={
        "header": "To check current private welcome message in group.",
        "usage": "{tr}listpwel",
    },
)
async def show_welcome(event):
    "To show current private welcome message in group"
    cws = getcurrent_welcome_settings(event.chat_id)
    if not cws:
        await edit_or_reply(event, "**โฏ๏ธููู ูุชูู ุญููุธ ุงู ุชุฑุญููุจ ุฎูุงุต ูููุง **")
        return
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "**โฏ๏ธุณุฃูููู ุจุงูุชุฑุญููุจ ุจุงูุฃุนุถูุงุก ุงูุฌูุฏุฏ ุจููุฐู ุงูุฑุณุงููุฉ :**"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "**โฏ๏ธุณุฃูููู ุจุงูุชุฑุญููุจ ุจุงูุฃุนุถูุงุก ุงูุฌูุฏุฏ ุจููุฐู ุงูุฑุณุงููุฉ :**"
        )
        await event.reply(cws.reply)
