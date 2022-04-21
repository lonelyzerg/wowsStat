## wwsStat
wowsStat试一个让QQ群成员通过输入简单指令就可以查询战舰世界(窝窝屎)战绩的机器人。本机器人基于[mirai](https://github.com/mamoe/mirai)和 [Ariadne](https://github.com/GraiaProject/Ariadne)开发，数据通过WG[官方的API](https://developers.wargaming.net/reference/)和wows-numbers.com 获取

wowsStat is a simple QQ group bot that allows members to query their WoWS battle statistics using some simple command. The bot is developed using [mirai](https://github.com/mamoe/mirai)和 [Ariadne](https://github.com/GraiaProject/Ariadne) and the data is accquired from WG [official API](https://developers.wargaming.net/reference/) and wows-numbers.com.

(Yuyuko 寄了之后随便搞得一个极can简fei版bot)

本bot依然在开发中(咕咕咕)，目前支持的功能非常简单，并发性能也很差，欢迎大佬们进行各种改进(或者直接写个新的)

This bot is still under development, and it only support limited commands with low parallel performance. Any improvements are welcome.

## 运行 Run:
- 安装 Python 3

  Install Python 3
- `pip install requests selenium undetected-chromedriver`
- 安装 Mirai 和 Ariadne

  Install Mirai and Ariadne
- 编辑mirai-api-http 配置文件，设置verifyKey 和adapter端口

  edit mirai-api-http config, set verifyKey and adapter's port number
- `git clone https://github.com/lonelyzerg/wowsStat.git`
- 在wowsStat目录下创建`config.txt`，复制下面的内容并替换bot的QQ号(不带引号)和你向WG申请的App ID

  Under /wowsStat, create `config.txt`, copy the following content and replace with your own account and ID.
{
  "qq": Bot QQ,
  "appid": "Your WG App ID"
}

- 启动 `mcl` / Start `mcl`
- `python bot.py`



## 命令：
- **账号绑定 Account Binding**: 

将自己的QQ账号与战舰世界账号绑定

Bind QQ account with WoWS account

  @bot wws set [server] [nickname]

  服务器可选项 亚服: asia, 欧服: eu, 美服: na, 毛服: ru.

  Server options: asia, eu, na and ru

- **总体战绩查询 Overall Statistics**: 

查询账号总体战绩

Overall statistics look up

  @bot wws [server] [nickname]
  
  如果绑定了账号，可以直接用me代替[server] [nickname]，下同

  if you have binded WoWS account, you can use "me" to replace "[server] [nickname]"
  
- **近期战绩查询 Recent Statistics**:

  查询最近N天的战绩

  Battle statistics of recent N days

  @bot wws [server] [nickname] recent N

  最多支持最近21天战绩查询，如果不填N，默认查询最近1天的战绩

  Maximum N is 21. Default N is 1 if left blank.
 
  (这一功能是爬取wowsnumbers网站数据所得，网站开起来cloudflare反爬虫，所以只能采用模拟浏览器的方式获取数据，稳定性较差，而且网站数据更新时间也不确定，并且当查询有些账号最近某天的战绩会HTTP 500加载不出来导致查询失败)
 
- **查询单船数据 Ship Statistics (Under development)**:

  查询指定战舰战绩

  Statistics of specified warship

  @bot wws [server] [nickname] ship [ship name]

  开发中...


