import db
import config
import time

cfg = config.set_config()
d = db.DBClient(cfg['db_ip'], cfg['db_name']).main()


def main():

    result = d.discovery_inventory.find()
    for i in result:
        print i

main()
