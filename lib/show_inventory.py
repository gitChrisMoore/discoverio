import re
import logging
import sys
import cmd_director

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

# Example SNMP
class ShowInventory(cmd_director.Builder):

	def get_cmd(self, vrf_name='default'):
		self.container.cmd = ('show inventory\n')

	def get_regex(self):
		pass

	def filter_cmd_output(self, cmd_output):
		self.container.filtered_output = cmd_output

	def set_properties(self):
		dict_array = []
		name = re.findall(r"NAME: (.+?)(\n|,)", self.container.filtered_output)
		desc = re.findall(r"DESCR: (.+)(\n|,)", self.container.filtered_output)
		pid = re.findall(r"PID: (.+?)(\n|,)", self.container.filtered_output)
		vid = re.findall(r"VID: (.+?)(\n|,)", self.container.filtered_output)
		sn = re.findall(r"SN: (.+)", self.container.filtered_output)

		for value in range(0, len(name)):
			dict_inv = {"Name": name[value][0].strip(), "Desc": desc[value][0].strip(),
			"PID": pid[value][0].strip(), "VID": vid[value][0].strip(), "SN": sn[value].strip()}
			dict_array.append(dict_inv)				
		self.container.regex_result = dict_array