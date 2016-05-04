import re

def main(self):

	command(self)
	self.command_result = self.ssh_session.child_execute(command=self.command)
	set_properties(self)
	return


def command(self):
	self.command = ('show ip int brief\n')
	return

def set_properties(self,regex_value="default"):

	# Set the vrf property
	split_by_lines = self.command_result.split('\n')
	# Pop last line

	dict_array = []

	split_by_lines.pop()
	split_by_lines.pop(0)
	split_by_lines.pop(0)
	for index, line in enumerate(split_by_lines):
		split_line = line.split()
		tmp_dict = {"interface_name": split_line[0], 
		"interface_ip": split_line[1],
		"interface_method": split_line[3], 
		"interface_status": split_line[4],
		"interface_protocol": split_line[5]}
		if split_line[1] == "unassigned":
			pass
		else:
			self.ipaddress_self.append(split_line[1])
		dict_array.append(tmp_dict)

	self.interfaces = dict_array
	return
