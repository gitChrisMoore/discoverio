import logging
import sys
import helpers.load_config
import helpers.ssh_child
import helpers.db
import os
import time
import lib.mapping
import lib.show_ip_route
import lib.show_ip_vrf

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class BuildContainers(object):
	""" This provides a wrapper around the MongoClient package, and also 
	allows for some default values to be added.
	"""

	def __init__(self):
		self.config = helpers.load_config.load_config(self)
		# Create the DB object
		self.db = helpers.db.DBWrapper()
		self.db.start_conn()
		self.director = lib.cmd_director.Director()
		self.stats = {}
		self.vrf = ['default']
		self.ip_discovered_list = []
		self.ip_owned_list = []

	def main(self):
		# standard start config: start
		self.abs_start(method_name = 'main')
		# standard start config: end
		while self.db.count_collection(
			collection=self.db.cfg['todo']) > 0:
			new_device = False
			while new_device == False:
				next_device = self.db.find_one_and_delete(collection=self.db.cfg['todo'])
				self.current_ip = next_device['ip_address']
				if self.db.ip_in_collection(ip= self.current_ip, collection=self.db.cfg['complete']):
					new_device = False
					print 'device already scanned'
				else:
					print 'need to scan devie'
					new_device = True

			self.start_ssh_session()

			
			self.get_function_list()

			try:
				self.check_for_vrf()
		

				for vrf in self.vrf:
					self.loop_show_ip_route(vrf_name=vrf)

				self.main_loop()	

				# Add Devices to the completed collection
				for device in self.ip_interface:
					if device['interface_ip'] == 'unassigned':
						pass
					else:
						self.db.add_ip_to_collection(ip=device['interface_ip'], 
							collection=self.db.cfg['complete'])

				# Add devices to the todo collection
				for device in self.ip_discovered_list:
					result = self.db.add_ip_if_not_exist(
						ip=device,
						first_collection=self.db.cfg['complete'],
						second_collection=self.db.cfg['todo'])

				# standard start config: start
				self.abs_end(method_name='main')
				# standard start config: end
				self.add_inventory()
			except Exception as e:
				pass	

	def add_inventory(self):
		# standard start config: start
		method_name = 'add_inventory'
		self.abs_start(method_name = method_name)
		# standard start config: end
		try:
			# Set the new inventory object
			self.new_inventory = {"host_ip": self.current_ip,
				"inventory": self.inventory,
				}

			# Insert the document into the database
			self.db.insert_single_document(
				collection_name=
					self.db.cfg['inventory'],
				document = self.new_inventory)
			# Log the successfuly output
			log.debug('{0}:added document: {1}'.format(
				method_name, self.new_inventory))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))

	def check_for_vrf(self):
		# standard start config: start
		self.abs_start(method_name = 'check_for_vrf')
		# standard start config: end

		self.director.builder = lib.show_ip_vrf.ShowIPVRF()
		self.director.construct_container()
		container = self.director.get_container()
		cmd_output = self.ssh_session.child_execute(command=container.cmd)
		self.director.container_filter(cmd_output)
		result = self.director.get_container()
		if len(result.regex_result) > 0:
			self.vrf = self.vrf + result.regex_result

		# standard start config: start
		self.abs_end(method_name='check_for_vrf')
		# standard start config: end

	def loop_show_ip_route(self, vrf_name):
		# standard start config: start
		method_name = 'loop_show_ip_route'
		self.abs_start(method_name = method_name)
		# standard start config: end

		self.director.builder = lib.show_ip_route.ShowIPRoute()
		self.director.construct_container(vrf_name=vrf_name)
		container = self.director.get_container()
		cmd_output = self.ssh_session.child_execute(command=container.cmd)
		self.director.container_filter(cmd_output)
		result = self.director.get_container()
		self.ip_discovered_list = self.ip_discovered_list + result.regex_result

		# standard start config: start
		self.abs_end(method_name='loop_show_ip_route')
		# standard start config: end		

	def main_loop(self):
		# standard start config: start
		method_name = 'main_loop'
		self.abs_start(method_name = 'main_loop')
		# standard start config: end
		for method in self.function_list:
			# standard start config: start
			try:
				self.abs_start(method_name = method['description'])
				# standard start config: end
				self.director.builder = method['name']()
				self.director.construct_container()
				container = self.director.get_container()
				cmd_output = self.ssh_session.child_execute(command=container.cmd)
				self.director.container_filter(cmd_output)
				result = self.director.get_container()
				setattr(self, method['description'], result.regex_result)
				# standard start config: start
				self.abs_end(method_name = method['description'])
				# standard start config: end
			except Exception as e:
				log.error('{0}:exception:'.format(method['description']))
				log.error('{0}:error: {1}'.format(method['description'], str(e)))
				# standard start config: start
				self.abs_end(method_name= method['description'])
				# standard start config: end
		# standard start config: start
		self.abs_end(method_name='main_loop')
		# standard start config: end

	def start_ssh_session(self):
		# standard start config: start
		method_name = 'start_ssh_session'
		self.abs_start(method_name = 'start_ssh_session')
		# standard start config: end
		try:
			self.ssh_session = helpers.ssh_child.SSHChild(
				host=self.current_ip,
				un=self.config['default_info']['un'],
				pw=self.config['default_info']['pw'],
				port=self.config['default_info']['port'])
			log.debug('{0}:success: {1}'.format(
				method_name, self.ssh_session))
			# standard start config: start
			self.abs_end(method_name='start_ssh_session')
			# standard start config: end
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))
			# standard start config: start
			self.abs_end(method_name='start_ssh_session')
			# standard start config: end
	def get_function_list(self):
		self.function_list = lib.mapping.return_function_list(self)
	def get_vrf_function_list(self):
		self.function_list = lib.mapping.return_vrf_function_list(self)
	# Start and End Abstract
	def abs_start(self, method_name):
		self.set_time(method_name=method_name, action='_start')
		log.debug('{0}: starting'.format(method_name))
	def abs_end(self, method_name):
		self.set_time(method_name=method_name, action='_finish')
		self.execution_time(method_name=method_name)
		log.debug('{0}: ending'.format(method_name))
	# Performance Helper Methods
	def set_time(self, method_name, action):
		self.stats[method_name + action] = time.time()
	def execution_time(self, method_name):
		self.stats[method_name + '_exec_time'] = (self.stats[method_name + '_finish'] - 
			self.stats[method_name + '_start'])
# Client
if __name__ == "__main__":
    client = BuildContainers()
    client.main()