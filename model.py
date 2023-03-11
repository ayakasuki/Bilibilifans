import json
import os
import warnings
import asyncio
import aiohttp
import itertools
from .user import BiliUser
from nonebot.typing import T_State
from nonebot import on_command, get_bot
from nonebot import get_driver
from nonebot.log import logger
from typing import Optional
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GROUP,
    GROUP_OWNER,
    GROUP_ADMIN,
    Message,
    GroupMessageEvent,
    MessageEvent,
)
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgStr
from configs.config import NICKNAME, Config

log = logger.bind(user="B站粉丝牌助手")
__VERSION__ = "0.3.6"

try:
    ASYNC = Config.get_config("Bilibili_fans", "ASYNC")
    LIKE_CD = Config.get_config("Bilibili_fans", "LIKE_CD")
    DANMAKU_CD = Config.get_config("Bilibili_fans", "DANMAKU_CD")
    WATCHINGLIVE = Config.get_config("Bilibili_fans", "WATCHINGLIVE")
    WEARMEDAL = Config.get_config("Bilibili_fans", "WEARMEDAL")
    SIGNINGROUP = Config.get_config("Bilibili_fans", "SIGNINGROUP", 2)
    PROXY = Config.get_config("Bilibili_fans", "PROXY")

    assert ASYNC in [0, 1], "ASYNC参数错误"
    assert LIKE_CD >= 0, "LIKE_CD参数错误"
    assert DANMAKU_CD >= 0, "DANMAKU_CD参数错误"
    assert WATCHINGLIVE >= 0, "WATCHINGLIVE参数错误"
    assert WEARMEDAL in [0, 1], "WEARMEDAL参数错误"
    config = {
        "ASYNC": ASYNC,
        "LIKE_CD": LIKE_CD,
        "DANMAKU_CD": DANMAKU_CD,
        "WATCHINGLIVE": WATCHINGLIVE,
        "WEARMEDAL": WEARMEDAL,
        "SIGNINGROUP": SIGNINGROUP,
        "PROXY": PROXY,
    }

except Exception as e:
    log.error(f"读取配置文件失败,请检查配置文件格式是否正确: {e}")
    exit(1)

# should_stop = False
@log.catch
async def HGDBILIBILIFANS():
    # global should_stop
    messageList = []
    session = aiohttp.ClientSession()
    try:
        log.warning("当前版本为: " + __VERSION__)
        resp = await (
            await session.get("http://version.fansmedalhelper.1961584514352337.cn-hangzhou.fc.devsapp.net/")
        ).json()
        if resp['version'] != __VERSION__:
            log.warning("新版本为: " + resp['version'] + ",请更新")
            log.warning("更新内容: " + resp['changelog'])
            messageList.append(f"当前版本: {__VERSION__} ,最新版本: {resp['version']}")
            messageList.append(f"更新内容: {resp['changelog']} ")
        if resp['notice']:
            log.warning("公告: " + resp['notice'])
            messageList.append(f"公告: {resp['notice']}")
    except Exception:
        messageList.append("检查版本失败")
        log.warning("检查版本失败")
    initTasks = []
    startTasks = []
    catchMsg = []

    access_key_val = Config.get_config("Bilibili_fans", "ACCESS_KEY")
    white_uid_val = Config.get_config("Bilibili_fans", "WHITE_UID")
    banned_uid_val = Config.get_config("Bilibili_fans", "BANNED_UID")
    if access_key_val:
        biliUser = BiliUser(
            access_key_val, white_uid_val, banned_uid_val, config
        )
        initTasks.append(biliUser.init())
        startTasks.append(biliUser.start())
        catchMsg.append(biliUser.sendmsg())
    try:
        await asyncio.gather(*initTasks)
        await asyncio.gather(*startTasks)
    except Exception as e:
        log.exception(e)
        # messageList = messageList + list(itertools.chain.from_iterable(await asyncio.gather(*catchMsg)))
        messageList.append(f"任务执行失败: {e}")
    # global should_stop
    # if should_stop == True:
        # pass
    finally:
        messageList = messageList + list(itertools.chain.from_iterable(await asyncio.gather(*catchMsg)))
    [log.info(message) for message in messageList]
    await bot.send_msg(user_id=event.user_id, message=f'【B站粉丝牌助手推送】 "  \n".join(messageList)')
    
# if __name__ == '__main__':
#     from apscheduler.schedulers.blocking import BlockingScheduler
#     from apscheduler.triggers.cron import CronTrigger

#     cron = users.get('CRON', None)
#     if cron:
#         log.info('使用内置定时器,开启定时任务,等待时间到达后执行')
#         schedulers = BlockingScheduler()
#         schedulers.add_job(run, CronTrigger.from_crontab(cron), misfire_grace_time=3600)
#         schedulers.start()
#     else:
#         log.info('外部调用,开启任务')
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         loop.run_until_complete(main())
#         log.info("任务结束")
