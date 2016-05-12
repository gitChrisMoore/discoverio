import re
import logging
import sys
import cmd_director

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

# Example SNMP
class ShowCDPNeghbors(cmd_director.Builder):

	def get_cmd(self, vrf_name='default'):
		self.container.cmd = ('show cdp neighbor detail\n')

	def get_regex(self):
		pass

	def filter_cmd_output(self, cmd_output):
		self.container.filtered_output = cmd_output

	def set_properties(self):
		dict_array = []
		neighbor_id = re.findall(r"Device ID: (.+?)(\n|,)", self.container.filtered_output)
		neighbor_platform = re.findall(r"Platform: (.+)(\n|,)", self.container.filtered_output)
		neighbor_ip = re.findall(r"IP address:(.+)(\n|,)", self.container.filtered_output)
		neighbor_capabilities = re.findall(r"Capabilities: (.+?)(\n|,)", self.container.filtered_output)
		neighbor_local_port = re.findall(r"Interface: (.+?)(\n|,)", self.container.filtered_output)
		neighbor_remote_port = re.findall(r"Port ID \(outgoing port\): (.+)(\n|,)", self.container.filtered_output)

		for value in range(0, len(neighbor_id)):
			tmp_dict = {"ip_address": neighbor_ip[value][0].strip(),
			"neighbor_platform": neighbor_platform[value][0].strip(),
			"neighbor_capabilities": neighbor_capabilities[value][0].strip(),
			"neighbor_local_port": neighbor_local_port[value][0].strip(),
			"neighbor_remote_port": neighbor_remote_port[value][0].strip()
			}
			dict_array.append(tmp_dict)

		self.container.regex_result = dict_array