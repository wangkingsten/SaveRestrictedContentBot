#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import time, os, asyncio

from .. import bot as Drone
from .. import userbot, Bot, AUTH
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_bulk_msg
from main.plugins.helpers import get_link, screenshot

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

from ethon.pyfunc import video_metadata
from ethon.telefunc import force_sub

ft = f"To use this bot you've to join @{fs}."

batch = []

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/cancel'))
async def cancel(event):
    if not event.sender_id in batch:
        return await event.reply("目前没有批量下载")
    batch.clear()
    await event.reply("已完成")
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/batch'))
async def _batch(event):
    if not event.is_private:
        return
    s, r = await force_sub(event.client, fs, event.sender_id, ft) 
    if s == True:
        await event.reply(r)
        return       
    if event.sender_id in batch:
        return await event.reply("目前批量下载未完成，稍后再试")
    async with Drone.conversation(event.chat_id) as conv: 
        if s != True:
            await conv.send_message("把想要下载的链接回复给本条消息", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("没有发现链接")
                    return conv.cancel()
            except Exception as e:
                print(e)
                await conv.send_message("等不到回复，已经取消")
                return conv.cancel()
            await conv.send_message("把想要下载的文件范围回复给本条消息", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                await conv.send_message("等不到回复，已经取消")
                return conv.cancel()
            try:
                value = int(_range.text)
                if value > 100:
                    await conv.send_message("批量下载一次最多100个")
                    return conv.cancel()
            except ValueError:
                await conv.send_message("范围必须是整数")
                return conv.cancel()
            batch.append(event.sender_id)
            await run_batch(userbot, Bot, event.sender_id, _link, value) 
            conv.cancel()
            batch.clear()

async def run_batch(userbot, client, sender, link, _range):
    for i in range(_range):
        timer = 60
        if i < 25:
            timer = 5
        if i < 50 and i > 25:
            timer = 10
        if i < 100 and i > 50:
            timer = 15
        if not 't.me/c/' in link:
            if i < 25:
                timer = 2
            else:
                timer = 3
        try: 
            if not sender in batch:
                await client.send_message(sender, "批量下载已经完成")
                break
        except Exception as e:
            print(e)
            await client.send_message(sender, "批量下载已经完成")
            break
        try:
            await get_bulk_msg(userbot, client, sender, link, i) 
        except FloodWait as fw:
            if int(fw.x) > 299:
                await client.send_message(sender, "请求太多，批量下载已经取消")
                break
            await asyncio.sleep(fw.x + 5)
            await get_bulk_msg(userbot, client, sender, link, i)
        protection = await client.send_message(sender, f"暂停 `{timer}` 秒避免被断开连接")
        await asyncio.sleep(timer)
        await protection.delete()
            
