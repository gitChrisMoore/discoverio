import logging
import sys
import helpers.load_config
import helpers.ssh_child
import helpers.db
import lib.lib_loop
import os
import time

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

class Discovery(object):
	""" This provides a wrapper around the MongoClient package, and also 
	allows for some default values to be added.
	"""

	def __init__(self):
		self.config = helpers.load_config.load_config(self)
		# Create the DB object
		self.db = helpers.db.DBWrapper(
			remote_address=self.config['db_config']['remote_address'],
			remote_port=self.config['db_config']['remote_port'],
			db_name=self.config['db_config']['db_name'],
			maxSevSelDelay=self.config['db_config']['maxSevSelDelay'],)

	def main(self):
		method_name = 'main'
		log.debug('{0}: starting'.format(method_name))

		# Count the number of documents which are left in the collection
		while self.db.count_collection(
			collection=self.config['db_config']['collection_todo']) > 0:
			# Get the next IP address
			self.time_get_next_device = time.time()
			self.get_next_device()
			# Build an SSH session to the next device in thelist
			self.time_start_ssh_session = time.time()
			self.start_ssh_session()
			# Start the loop through all of the library
			self.time_loop_through_lib = time.time()
			self.loop_through_lib()
			# Add all of the errors to remediation database
			self.time_add_remediations = time.time()
			self.add_remediations()
			# Add the information to the inventory
			self.time_add_inventory = time.time()
			self.add_inventory()
			# Add the addresses to the list of devices to scan
			self.time_add_todo_devices = time.time()
			self.add_todo_devices()
			# Add the list of devices which are found on the device
			self.time_add_self_devices = time.time()
			self.add_self_devices()
			self.time_end = time.time()
			# Get the statistics
			self.device_statistics()
			self.add_performance()

	def get_next_device(self):
		# Try to start the ssh session
		method_name = 'get_next_device'
		log.debug('{0}: starting'.format(method_name))
		try:
			document = self.db.find_one_and_delete(
				collection=self.config['db_config']['collection_todo'])
			self.current_ip = document['ip_address']
			log.debug('{0}:added document: {1}'.format(
				method_name, document))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))


	def loop_through_lib(self):
		# Try to start the ssh session
		method_name = 'loop_through_lib'
		log.debug('{0}: starting'.format(method_name))
		self.inventory = {}
		self.error_list = []
		self.ipaddress_neighbor = []
		self.ipaddress_self = []
		try:
			lib.lib_loop.main(self)
			log.debug('{0}:success: loop complete'.format(method_name))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))

	def add_self_devices(self):
		# Try to start the ssh session
		method_name = 'add_self_devices'
		log.debug('{0}: starting'.format(method_name))

		try:
			if len(self.ipaddress_self) > 0 :
				for ip_address in self.ipaddress_self:
					self.db.add_ip_to_collection(ip=ip_address,
						collection=
							self.config['db_config']['collection_complete'])
					log.debug('{0}:added document: {1}'.format(
						method_name, ip_address))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))

	def add_todo_devices(self):
		# Try to start the ssh session
		method_name = 'add_todo_devices'
		log.debug('{0}: starting'.format(method_name))

		try:
			if len(self.ipaddress_neighbor) > 0 :
				for ip_address in self.ipaddress_neighbor:
					self.db.add_ip_if_not_exist(ip=ip_address,
						first_collection=
							self.config['db_config']['collection_complete'],
						second_collection=
							self.config['db_config']['collection_todo'])
					log.debug('{0}:added document: {1}'.format(
						method_name, ip_address))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))

	def add_inventory(self):
		# Try to start the ssh session
		method_name = 'add_inventory'
		log.debug('{0}: starting'.format(method_name))

		try:
			# Set the new inventory object
			new_inventory = {"host_ip": self.current_ip,
				"inventory": self.inventory,
				}

			# Insert the document into the database
			self.db.insert_single_document(
				collection_name=
					self.config['db_config']['collection_inventory'],
				document = new_inventory)
			# Log the successfuly output
			log.debug('{0}:added document: {1}'.format(
				method_name, new_inventory))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))

	def add_performance(self):
		# Try to start the ssh session
		method_name = 'add_performance'
		log.debug('{0}: starting'.format(method_name))

		try:
			# Insert the document into the database
			self.db.insert_single_document(
				collection_name=
					self.config['db_config']['collection_performance'],
				document = self.device_stats)
			# Log the successfuly output
			log.debug('{0}:added document: {1}'.format(
				method_name, self.device_stats))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))


	def add_remediations(self):
		# Try to start the ssh session
		method_name = 'add_remediations'
		log.debug('{0}: starting'.format(method_name))

		if len(self.error_list) > 0:
			for item in self.error_list:
				try:
					self.db.insert_single_document(
						collection_name=
							self.config['db_config']['collection_remediation'],
						document = item)
					log.debug('{0}:added document: {1}'.format(
						method_name, item))
				except Exception as e:
					log.error('{0}:exception:'.format(method_name))
					log.error('{0}:error: {1}'.format(method_name, str(e)))
	def device_statistics(self):
		# Try to start the ssh session
		method_name = 'device_statistics'
		log.debug('{0}: starting'.format(method_name))
		try:
			time_get_next_device = (self.time_start_ssh_session - 
				self.time_get_next_device)
			time_start_ssh_session = (self.time_loop_through_lib - 
				self.time_start_ssh_session)
			time_loop_through_lib = (self.time_add_remediations - 
				self.time_loop_through_lib)
			time_add_remediations = (self.time_add_inventory - 
				self.time_add_remediations)
			time_add_inventory = (self.time_add_todo_devices - 
				self.time_add_inventory)
			time_add_todo_devices = (self.time_add_self_devices - 
				self.time_add_todo_devices)
			time_add_self_devices = (self.time_end - 
				self.time_add_self_devices)
			time_total = (self.time_end - 
				self.time_get_next_device)
			self.device_stats = {
			"host_ip": self.current_ip,
			"total_execution_time": time_total,
			"get_next_device": time_get_next_device,
			"start_ssh_session": time_start_ssh_session,
			"loop_through_lib": time_loop_through_lib,
			"add_remediations": time_add_remediations,
			"add_inventory": time_add_inventory,
			"add_todo_devices": time_add_todo_devices,
			"time_add_self_devices": time_add_self_devices,
			"errors": self.error_list,
			}
			log.info('{0}:added document: {1}'.format(
				method_name, self.device_stats))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))

	def start_ssh_session(self):
		# Try to start the ssh session
		method_name = 'start_ssh_session'
		log.debug('{0}: starting'.format(method_name))

		try:
			self.ssh_session = helpers.ssh_child.SSHChild(
				host=self.current_ip,
				un=self.config['default_info']['un'],
				pw=self.config['default_info']['pw'],
				port=self.config['default_info']['port'])
			log.debug('{0}:success: {1}'.format(
				method_name, self.ssh_session))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))

# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = Discovery()
    tmprun.main()
