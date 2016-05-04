# discoverio
network based discovery python script


Requires:
  Paramiko
  Mongodb

Also requires a config.json file to be created in the following fashion:
```
/
	discovery.py 			- main app that looks through devices
	discovery_init.py 		- preps the environment to start
	discovery_inventory.py  - query database every 60 seconds for inventory
	discovery_mon.py 		- every 10 seconds shows the different queues
/lib/*
	This folder contains all of the protocol specific files which are looped through
/helpers/*
	This folder contains all of the wrappers which allow easy access to ssh and database
```

/helpers/config.json
```
{
    "db_config": {
        "remote_address": "dbip",
        "remote_port": 27017,
        "db_name": "databasename",
        "maxSevSelDelay": 3,
        "collection_todo": "discovery_todo",
        "collection_complete": "discovery_complete",
        "collection_inventory": "discovery_inventory",
        "collection_remediation": "discovery_remediation",
        "collection_list": [{
            "complete": "discovery_complete"
        }, {
            "todo": "discovery_todo"
        }, {
            "inventory": "discovery_inventory"
        }, {
            "remediation": "discovery_remediation"
        }, {
            "performance": "discovery_performance"
        }],
        "main": [{
            "adr": "dbip"
        }, {
            "prt": 27017
        }, {
            "dbn": "databasename"
        }, {
            "msd": 3
        }],
        "seed_ips": [
            "ip1",
            "ip2",
            "ip3"
        ]
    },
    "default_info": {
        "un": "username",
        "pw": "password",
        "port": 22
    }
}
```
