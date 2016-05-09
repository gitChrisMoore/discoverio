import re
import logging
import sys
import snmpv2

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


# Example SNMP
class ShowIPInt(snmpv2.Builder):

	def get_cmd(self, vrf_name='default'):
		self.container.cmd = ('show ip int brief\n')

	def get_regex(self):
		pass

	def filter_cmd_output(self, cmd_output):
		self.container.filtered_output = cmd_output.split('\n')

	def set_properties(self):
		dict_array = []
		self.container.filtered_output.pop()
		self.container.filtered_output.pop(0)
		self.container.filtered_output.pop(0)
		for index, line in enumerate(self.container.filtered_output):
			split_line = line.split()
			tmp_dict = {"interface_name": split_line[0], 
			"interface_ip": split_line[1],
			"interface_method": split_line[3], 
			"interface_status": split_line[4],
			"interface_protocol": split_line[5]}
			dict_array.append(tmp_dict)
		self.container.regex_result = dict_array