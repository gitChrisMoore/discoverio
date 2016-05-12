
import sys
import helpers.ssh_child
import helpers.db2
import helpers.cmn_tool
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

class DiscoveryInit(object):
	""" This provides a wrapper around the MongoClient package, and also 
	allows for some default values to be added.
	"""

	def __init__(self):
		self.cfg = helpers.cmn_tool.Config._load_config()
		# Create the DB object
		self.db = helpers.db2.DB()

	def main(self):
		method_name = 'main'
		log.debug('{0}: starting'.format(method_name))
		self._remove_all_collections()
		self._set_unique_fields()
		self._seed_collecctions()

	def _remove_all_collections(self):
		for d in self.cfg['db_config']['collection_list']:
			for k,v in d.iteritems():
				result = self.db._init_remove_collection(col=v)
				log.info(result)

	def _set_unique_fields(self):
		result = self.db._init_unique_index(col=self.cfg['todo'], prop='ip_address')
		log.info(result)
		result = self.db._init_unique_index(col=self.cfg['complete'], prop='ip_address')
		log.info(result)
		result = self.db._init_unique_index(col=self.cfg['cdp'], prop='ip_address')
		log.info(result)

	def _seed_collecctions(self):
		log.info('Seeding Documents in Todo')
		for i in self.cfg['db_config']['seed_ips']:
			document = helpers.cmn_tool.Doc._build_todo_obj(i)
			result = self.db._todo_insert_todo(document)
			log.info(result)
		log.info('The next 3 documents should fail, testing the unique fileds')
		for i in self.cfg['db_config']['seed_ips']:
			document = helpers.cmn_tool.Doc._build_todo_obj(i)
			result = self.db._todo_insert_todo(document)
			log.info(result)

# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = DiscoveryInit()
    tmprun.main()
