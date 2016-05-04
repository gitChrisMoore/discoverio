import re

def main(self):

	command(self)
	self.command_result = self.ssh_session.child_execute(command=self.command)
	audit(self)
	set_properties(self)
	return

def audit(self):
	match = re.findall(r"snmp-server community (.+?)(\n|,)", self.command_result)
	if len(match) > 1:
		self.snmp_audit = True
	else:
		self.snmp_audit = False
	return

def command(self):
	self.command = ('show run | i snmp-server comm\n')
	return

def set_properties(self,regex_value="default"):
	match = re.search(r"snmp-server community (.+?)(\r|,)", self.command_result)
	split_match = match.group(0).split()
	self.snmp_community = split_match[2]
	self.snmp_configtype = split_match[3]
	self.snmp_acl = split_match[4]
	print match
	return
