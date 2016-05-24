import config
import db
import mapping
import ssh
import workflows
import mixins

cfg = config.set_config()
d = db.DBClient(cfg['db_ip'], cfg['db_name']).main()


def main():

    while d.discovery_todo.find().count() > 0:
        try:
            next_device = db.NextAvailDoc().main(d)
            s = ssh.Session(next_device['ip_address'], cfg['un'], cfg['pw'])
            upsert_doc(next_device, next_device['ip_address'], 'discovery_completed')
            current_ip = next_device['ip_address']
            m = mapping.mapping()
            d_complete = discovery_loop(s, m)
            update_collections(d_complete, current_ip)
        except Exception as e:
            print upsert_doc(next_device, next_device['ip_address'], 'discovery_completed')

def discovery_loop(s, m):

    def _discovery_loop():
        d = {}
        for i in m:
            cmd_result = s.cmd(i['runtime_command'])
            split_result = workflows.regex_split(cmd_result, i['regex_split'])
            d[i['name']] = workflows.loop_through_output(split_result, i['method_list'])
        return d

    return _discovery_loop()


def update_collections(d_complete, current_ip):

    def _update_collections():
        try:
            [upsert_doc(x, x.values()[0], 'discovery_completed')
             for x in mixins.make_completed_list(d_complete)]

            [upsert_doc(x, x.values()[0], 'discovery_todo')
             for x in mixins.make_todo_list(d_complete)]

            [upsert_doc(x, x.values()[0], 'discovery_cdp')
             for x in mixins.make_cdp_list(d_complete)]

            inventory_doc = {"ip_address": current_ip, "inventory": mixins.make_inventory_list(d_complete)}
            upsert_doc(inventory_doc, current_ip, 'discovery_inventory')

        except Exception as e:
            print str(e)

    return _update_collections()


def build_inventory():

    def _build_inventory():
        return

    return _build_inventory()

def upsert_doc(doc, ip, col):
    try:
        d[col].update_one({'ip_address': ip}, {'$set': doc}, upsert=True)
    except Exception as e:
        print str(e)


main()