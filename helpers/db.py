from pymongo import MongoClient
import sys
import load_config
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class DBWrapper(object):
	""" This provides a wrapper around the MongoClient package, and also 
	allows for some default values to be added.

	"""

	def __init__(self):
		pass

	def main(self):
		method_name = 'main'
		log.debug('{0}: starting'.format(method_name))

	def start_conn(self):
		config = load_config.load_config(self)
		# Create the DB object
		self.cfg = {}
		self.cfg['collection_list'] = config['db_config']['collection_list']
		for d in config['db_config']['main']:
			for k,v in d.iteritems():
				self.cfg[k] = v
		for d in config['db_config']['collection_list']:
			for k,v in d.iteritems():
				self.cfg[k] = v
		self.client = MongoClient(self.cfg['adr'], self.cfg['prt'],
			serverSelectionTimeoutMS=self.cfg['msd'])
		db_name = self.cfg['dbn']
		self.db = self.client[db_name]

	def validate_conn(self):
		method_name = 'connect_to_db'
		log.debug('{0}:start:'.format(method_name))
		log.debug('{0}:try:{1} {2} {3}'.format(
			method_name,self.remote_address, self.remote_port, self.db_name))
		#Validate that the connection to the database has been made
		try:
			result = self.client.server_info()
			log.debug('{0}:success: {1} {2} {3}'.format(
				method_name,self.remote_address, 
				self.remote_port, self.db_name))
			log.debug('{0}:result: {1})'.format(method_name, result))
		except Exception as e:
			log.error('{0}:exception: {1} {2} {3}'.format(
				method_name,self.remote_address, 
				self.remote_port, self.db_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def set_unqiue_index(self, field, collection_name):
		method_name = 'set_unqiue_index'
		log.debug('{0}:start:'.format(method_name))
		try:
			print 'field'
			print field
			print collection_name
			result = self.db[collection_name].create_index(field, unique = True)
			log.debug('{0}:success: unique collection: {1}'.format(
				method_name,result))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))	

	def transform_ip_to_dict(self,ip):
		method_name = 'transform_ip_to_dict'
		log.debug('{0}:start:'.format(method_name))
		try:
			result = {"ip_address": ip}
			log.debug('{0}:success: {1}'.format(method_name, result))
			return result
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def build_document_list(self,ip_list):
		method_name = 'build_document_list'
		log.debug('{0}:start:'.format(method_name))
		try:
			document_list = []
			for item in ip_list:
				document = self.transform_ip_to_dict(ip=item)
				document_list.append(document)
			log.debug('{0}:success: {1}'.format(method_name, document_list))
			return document_list
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def add_ip_to_collection(self, ip, collection):
		method_name = 'add_ip_to_collection'
		log.debug('{0}:start:'.format(method_name))
		try:
			document = self.transform_ip_to_dict(ip=ip)
			result = self.db[collection].insert(document)
			print'hi'
			print result
			log.debug('{0}:success: {1}'.format(method_name, result))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))
			print str(e)

	def find_one_and_delete(self, collection):
		method_name = 'find_one_and_delete'
		log.debug('{0}:start:'.format(method_name))	
		try:
			document = self.db[collection].find_one({})
			self.db[collection].remove(document)
			return document
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def find_next_todo(self):
		method_name = 'find_next_todo'
		log.debug('{0}:start:'.format(method_name))	
		try:
			document = self.db[self.cfg['todo']].find_one({})
			self.db[self.cfg['todo']].remove(document)
			return document['ip_address']
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, str(e)))

	def find_all(self, collection):
		method_name = 'find_one_and_delete'
		log.debug('{0}:start:'.format(method_name))	
		try:
			document = self.db[collection].find({})
			return document
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def count_collection(self, collection):
		method_name = 'count_collection'
		log.debug('{0}:start:'.format(method_name))	
		try:
			result = self.db[collection].count()
			if result > 0:
				log.debug('{0}:success: {1}'.format(method_name, result))
				return result
			else:
				log.debug('{0}:success: No More Documents'.format(method_name))
				return False
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def ip_in_collection(self, ip, collection):
		method_name = 'ip_in_collection'
		log.debug('{0}:start:'.format(method_name))
		try:
			if self.db[collection].find(
					{"ip_address": ip}).limit(1).count() > 0:
				log.debug('{0}:success: exists'.format(method_name))
				return True
			else:
				log.debug('{0}:success: does not exist'.format(method_name))
				return False
			return document_list
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def delete_single_collection(self, collection_name):
		method_name = 'delete_single_collection'
		log.debug('{0}:start:'.format(method_name))
		try:
			result = self.db[collection_name].drop()
			log.debug('{0}:success: deleted collection: {1}'.format(
				method_name,result))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def insert_single_document(self, collection_name, document):
		method_name = 'insert_single_document'
		log.debug('{0}:start:'.format(method_name))
		try:
			result = self.db[collection_name].insert(document)
			log.debug('{0}:success: inserted document in collection: {1}'.format(
				method_name,result))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))

	def add_ip_if_not_exist(self, ip, first_collection, second_collection):
		method_name = 'add_ip_if_not_exist'
		log.debug('{0}:start:'.format(method_name))
		try:
			# check to see if the ip exists in the first collection
			if self.ip_in_collection(ip=ip,collection=first_collection):
				log.debug('{0}:success: '\
						'exists first_collection'.format(method_name))
				return
			else:
				# Check to see if the ip exists in the second collection
				if self.ip_in_collection(ip=ip,collection=second_collection):
					log.debug('{0}:success: '\
						'exists second_collection'.format(method_name))
					return
				else:
					# Add to collection
					self.add_ip_to_collection(ip=ip,
						collection=second_collection)
					log.debug('{0}:success: '\
						'added to second_collection'.format(method_name))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))