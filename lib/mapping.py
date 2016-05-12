import show_inventory
import show_ip_int
import show_cdp_neighbors
import show_ip_bgp_all_neighbors

list_of_methods = [{"name": show_inventory.ShowInventory, "description": "inventory"},
{"name": show_ip_int.ShowIPInt, "description": "ip_interface"},
{"name": show_cdp_neighbors.ShowCDPNeghbors, "description": "cdp_info"},
{"name": show_ip_bgp_all_neighbors.RunBGPCommand, "description": "bgp_info"},
]

def return_function_list(self):
	return list_of_methods
