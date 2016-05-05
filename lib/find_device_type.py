import re

def main(self):


	command(self)
	self.command_result = self.ssh_session.child_execute(command=self.command)
	set_properties(self)
	set_device_type(self)
	return

def set_device_type(self):
	method_name = 'set_device_type'
	known_devices = [{"PID": "WS-C3560-48PS-S", "device_type": "IOS", "vrf": False, "bgp": False},
	{"PID": "ISR4331/K9", "device_type": "IOS-XE"},
	{"PID": "ASR1000-ESP5", "device_type": "IOS-XE"},
	{"PID": "WS-X4515", "device_type": "IOS"},
	{"PID": "WS-C3650-48PS", "device_type": "IOS"},
	{"PID": "WS-C3650-48PD", "device_type": "IOS"},
	{"PID": "WS-X45-SUP6-E", "device_type": "IOS"},
	{"PID": "WS-X45-SUP8-E", "device_type": "IOS"},
	{"PID": "N7K-C7004", "device_type": "IOS-XE"},
	{"PID": "WS-C6K-VTT-E", "device_type": "IOS-XE"},
	{"PID": "WS-C3750X-24S-E", "device_type": "IOS"},
	{"PID": "WS-C3550-48-SMI", "device_type": "IOS"},
	{"PID": "WS-C3560G-24TS-S", "device_type": "IOS"},
	{"PID": "WS-C3750-48PS-E", "device_type": "IOS"},
	{"PID": "WS-C3560V2-48PS-S", "device_type": "IOS"},
	{"PID": "WS-C3750-48PS-E", "device_type": "IOS"},
	{"PID": "WS-C3650-48TD", "device_type": "IOS"},
	{"PID": "WS-C3750E-48TD-S", "device_type": "IOS"},
	{"PID": "WS-C3750X-48PF-S", "device_type": "IOS"},
	{"PID": "WS-C3750E-24TD-E", "device_type": "IOS"},
	{"PID": "WS-C3750G-12S-S", "device_type": "IOS"},
	{"PID": "WS-SUP720-3B", "device_type": "IOS"},
	{"PID": "WS-X45-SUP7-E", "device_type": "IOS"},
	{"PID": "WS-C3560V2-24PS-S", "device_type": "IOS"},
	{"PID": "WS-C3750X-48P-S", "device_type": "IOS"},
	{"PID": "WS-X45-SUP6L-E", "device_type": "IOS"},
	{"PID": "WS-C3750G-24PS-S", "device_type": "IOS"},
	{"PID": "WS-SUP720-3B", "device_type": "IOS"},
	{"PID": "CISCO2851", "device_type": "IOS"},
	]


	self.device_type = None
	for i in self.inventory:
		for j in known_devices:
			for (key, value) in set(i.items()) & set(j.items()):
			    self.device_type = j

def audit(self):
	pass

def command(self):
	self.command = ('show inventory\n')
	return

def set_properties(self,regex_value="default"):
	dict_array = []
	name = re.findall(r"NAME: (.+?)(\n|,)", self.command_result)
	desc = re.findall(r"DESCR: (.+)(\n|,)", self.command_result)
	pid = re.findall(r"PID: (.+?)(\n|,)", self.command_result)
	vid = re.findall(r"VID: (.+?)(\n|,)", self.command_result)
	sn = re.findall(r"SN: (.+)", self.command_result)

	for value in range(0, len(name)):
		dict_inv = {"Name": name[value][0].strip(), "Desc": desc[value][0].strip(),
		"PID": pid[value][0].strip(), "VID": vid[value][0].strip(), "SN": sn[value].strip()}
		dict_array.append(dict_inv)

	self.inventory = dict_array
	return
