import re

def main(self):

	command(self)
	self.command_result = self.ssh_session.child_execute(command=self.command)
	set_properties(self)
	return

def command(self):
	self.command = ('show cdp neighbor detail\n')
	return

def set_properties(self,regex_value="default"):
	#print(self.command_result)

	dict_array = []
	neighbor_id = re.findall(r"Device ID: (.+?)(\n|,)", self.command_result)
	neighbor_platform = re.findall(r"Platform: (.+)(\n|,)", self.command_result)
	neighbor_capabilities = re.findall(r"Capabilities: (.+?)(\n|,)", self.command_result)
	neighbor_local_port = re.findall(r"Interface: (.+?)(\n|,)", self.command_result)
	neighbor_remote_port = re.findall(r"Port ID \(outgoing port\): (.+)(\n|,)", self.command_result)

	for value in range(0, len(neighbor_id)):
		tmp_dict = {"neighbor_id": neighbor_id[value][0].strip(), 
		"neighbor_platform": neighbor_platform[value][0].strip(),
		"neighbor_capabilities": neighbor_capabilities[value][0].strip(), 
		"neighbor_local_port": neighbor_local_port[value][0].strip(),
		"neighbor_remote_port": neighbor_remote_port[value][0].strip()}
		dict_array.append(tmp_dict)

	self.cdp_info = dict_array

	return
