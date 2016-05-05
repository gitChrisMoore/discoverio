import re

def main(self):

	self.bgp_neighbors = []
	command(self)
	self.command_result = self.ssh_session.child_execute(command=self.command)
	set_properties(self)
	if self.vrf:
		for vrf in self.vrf:
			#print vrf
			command_vrf(self=self,vrf_name=vrf['vrf_name'])
			self.command_result = self.ssh_session.send_command(command=self.command)
			get_bgp_neighbors(self=self,vrf_name=vrf['vrf_name'])
	return

def command(self):
	self.command = ('show ip bgp summary\n')
	return

def command_vrf(self,vrf_name):
	command = ('show bgp vpnv4 unicast vrf ' + vrf_name + ' neighbors')
	return

def bgp_exist_test(self):
	split_by_lines = self.command_result.split('\n')
	for line in split_by_lines:
		if re.match(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line):
			return True
	return False

def get_bgp_neighbors(self, vrf_name):

	split_by_lines = self.command_result.split('\n')
	for line in split_by_lines:
		if re.match(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line):
			split_line = line.split()
			tmp_dict = {"bgp_neighbor_ip": split_line[0], 
			"bgp_neighbor_version": split_line[1],
			"bgp_neighbor_up_down": split_line[8], 
			"bgp_neighbor_pfxrcd": split_line[9],
			"bgp_neighbor_vrf": vrf_name}
			self.ipaddress_neighbor.append(split_line[0])
			self.bgp_neighbors.append(tmp_dict)
	return

def set_properties(self,regex_value="default"):

	if not bgp_exist_test(self):
		return
	else:
		bgp_router_id = re.findall(r"BGP router identifier (.+?)(\n|,)", self.command_result)
		bgp_local_as = re.findall(r"local AS number (.+?)(\n|,)", self.command_result)

		self.bgp_router_id = bgp_router_id[0][0]
		self.bgp_local_as = bgp_local_as[0][0]

		get_bgp_neighbors(self=self, vrf_name='default')
	return
