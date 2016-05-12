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
		self.client = MongoClient(self.cfg['adr'], self.cfg['prt'],
			serverSelectionTimeoutMS=self.cfg['msd'])
		self._start_client()

	def _start_client(self):
		try:
			self.db = self.client[self.cfg['dbn']]
		except Exception as e:
			return str(e)
		
	""" Inital operations to run on the database
	"""

	def _init_unique_todo(self):
		return self.db[self.cfg['todo']].create_index(
			"ip_address", unique = True)

	def _init_unique_complete(self):
		return self.db[self.cfg['complete']].create_index(
			"ip_address", unique = True)

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

    tst_document_list = [{"ip_address": "1.3.4.1"},{"ip_address": "1.3.3.1"},{"ip_address": "3.4.3.1"}]

    for document in tst_document_list:
    	print test._todo_insert_complete(document)

    print test.todo_count()

    while test.todo_count() > 0:
    	new_device = test.todo_get_doc()
    	print next_ip



