# discoverio
network based discovery python script


Requires:
  Paramiko
  Mongodb

Also requires a config.json file to be created in the following fashion:
```
discoverio/
    disocverio/
        private.json            # required see below
        public.json             # required see below
        discoverio.py           # Main file for discovery
        discoverio_init.py      # This file resets the collections on the db to start
        discoverio_monitor.py   # Simple monitoring file

```

discoverio/disocverio/private.json
```
{

	"db_ip": "dbip",
	"db_port": 27017,
	"db_name": "db",
	"db_msd": 3,
	"test_ip": "ip",
	"un": "un",
	"pw": "pw",
	"locations": [{
		"friendly_name": "site_1",
		"phy_addr_country": "a",
		"ip_range": ["10.0.0.0/24"]
	}, {
		"friendly_name": "site_2",
		"phy_addr_country": "b",
		"ip_range": ["10.0.0.0/24"]
	}],
	"seed_ips": [
		"172.0.0.1",
		"10.0.0.1"
	]
}
```

discoverio/disocverio/public.json
```
{

		"collection_list": [{
			"complete": "discovery_completed"
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
		}]
}
```
