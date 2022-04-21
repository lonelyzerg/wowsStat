import sqlite3
from .query import get_accid


def connect_db():
    con = sqlite3.connect('./database/wows.db')
    cur = con.cursor()
    return con, cur


def bind(qq, server, nickname):
    con, cur = connect_db()
    if len(nickname) > 50:
        return -1
    accid = get_accid(server, nickname)
    if accid == -1:
        print('no player found')
        return -1
    command = '''INSERT OR REPLACE INTO player VALUES ("{}","{}",{});'''.format(qq, server, accid)
    print(command)
    cur.execute(command)
    con.commit()
    con.close()
    return 0

def read_accid(qq):
    con, cur = connect_db()
    cur.execute('''SELECT * FROM player WHERE qq={};'''.format(qq))
    row = cur.fetchone()
    if row == None:
        con.close()
        return -1
    else:
        result = {'server': row[1], 'accid': row[2]}
        con.close()
        return result

