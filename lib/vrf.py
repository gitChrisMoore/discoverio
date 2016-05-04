import re

def main(self):

	command(self)
	self.command_result = self.ssh_session.send_commandself.ssh_session.child_execute
	return

def audit(self):
	pass

def command(self):
	self.command = ('show ip vrf brief\n')
	return

def set_properties(self,regex_value="default"):

	# Test to see if there is a VRF
	split_by_lines = self.command_result.split('\n')
	if len(split_by_lines) < 4:
		self.vrf = None
		return

	dict_array = []

	# Set the vrf property
	split_by_lines = self.command_result.split('\n')
	# Pop last line
	split_by_lines.pop()
	split_by_lines.pop(0)
	split_by_lines.pop(0)
	for line in split_by_lines:
		split_by_space = line.split()
		if re.search('^\s*[0-9]', split_by_space[1]):
			vrf_name = split_by_space[0]
			vrf_rd = split_by_space[1]
			vrf_interfaces = []
			split_by_space.pop(0)
			split_by_space.pop(0)
			for interface in split_by_space:
				vrf_interfaces.append(interface)
			dict_vrf = {"vrf_name": vrf_name, "vrf_rd": vrf_rd, "vrf_interfaces": vrf_interfaces}
			dict_array.append(dict_vrf)
	self.vrf = dict_array

	return
