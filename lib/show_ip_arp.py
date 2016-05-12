import re
import logging
import sys
import cmd_director

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


# Example SNMP
class ShowIPARP(cmd_director.Builder):

	def get_cmd(self, vrf_name='default'):
		self.container.cmd = ('show ip arp\n')

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
			tmp_dict = {"ip_address": split_line[1], 
			"mac_address": split_line[3]}
			dict_array.append(tmp_dict)
		self.container.regex_result = dict_array