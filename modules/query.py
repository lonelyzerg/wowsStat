import requests

APP_ID = ''
URL_BASE = 'https://api.worldofwarships.{}/wows/account/'

RECENT_BASE = 'https://{}wows-numbers.com/user/snapshot/ships.ajax?accountId={}&date={}&type=pvp'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'


def init(appid):
    global APP_ID
    APP_ID = appid
    print('appid:', APP_ID)


def get_base_url(server):
    # check server
    if (server == 'na'):
        url_base = URL_BASE.format('com')
    elif (server == 'asia'):
        url_base = URL_BASE.format('asia')
    elif (server == 'eu'):
        url_base = URL_BASE.format('eu')
    elif (server == 'ru'):
        url_base = URL_BASE.format('ru')
    else:
        return -1

    return url_base


def get_recent_url(server, accountID, date):
    # check server
    if (server == 'na'):
        url = RECENT_BASE.format('na.', accountID, date)
    elif (server == 'asia'):
        url = RECENT_BASE.format('asia.', accountID, date)
    elif (server == 'eu'):
        url = RECENT_BASE.format('', accountID, date)
    elif (server == 'ru'):
        url = RECENT_BASE.format('ru.', accountID, date)
    else:
        return -1

    return url


def get_stat(server, accid, extra='', fields='', language='zh-cn'):
    # get base url
    url_base = get_base_url(server)

    # stat prefix
    url = url_base + 'info/?'

    # add app id
    url = url + 'application_id=' + APP_ID

    # add acc id
    url = url + '&' + 'account_id=' + str(accid)

    # add other parameters if not empty
    if (extra):
        url = url + '&' + 'extra=' + extra

    if (fields):
        url = url + '&' + 'fields=' + fields

    if (language):
        url = url + '&' + 'language=' + language

    # print(url)
    # get data
    r = requests.get(url=url)

    return r.json()['data'][str(accid)]


def get_recent_stat(server, accid, date):
    url = get_recent_url(server, accid, date)
    return -1


def get_pvp(server, accid):
    return get_stat(server, accid)


def get_pve(server, accid):
    return get_stat(server, accid, extra='statistics.pve', fields='-statistics.pvp')


def get_pvp_div2(server, accid):
    return get_stat(server, accid, extra='statistics.pvp_div2', fields='-statistics.pvp')


def get_pvp_div3(server, accid):
    return get_stat(server, accid, extra='statistics.pvp_div3', fields='-statistics.pvp')


def get_pvp_solo(server, accid):
    return get_stat(server, accid, extra='statistics.pvp_solo', fields='-statistics.pvp')


def get_rank(server, accid):
    return get_stat(server, accid, extra='statistics.rank_solo', fields='-statistics.pvp')


def get_ship_name(ship_id, language='zh-cn', fields='name'):
    url_base = 'https://api.worldofwarships.com/wows/encyclopedia/ships/?'

    # add app id
    url = url_base + 'application_id=' + APP_ID

    # add ship id
    url = url + '&' + 'ship_id=' + str(ship_id)

    if (fields):
        url = url + '&' + 'fields=' + fields

    if (language):
        url = url + '&' + 'language=' + language

    # get data
    r = requests.get(url=url).json()

    ship = r['data'][str(ship_id)]['name']

    return ship


def get_accid(server, nickname, type='exact'):
    # get base url
    url_base = get_base_url(server)

    # stat prefix
    url = url_base + 'list/?'

    # add app id
    url = url + 'application_id=' + APP_ID

    # add player nickname
    url = url + '&' + 'search=' + nickname

    # specify search type
    url = url + '&' + 'type=' + type

    # get data
    r = requests.get(url=url).json()

    # return -1 if not account not found
    if (len(r['data']) == 0):
        # return -1 if not account not found
        return -1
    else:
        accid = r['data'][0]['account_id']
        return accid


def get_stat_recent(server, accid, dates):
    return None


if __name__ == "__main__":
    data = get_accid('na', 'n00b_cv_fudge_me')
    print(data)
