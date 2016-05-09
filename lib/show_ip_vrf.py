import re
import logging
import sys
import cmd_director

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


# Example SNMP
class ShowIPVRF(cmd_director.Builder):

	def get_cmd(self, vrf_name='default'):
		self.container.cmd = ('show run | i ip vrf\n')

	def get_regex(self):
		pass

	def filter_cmd_output(self, cmd_output):
		self.container.filtered_output = cmd_output.split('\n')

	def set_properties(self):
		# Pop last line
		dict_array = []
		for line in self.container.filtered_output:
			split_by_space = line.split()
			if len(split_by_space) == 3:
				dict_array.append(split_by_space[2])
		self.container.regex_result = dict_array