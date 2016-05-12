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
        "ip": "ip",
        "port": port,
        "name": "db",
        "msd": 3,
        "collection_list": [{
            "complete": "discovery_complete"
        }, {
            "todo": "discovery_todo"
        }, {
            "inventory": "discovery_inventory"
        }, {
            "remediation": "discovery_remediation"
        }, {
            "unknown": "discovery_unknown"
        }, {
            "cdp": "discovery_cdp"
        }, {
            "known": "discovery_known"
        }, {
            "performance": "discovery_performance"
        }],
        "seed_ips": [
            "a",
            "b",
            "c"
        ]
    },
    "default_info": {
        "un": "un",
        "pw": "pw",
        "port": 22
    }
}
```
