
import sys
import load_config
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

class DeviceList(object):
	""" This imports the known devices from the config.json file

	"""

	def __init__(self):
		config = load_config.load_config(self)

	def main(self):
		method_name = 'main'
		log.debug('{0}: starting'.format(method_name))

	def default_settings(self)


if __name__ == '__main__':
    tmprun = DeviceList()
    tmprun.main()
