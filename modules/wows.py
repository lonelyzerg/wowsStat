from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.ariadne.message.element import At, Image, Plain, Member
from graia.saya import Saya
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.base import MentionMe
from modules.db import bind, read_accid
from modules.query import init, get_stat, get_accid, get_recent_stat
from modules.parse import parser
import datetime
import traceback
import socket
import pickle


appid = Saya.current().access('appid')
init(appid)
channel = Channel.current()
parser = parser()
ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sr.bind(('127.0.0.1', 9874))
sr.settimeout(10)


@channel.use(ListenerSchema(listening_events=[GroupMessage], decorators=[MentionMe()]))
async def query(app: Ariadne, group: Group, member: Member, message: MessageChain):
    if group.id == 210801034 or group.id == 107284013:
        if message[1] == At(app.account) and len(message) > 2:
            command = str(message[2:]).strip().lower()
            if len(command) > 5:
                result = parse_command(command, member.id)
                if result == -1:
                    result = '查询出错，请检查指令'
                await app.sendMessage(
                    group,
                    MessageChain.create(str(result)),
                )


try:
    raise Exception("just for fun")
except:
    print('wtf')




def parse_command(string, qq):
    # wws 支持的指令
    # set
    #
    command = string.split()
    if command[0] == 'wws':
        try:
            args = vars(parser.parse_args(command[1:]))
            if args['func'] == 'set':
                result = bind(qq=qq, server=args['server'], nickname=args['nickname'])
                if result == 0:
                    return '绑定成功'
                else:
                    return '绑定失败，请检查服务器与昵称'

            server = ''
            accid = -1
            if args['func'] == 'me':
                result = read_accid(qq=qq)
                if result == -1:
                    return '请先绑定账号'
                server = result['server']
                accid = result['accid']

            if args['func'] == 'stat':
                server = args['server']
                nickname = args['nickname']
                accid = get_accid(server=server, nickname=nickname)
                if accid == -1:
                    return '玩家不存在'

            if not args['mode']:
                stat = get_stat(server=server, accid=accid,
                                extra='statistics.pvp_solo,statistics.pvp_div2,statistics.pvp_div3')
                if stat is None:
                    return '未找到数据'

                return parse_overall(stat)

            elif len(args['mode']) > 2:
                return '请检查命令格式，帮助请输入wws -h'

            elif args['mode'][0] == 'record' and len(args['mode']) == 1:
                # get record
                pass

            elif args['mode'][0] == 'recent':
                day = 0
                if len(args['mode']) == 1:
                    day = 1
                else:
                    day = int(args['mode'][1])
                    if day > 21:
                        return '最多查询最近21天的战绩'
                now = datetime.datetime.today()
                date = now - datetime.timedelta(days=day)
                date_str = date.strftime('%Y-%m-%d')

                string = bytes(' '.join([server, str(accid), date_str]), encoding="UTF-8")
                ss.sendto(string, ('127.0.0.1', 9875))
                recent = pickle.loads(sr.recv(102400))
                print('wowsnumbers query complete.')
                if recent['status']:
                    data = recent['data']
                    message = '最近' + str(day) + '天战绩\n'
                    for ship in data:
                        ship_msg = ''
                        ship_msg += ship['等级'] + ' ' + ship['战舰'] + ':\n'
                        ship_msg += '场次: ' + ship['场次'] + ' '
                        ship_msg += '胜率: ' + ship['胜率'][0] + ' '
                        ship_msg += 'PR: ' + ship['PR'][0] + ' '
                        ship_msg += '场均伤害: ' + ship['场均伤害'][0] + ' '
                        ship_msg += '场均击沉: ' + ship['场均击沉'][0] + ' '
                        ship_msg += '场均飞机击落: ' + ship['场均飞机击落'][0] + '\n\n'
                        message += ship_msg
                    return message
                else:
                    return '查询失败'




                return '施工中...'

        except SystemExit:
            return '请检查命令格式，帮助请输入wws -h'
        except Exception as e:
            print(traceback.format_exc())
            return '请检查命令格式，帮助请输入wws -h'
    else:
        return -1


def to_date(timestamp):
    time = datetime.datetime.fromtimestamp(timestamp)
    return '{}年{}月{}日 {}:{}'.format(time.year, time.month, time.day, time.hour, time.minute)


def parse_overall(stat):
    overall = {}
    nickname = stat['nickname']
    if stat['hidden_profile']:
        return -1
    last_update = to_date(stat['updated_at'])
    last_battle = to_date(stat['last_battle_time'])
    overall['游戏ID'] = nickname
    overall['最近更新'] = last_update
    overall['上场比赛'] = last_battle
    pvp = parse_pvp(stat['statistics']['pvp'])
    pvp_solo = parse_pvp(stat['statistics']['pvp_solo'])
    pvp_div2 = parse_pvp(stat['statistics']['pvp_div2'])
    pvp_div3 = parse_pvp(stat['statistics']['pvp_div3'])

    message = ''
    for key, val in overall.items():
        message += key + ': ' + str(val) + '\n'

    message += '总体数据:\n'
    for key, val in pvp.items():
        message += key + ': ' + str(val) + '\n'

    message += '独轮车:\n'
    for key, val in pvp_solo.items():
        message += key + ': ' + str(val) + '\n'

    message += '自行车:\n'
    for key, val in pvp_div2.items():
        message += key + ': ' + str(val) + '\n'

    message += '三轮车:\n'
    for key, val in pvp_div3.items():
        message += key + ': ' + str(val) + '\n'

    return message


def parse_pvp(data):
    res = {}
    battles = data['battles']
    wins = data['wins']
    wr = str(round(wins * 100 / battles, 2)) + '%'
    avg_plane = round(data['planes_killed'] / battles, 2)
    avg_damage = round(data['damage_dealt'] / battles)
    avg_frag = round(data['frags'] / battles, 2)
    avg_xp = round(data['xp'] / battles
                   )

    res['总场次'] = battles
    res['胜场数'] = wins
    res['胜率'] = wr
    res['场均伤害'] = avg_damage
    res['场均击沉'] = avg_frag
    res['场均飞机击落'] = avg_plane
    res['场均经验'] = avg_xp
    return res

