def mapping():

    def _mapping():
        data = [
            {
                "regex_split": "\n",
                "runtime_command": "show ip arp\n",
                "name": "arp",
                "method_list": [
                    {"regex_method": "regex", "regex_syntax": "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
                     "item_property": "ip_address"},
                    {"regex_method": "regex", "regex_syntax": "(   (.*)  ARPA", "item_property": "mac_address"}
                ]
            },
            {
                "regex_split": "-------------------------",
                "runtime_command": "show cdp neighbor detail\n",
                "name": "cdp",
                "method_list": [{"regex_method": 'regex_group_one', "regex_syntax": "Device ID: (.+?)(\n|,)", "item_property": "device_id"},
                    {"regex_method": "regex", "regex_syntax": "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", "item_property": "entry_ip_address"},
                    {"regex_method": "regex", "regex_syntax": "Platform: (.+?)(\n|,)", "item_property": "platform"},
                    {"regex_method": "regex", "regex_syntax": "Capabilities: (.+?)(\n|,)", "item_property": "capabilities"},
                    {"regex_method": "regex", "regex_syntax": "Holdtime : (.+?)(\n|,)", "item_property": "holdtime"},
                    {"regex_method": "regex", "regex_syntax": "Version :\n(.*)\n", "item_property": "version"},
                    {"regex_method": "regex", "regex_syntax": "advertisement version: (.*)\n", "item_property": "advertisement_version"},
                    {"regex_method": "regex", "regex_syntax": "VTP Management Domain: (.*)\n", "item_property": "vtp_management_domain"},
                    {"regex_method": "regex", "regex_syntax": "Duplex: (.*)\n", "item_property": "duplex"},
                    {"regex_method": "regex", "regex_syntax": "Management address\(es\):\n  IP address: (.+?)(\n|,)", "item_property": "management_ip_address"},
                ]
            },
            {
                "regex_split": "\n\n",
                "runtime_command": "show inventory\n",
                "name": "inventory",
                "method_list": [
                    {"regex_method": "regex", "regex_syntax": "NAME: \"(.+?)(\n|,|\")", "item_property": "name"},
                    {"regex_method": "regex", "regex_syntax": "DESCR: \"(.+?)(\n|,|\")", "item_property": "descr"},
                    {"regex_method": "regex", "regex_syntax": "PID: (.+?)(\n|,)", "item_property": "pid"},
                    {"regex_method": "regex", "regex_syntax": "VID: (.+?)(\n|,)", "item_property": "vid"},
                    {"regex_method": "regex", "regex_syntax": "SN: (.+)", "item_property": "sn"}
                ]
            },
            {
                "regex_split": "\n",
                "runtime_command": "show ip route\n",
                "name": "route",
                "method_list": [
                    {"regex_method": "regex", "regex_syntax": "(?<=via )([0-9]+(?:\.[0-9]+){3})(?=.*)",
                     "item_property": "next_hop"}
                ]
            },
            {
                "regex_split": "\n\n",
                "runtime_command": "show bgp all neighbors\n",
                "name": "bgp",
                "method_list": [
                    {"regex_method": "regex", "regex_syntax": "BGP neighbor is (.+?)(\n|,)",
                     "item_property": "neighbor_ip"},
                    {"regex_method": "regex", "regex_syntax": "remote router ID (.+)(\n|,)", "item_property": "neighbor_router_id"}
                ]
            },
            {
                "regex_split": "\n",
                "runtime_command": "show ip eigrp neighbors\n",
                "name": "eigrp",
                "method_list": [
                    {"regex_method": "regex", "regex_syntax": "([0-9]+(?:\.[0-9]+){3})(?=.*)", "item_property": "eigrp_neighbor"}
                ]
            },
            {
                "regex_split": "\n",
                "runtime_command": "show ip int brief\n",
                "name": "int",
                "method_list": [
                    {"regex_method": "regex", "regex_syntax": "([0-9]+(?:\.[0-9]+){3})(?=.*)", "item_property": "int"}
                ]
            },
            {
                "regex_split": "\n",
                "runtime_command": "show vrf detail\n",
                "name": "vrf",
                "method_list": [
                    {"regex_method": "regex", "regex_syntax": "VRF (.+?)(\n|,|\()", "item_property": "vrf"}
                ]
            }
        ]
        return data

    return _mapping()