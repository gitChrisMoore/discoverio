import ssh_parent
import sys
import logging
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class SSHChild(ssh_parent.SSHWrapper):
	""" The object of this class is to provide a wrapper around the paramiko
		package.  There are two main pieces two the package, the transport
		and the channel.  Once the channel is created, if it is a cisco device
		it will disable the paging from interfering with the output
	"""

	def child_execute(self, command):
		self.command_result = self.main(command=command)
		return self.command_result
