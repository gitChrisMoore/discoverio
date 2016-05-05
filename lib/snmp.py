import re

def main(self):

	self.snmp_community = []
	command(self)
	self.command_result = self.ssh_session.child_execute(command=self.command)
	audit(self)
	set_properties(self)

def audit(self):
	pass

def command(self):
	self.command = ('show run | i snmp-server comm\n')
	return

def set_properties(self,regex_value="default"):
	dict_array = []
	comm_str = re.findall(r"snmp-server community (.+?)(\n|,)", self.command_result)

	for value in range(0, len(comm_str)):
		tmp_dict = {"comm_str": comm_str[value][0].strip()
		}
		dict_array.append(tmp_dict)

	self.snmp_community = dict_array
	return
