import db
import config


cfg = config.set_config()
d = db.DBClient(cfg['db_ip'], cfg['db_name']).main()


class main(object):

    print 'Dropping existing database collections'
    a = [d[x.values()[0]].drop()
         for x in cfg['collection_list']]
    print a

    print 'Checking that all collections are dropped'
    b = [d[x.values()[0]].find().count()
         for x in cfg['collection_list']]
    print b

    print 'Setting unique fields'
    l = ['discovery_todo', 'discovery_completed', 'discovery_cdp']
    c = [d[x].create_index("ip_address", unique=True)
         for x in l]
    print c

    print 'seeding the database'
    f = [d.discovery_todo.insert({"ip_address": x})
         for x in cfg['seed_ips']]
    print f

    print 'should fail'
    try:
        g = [d.discovery_todo.insert({"ip_address": x})
             for x in cfg['seed_ips']]
        print g
    except Exception as e:
        print 'this should fail.... e: {}'.format(str(e))

    print 'Complete!!!'

main()
