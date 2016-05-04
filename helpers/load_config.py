import sys
import json
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


def load_config(self):
	method_name = 'main'
	log.debug('{0}: load_config'.format(method_name))
	try:
		with open('helpers/config.json') as data_file:
			result = json.load(data_file)
			log.debug('{0}'.format(result))
			return result 
	except Exception as e:
		log.error('{0}:error: loading config {1}'.format(method_name, e))
