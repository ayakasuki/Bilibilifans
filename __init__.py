import os
import time
import traceback
import psutil
import signal
import sys
from .model import HGDBILIBILIFANS
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
#from nonebot.plugin import PluginMetadata
# 定义插件元数据

#__plugin_name__ = 'B站粉丝牌助手'
__zx_plugin_name__ = 'B站粉丝牌助手'
__plugin_usage__ = """
usage：
    B站粉丝牌：立即运行-----定时任务出错时备用！\n
    指令：
    \nB站粉丝牌任务
    """.strip()                   # __plugin_usage__
__plugin_des__ = "B站粉丝牌助手-定时执行粉丝牌插件任务、单次立即执行粉丝牌任务，帮忙观看直播。"       # __plugin_des__
__plugin_cmd__ = ["B站粉丝牌任务"]
__plugin_help_name__ = "B站粉丝牌助手帮助"
__plugin_help_info__ = f'''\
    🍺欢迎使用B站粉丝牌助手！\
    \nB站粉丝牌任务
'''.strip()
__plugin_settings__ = {
    "level": 5,             # 群权限等级，请不要设置为1或999，若无特殊情况请设置为5
    "default_status": True,     # 进群时的默认开关状态
    "limit_superuser": False,   # 开关插件的限制是否限制超级用户
    "cmd": ["B站粉丝牌任务"],   # 命令别名，主要用于帮助和开关
    "cost_gold": 0,             # 该功能需要花费的金币
}
__plugin_type__ = ('工具', 1)
__plugin_version__ = 1.0
__plugin_author__ = "今天要来点桃子吗？"

#metadata = PluginMetadata(name=__plugin_name__, usage=__plugin_usage__, description=__plugin_description__, help=__plugin_help_name__ + __plugin_help_info__)
#plugin_config = Config.parse_obj(get_driver().config.dict())

#添加元插件初始化配置
Config.add_plugin_config(
    "Bilibili_fans",
    "access_key",
    "",
    name="异步执行还是同步执行",
    help_="注意冒号后的空格 否则会读取失败 英文冒号",
    default_value = ""
)
Config.add_plugin_config(
    "Bilibili_fans",
    "white_uid",
    0,
    name="白名单用户ID",
    help_="白名单用户ID, 可以是多个用户ID, 以逗号分隔,填写后只会打卡这些用户,黑名单失效，不用就填0",
    default_value=0
)
Config.add_plugin_config(
    "Bilibili_fans",
    "banned_uid",
    0,
    name="黑名单用户ID",
    help_="黑名单UID 同上,填了后将不会打卡，点赞，分享 用英文逗号分隔 不填则不限制,两个都填0则不限制,打卡所有直播间",
    default_value=0
)
Config.add_plugin_config(
    "Bilibili_fans",
    "PROXY",
    "",
    name="推送代理地址",
    help_=" 推送代理地址,如：http://1.2.3.4:5678 支持 http/socks4/socks5 不支持 https 不用代理的不用填",
    default_value = ""
)
Config.add_plugin_config(
    "Bilibili_fans",
    "ASYNC",
    0,
    name="异步执行还是同步执行",
    help_="异步执行,默认异步执行,设置为0则同步执行,开启异步后,将不支持设置点赞CD时间量。 说明：本项目中的异步执行指的是：同时点赞或者分享所有直播间，速度非常快，但缺点就是可能会被B站吞掉亲密度，所以建议粉丝牌较少的用户开启异步执行,粉丝牌数大于30的用户建议使用同步，会更加稳定。缺点就是速度比较慢，但是可以设置点赞和分享的CD时间，避免被B站吞掉亲密度多用户之间依然是异步，不受配置影响",
    default_value=0
)
Config.add_plugin_config(
    "Bilibili_fans",
    "LIKE_CD",
    2,
    name="点赞间隔时间",
    help_="点赞间隔时间,单位秒,默认2秒,仅为同步时生效,设置为0则不点赞",
    default_value=2
)
Config.add_plugin_config(
    "Bilibili_fans",
    "DANMAKU_CD",
    6,
    name="弹幕间隔时间",
    help_="弹幕间隔时间,单位秒,默认6秒,设置为0则不发弹幕打卡,只能同步打卡",
    default_value=6
)
Config.add_plugin_config(
    "Bilibili_fans",
    "WATCHINGLIVE",
    65,
    name="每日观看直播时长",
    help_="每日观看直播时长，单位 min ，设置为0则关闭, 默认 65 分钟",
    default_value=65
)
Config.add_plugin_config(
    "Bilibili_fans",
    "WEARMEDAL",
    1,
    name="弹幕打卡时自动带上当前房间的粉丝牌开关",
    help_="是否弹幕打卡时自动带上当前房间的粉丝牌，避免房间有粉丝牌等级禁言，默认关闭，设置为1则开启",
    default_value=0
)
Config.add_plugin_config(
    "Bilibili_fans",
    "SIGNINGROUP",
    2,
    name="弹幕打卡时自动带上当前房间的粉丝牌开关",
    help_="应援团签到CD时间,单位秒,默认2秒,设置为0则不签到",
    default_value=2
)


# 初始赋值，定义命令处理函数
is_running = False
# should_stop = False

HGD = on_command('B站粉丝牌任务', block=True, priority=5)
@HGD.handle()
async def run_main(bot: Bot, event: MessageEvent, state: T_State):
    global is_running
    if is_running:
        await HGD.finish(f'{NICKNAME}还在看哦！')
    else:
        global should_stop
        await bot.send_msg(event, message=f'{NICKNAME}帮忙看直播与提升粉丝牌好感度中！')
        is_running = True
        result = await model.HGDBILIBILIFANS()
        is_running = False
        # should_stop = False
        await HGD.finish(result)
        

# stop_bilibili_fans = on_command('终止B站粉丝牌', block=True, priority=5)
# @stop_bilibili_fans.handle()

# async def stop_bilibili_fans(bot: Bot, event: Event, state: T_State):
#     global should_stop
#     should_stop = True
#     await bot.send(event, message=f"{NICKNAME}解放啦！")
#     should_stop = False
#     return
#     try:
#         if should_stop == False:
#             msg = "B站粉丝牌未运行！"
#             await bot.send_msg(event, message=msg)
#             return
#     except Exception as e:
#         await bot.send_msg(event, message=f"停止 B站粉丝牌失败，错误信息：{str(e)}")
        
        
async def on_error_handler(bot: Bot, event: MessageEvent, exception: Exception):
    # 获取 traceback 信息
    traceback_msg = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
    # 发送错误信息到指定群组
    await bot.send_msg(event, message=f"发生错误：\n{traceback_msg}")

bilibili_fanshelp = on_command('B站粉丝牌帮助', block=True, priority=5)
@bilibili_fanshelp.handle()
async def _(bot: Bot, event: Event):
    await bot.send_msg(event, message= "欢迎使用B站粉丝牌助手！\nB站粉丝牌任务")

