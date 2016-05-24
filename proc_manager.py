from subprocess import Popen
from sys import stdout, stdin, stderr
import time, os, signal



class Command(object):
    help = 'Run all commands'
    commands = [
        'python discoverio/discoverio.py',
        'python discoverio/discoverio.py',
        'python discoverio/discoverio.py', 'python discoverio/discoverio.py',
        "python discoverio/discoverio.py", 'python discoverio/discoverio.py',
        'python discoverio/discoverio.py', 'python discoverio/discoverio.py',
        'python discoverio/discoverio.py', 'python discoverio/discoverio.py',
        'python discoverio/discoverio.py', 'python discoverio/discoverio.py',
        'python discoverio/discoverio.py', 'python discoverio/discoverio.py',
        "python discoverio/discoverio.py", 'python discoverio/discoverio.py',
        'python discoverio/discoverio.py'
    ]

    def main(self, *args, **options):
        proc_list = []

        for command in self.commands:
            print "$ " + command
            proc = Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
            proc_list.append(proc)
            time.sleep(15)

        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            for proc in proc_list:
                os.kill(proc.pid, signal.SIGKILL)
if __name__ == "__main__":
    client = Command()
    client.main()