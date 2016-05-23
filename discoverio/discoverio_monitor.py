import db
import config
import time

cfg = config.set_config()
d = db.DBClient(cfg['db_ip'], cfg['db_name']).main()


def main():

    a = 'a'
    while a:
        dic = {}
        for item in cfg['collection_list']:
            dic[item.keys()[0]] = d[item.values()[0]].find().count()
        print dic
        time.sleep(20)

main()
