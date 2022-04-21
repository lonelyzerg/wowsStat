import argparse

def parser():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='wws')

    subparsers = parser.add_subparsers(dest='func',help='功能')

    parser_set = subparsers.add_parser('set', help='将WG账号与QQ号绑定')
    parser_me = subparsers.add_parser('me', help='查询已绑定账号数据')
    parser_stat = subparsers.add_parser('stat', help='查询未绑定账号数据')

    parser_set.add_argument('server', choices=['na', 'asia', 'eu', 'ru'], help='服务器')
    parser_set.add_argument('nickname', help='游戏昵称')

    parser_me.add_argument('mode', nargs='*', help='查询内容')


    parser_stat.add_argument('server', choices=['na', 'asia', 'eu', 'ru'], help='服务器')
    parser_stat.add_argument('nickname', help='游戏昵称')
    parser_stat.add_argument('mode', nargs='*', help='查询内容')

    return parser

if __name__ == "__main__":
    p = parser()
    command = 'me'
    result = vars(p.parse_args(command.split()))
    print(result['mode'][0])

# wws set server name
# wws me/stat [server name] [random/ranked/record] [recent] [n]
# wws help