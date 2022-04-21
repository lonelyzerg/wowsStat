from graia.ariadne.app import Ariadne
from graia.ariadne.model import MiraiSession
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from multiprocessing import Process
import wowsnumbers_service as ws
import json


if __name__ == '__main__':
    data = {}
    with open('config.txt', 'r') as f:
        data = json.load(f)
    p = Process(target=ws.init)
    p.start()
    app = Ariadne(
        MiraiSession(
            # 以下3行请按照你的 MAH 配置来填写
            host="http://localhost:9990",  # 同 MAH 的 port
            verify_key="wowsstat",  # 同 MAH 配置的 verifyKey
            account=data['qq'],  # 机器人 QQ 账号
        ),
    )

    saya = app.create(Saya)
    saya.mount('appid', data['appid'])
    saya.install_behaviours(
        app.create(BroadcastBehaviour),
    )

    with saya.module_context():
        saya.require("modules.wows")



    app.launch_blocking()
