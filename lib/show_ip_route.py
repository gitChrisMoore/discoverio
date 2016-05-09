import re
import logging
import sys
import cmd_director

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


#
class ShowIPRoute(cmd_director.Builder):

	def get_cmd(self, vrf_name):
		if vrf_name == 'default':
			self.container.cmd = ('show ip route\n')
		else:
			self.container.cmd = ('show ip route vrf ' + str(vrf_name) +'\n')

	def get_regex(self):
		pass

	def filter_cmd_output(self, cmd_output):
		self.container.filtered_output = re.findall(
			r'(?<=via )([0-9]+(?:\.[0-9]+){3})(?=.*)', cmd_output)

	def set_properties(self):
		self.container.regex_result = self.container.filtered_output