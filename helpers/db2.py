from pymongo import MongoClient
import sys
import cmn_tool

class DB(object):
	""" This provides a wrapper around the MongoClient package, and also 
		allows for some default values to be added.
		.db = self.client[db_name]
	"""
	def __init__(self):
		self.cfg = cmn_tool.Config._load_config()
		self.client = MongoClient(self.cfg['db_config']['ip'], self.cfg['db_config']['port'],
			serverSelectionTimeoutMS=self.cfg['db_config']['msd'])
		self._start_client()

	def _start_client(self):
		try:
			self.db = self.client[self.cfg['db_config']['name']]
		except Exception as e:
			return str(e)
		
	""" Inital operations to run on the database
	"""

	def _init_unique_index(self, col, prop):
		return self.db[col].create_index(prop,unique=True)

	def _init_remove_collection(self, col):
		return self.db[col].drop()

	def find_all(self, col):
		return self.db[col].find()

	def count(self, col):
		return self.db[col].count()

	def upsert_arp(self, col, doc):
		try:
			self.db[col].update_one({'ip_address':doc['ip_address']},
			 {'$set':{'mac_address':doc['mac_address']}}, upsert=True)
		except Exception as e:
			print str(e)

	def upsert_cdp(self, col, doc):
		try:
			data = {'neighbor_platform':doc['neighbor_platform'],
			 'neighbor_capabilities':doc['neighbor_capabilities'],
			 'neighbor_local_port':doc['neighbor_local_port'],
			 'neighbor_remote_port':doc['neighbor_remote_port']}
			self.db[col].update_one({'ip_address':doc['ip_address']},
			 {'$set': data}, upsert=True)
		except Exception as e:
			print str(e)

	def add_document(self, col, doc):
		try:
			return self.db[col].insert(doc)
		except Exception as e:
			return str(e)

	""" Below are the methods which were developed to compare the 'todo'
		collection to the 'complete collection'
	"""

	def _todo_single_find(self):
		docs = self.db[self.cfg['todo']].find({},{'_id':False}).limit(1)
		return docs[0]

	def _todo_single_remove(self, document):
		return self.db[self.cfg['todo']].remove(document)

	def _todo_search_complete(self,document):
		return self.db[self.cfg['complete']].find(
			{"ip_address": document['ip_address']}).count()



	def _todo_insert_complete(self, document):
		try:
			return self.db[self.cfg['complete']].insert(
				{"ip_address": document['ip_address']})	
		except Exception as e:
			return str(e)
			
	def _todo_insert_todo(self, document):
		try:
			return self.db[self.cfg['todo']].insert(
				{"ip_address": document['ip_address']})
		except Exception as e:
			return str(e)

	""" Methods which are called outside of the class
	"""

	def todo_count(self):
		return self.db[self.cfg['todo']].count()

	def todo_get_doc(self):
		self.unique_todo = False
		while self.unique_todo is False:
			next_doc = self._todo_single_find()
			self._todo_single_remove(next_doc)
			if self._todo_search_complete(next_doc) > 0:
				self.unique_todo = False
			else:
				self.unique_todo = True
		return next_doc

if __name__ == '__main__':
    """ IP Address Validation
    """
    test = DB()



