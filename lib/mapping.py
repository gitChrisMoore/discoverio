import show_inventory
import show_ip_int

list_of_methods = [{"name": show_inventory.ShowInventory, "description": "inventory"},
{"name": show_ip_int.ShowIPInt, "description": "ip_interface"}
]

def return_function_list(self):
	return list_of_methods
