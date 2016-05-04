import re

def main(self):

	command(self)
	self.command_result = self.ssh_session.child_execute(command=self.command)
	audit(self)
	set_properties(self)
	return

def audit(self):

	match = re.findall(r"username (.+?)(\n|,)", self.command_result)
	if len(match) == 1:
		self.username_audit = True
	else:
		raise Exception(self.command_result)
	return

def command(self):
	self.command = ('show run | i usern\n')
	return

def set_properties(self,regex_value="default"):
	split_by_lines = self.command_result.split('\n')
	split_by_space = split_by_lines[1].split()
	self.username = split_by_space[1]
	return