import re

from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

repeater_group = ["all"]
shortest = 2
shortest_times = 2
blacklist = []

m = on_message(priority=10, block=False)

last_message = {}
message_times = {}


# 消息预处理
def message_preprocess(message: str):
    raw_message = message
    contained_images = {}
    images = re.findall(r'\[CQ:image.*?]', message)
    for i in images:
        contained_images.update({i: [re.findall(
            r'url=(.*?)[,\]]', i)[0][0], re.findall(r'file=(.*?)[,\]]', i)[0][0]]})
    for i in contained_images:
        message = message.replace(i, f'[{contained_images[i][1]}]')
    return message, raw_message


@m.handle()
async def repeater(bot: Bot, event: GroupMessageEvent):
    # 检查是否在黑名单中
    if event.raw_message in blacklist:

        return
    gid = str(event.group_id)
    if gid in repeater_group or "all" in repeater_group:
        global last_message, message_times
        message, raw_message = message_preprocess(str(event.message))

        if last_message.get(gid) != message:
            message_times[gid] = 1
        else:
            message_times[gid] += 1
        if message_times.get(gid) == shortest_times:
            await bot.send_group_msg(group_id=event.group_id, message=raw_message, auto_escape=False)
        last_message[gid] = message
