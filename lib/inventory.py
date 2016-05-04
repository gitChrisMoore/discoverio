import re

def main(self):

	command(self)
	self.command_result = self.ssh_session.child_execute(command=self.command)
	audit(self)
	set_properties(self)
	return

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
