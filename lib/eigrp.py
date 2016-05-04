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
	self.command = ('show ip eigrp neighbors\n')
	return

def set_properties(self,regex_value="default"):

	# Set the vrf property
	split_by_lines = self.command_result.split('\n')
	# Pop last line

	dict_array = []

	for index, line in enumerate(split_by_lines):
		if re.search('^\s*[0-9]', line):
			split_line = line.split()

			tmp_dict = {"eigrp_address": split_line[1], 
			"eigrp_interface": split_line[2],
			"eigrp_hold": split_line[3], 
			"eigrp_srtt": split_line[4]}

			self.ipaddress_neighbor.append(split_line[1])
			
			dict_array.append(tmp_dict)

	self.eigrp_info = dict_array


	return
