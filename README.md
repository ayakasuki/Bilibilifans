<p align="center">
  <img src="https://s1.ax1x.com/2022/05/24/XPx1tx.png" width="200" height="200" alt="">
</p>
<div align="center">
<h1> 真寻版 —— B 站粉丝牌助手
</h1>

<p>当前版本：1.0</p>

</div>

**TODO**

* [x] B站粉丝牌任务          --首次执行会直接打开，重复运行会显示BOT真正看！

* [x] 定时执行助手            --原cron表达式自动每天观看，但在考虑适配zhenxun的apscheduler定时任务插件
- [ ] 关闭粉丝牌任务 --手动结束执行函数

- [ ] 多用户适配                --目前仅超级用户用于个人access_key签到，理论支持多用户异步执行，欢迎pr

- [ ] 填入不同用户access_key   --目前access_key尚未支持绑定不同bot的user_id,有机会实现，欢迎pr
  
  

**B站粉丝牌功能实现**

- [x] 每日直播区签到

- [x] 每日点赞 1 次直播间 （100 亲密度）

- [x] 每日弹幕打卡（100 亲密度）

- [x] 每日观看 65 分钟 （ 每 5 分钟 100 共 1300 亲密度）

- [x] 每日应援团签到 (如果有的话) （10 亲密度）

<small>ps: 新版 B 站粉丝牌的亲密度每一个牌子都将单独计算  </small>

---

### 使用说明

* Access_key (必填)  B站账户鉴权 [鉴权获取方式](https://github.com/XiaoMiku01/fansMedalHelper/releases/tag/logintool)

* 在bot根目录下env.dev文件添加以下配置
  ```APSCHEDULER_CONFIG={"apscheduler.timezone": "Asia/Shanghai"}```（国外自查）
  以纠正因人而异的BOT时区。

* 其他配置字段，移步zhunxun_bot/configs/config.yaml 注释观看

* 本真寻BOT适配插件为新手重新适配，代码如shit，敬请原谅。同时欢迎pr。
  
  

原B站粉丝牌助手详细文档在这里 👉 [文档](https://xiaomiku01.github.io/fansMedalHelperVersion/)  （配置文件已移入bot/configs/config.yaml）

打不开的用这个镜像文档 👉 [镜像](https://doc.loveava.top/)  

**请细心阅读**

---

### 问题反馈

- 提 issue
  **提之前请明确问题主题和运行日志**

---

### 友情链接

- 感谢 原B站粉丝牌助手 [XiaoMiku01/fansMedalHelper](https://github.com/XiaoMiku01/fansMedalHelper)
- 此脚本的 Go 语言实现版本 [ThreeCatsLoveFish/MedalHelper](https://github.com/ThreeCatsLoveFish/MedalHelper)
- AW 的 B 站挂机助手 [andywang425/BLTH](https://github.com/andywang425/BLTH)

**衷心感谢 微软New Bing的代码报错解惑，助力测试。**

---
