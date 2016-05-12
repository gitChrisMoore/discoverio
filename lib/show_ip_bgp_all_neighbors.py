import re
import logging
import sys
import cmd_director

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

# Example SNMP
class RunBGPCommand(cmd_director.Builder):

	def get_cmd(self, vrf_name='default'):
		self.container.cmd = ('show bgp all neighbors\n')

	def get_regex(self):
		pass

	def filter_cmd_output(self, cmd_output):
		self.container.filtered_output = cmd_output

	def set_properties(self):
		dict_array = []
		neighbor_ip = re.findall(r"BGP neighbor is (.+?)(\n|,)", self.container.filtered_output)
		neighbor_router_id = re.findall(r"remote router ID (.+)(\n|,)", self.container.filtered_output)

		for value in range(0, len(neighbor_ip)):
			dict_inv = {"neighbor_ip": neighbor_ip[value][0].strip(), 
			"neighbor_router_id": neighbor_router_id[value][0].strip()}
			dict_array.append(dict_inv)				
		self.container.regex_result = dict_array