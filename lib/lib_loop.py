import logging
import time
import mapping
from datetime import timedelta
logging.basicConfig(filename='example.log',level=logging.INFO)




def main(self):
	logging.debug("Starting: lib_loop.main")
	self.log_info = []
	get_list_of_functions(self)
	for module in self.list_of_functions:
		try:
			start_time = time.time()
			module['function_name'].main(self)
		except Exception as e:
			logging.debug("Failed on module: " + module['error_function_name'])
			logging.debug(e)
			add_error_range(self,error_string=str(e))

def get_list_of_functions(self):
	self.list_of_functions = mapping.return_list_of_functions(self)
	return

def add_error_range(self, error_string):
	error_object = {
	"host_ip" : self.current_ip,
	"error" : error_string
	}
	self.error_list.append(error_object)
	return
