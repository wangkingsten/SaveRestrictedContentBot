#Github.com/Vasusen-code

import os
from .. import bot as Drone
from telethon import events, Button

from ethon.mystarts import start_srb
    
S = '/' + 's' + 't' + 'a' + 'r' + 't'

@Drone.on(events.callbackquery.CallbackQuery(data="set"))
async def sett(event):    
    Drone = event.client                    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("用图片回复本条消息")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("没有检测到图片")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("没有检测到图片")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, '尝试中')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("已保存略所图")
        
@Drone.on(events.callbackquery.CallbackQuery(data="rem"))
async def remt(event):  
    Drone = event.client            
    await event.edit('尝试中')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('已经移除')
    except Exception:
        await event.edit("没有保存相关资源")                        
  
@Drone.on(events.NewMessage(incoming=True, pattern=f"{S}"))
async def start(event):
    text = "把链接或者内容转发到这里, 如果是私人群组的消息, 请先发送入群链接"
    await start_srb(event, text)
    
