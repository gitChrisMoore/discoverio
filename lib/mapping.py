import snmp
import username
import inventory
import vrf
import cdp
import eigrp
import bgp
import int_brief
import logging
import time
import mapping
import find_device_type

list_of_functions = [ {"function_name": find_device_type, "error_function_name": "find_device_type"},
	{"function_name": snmp, "error_function_name": "snmp"},
	{"function_name": username, "error_function_name": "username"},
	{"function_name": inventory, "error_function_name": "inventory"},
	{"function_name": vrf, "error_function_name": "vrf"},
	{"function_name": cdp, "error_function_name": "cdp"},
	{"function_name": eigrp, "error_function_name": "eigrp"},
	{"function_name": bgp, "error_function_name": "bgp"},
	{"function_name": int_brief, "error_function_name": "int_brief"},
]


def return_list_of_functions(self):
	return list_of_functions