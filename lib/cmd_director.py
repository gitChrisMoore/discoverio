import re
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

# Abstract Factory
# https://github.com/faif/python-patterns/blob/master/builder.py
# Directory
class Director(object):

	def __init__(self):
		self.builder = None

	def construct_container(self, vrf_name='default'):
		self.builder.new_container()
		self.builder.get_cmd(vrf_name)

	def container_filter(self, cmd_output):
		self.builder.get_regex()
		self.builder.filter_cmd_output(cmd_output)
		self.builder.set_properties()

	def get_container(self):
		return self.builder.container

# Abstract Builder
class Builder(object):

	def __init__(self):
		self.container = None

	def new_container(self):
		self.container = Container()

	def get_cmd(self):
		raise NotImplementedError

	def get_regex(self):
		raise NotImplementedError

	def filter_cmd_output(self):
		raise NotImplementedError

	def set_properties(self):
		raise NotImplementedError

# Product Container

class Container(object):

	def __init__(self):
		self.cmd = None
		self.regex = None
		self.filtered_output = None
		self.regex_result = None

	def __repr__(self):
		return 'cmd: {0.cmd} | regex: {0.regex} | filtered_output: {0.filtered_output} | regex_result: {0.regex_result} '.format(self)

# Client
if __name__ == "__main__":
    director = Director()
    director.builder = BuilderSNMP()
    director.construct_container()
    building = director.get_container()
    print(building)
