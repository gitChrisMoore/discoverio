# ssh_helper.py
import paramiko
import time
import socket


class Base(object):

    def __init__(self):
        self.base = None
        self._base_config()

    def _base_config(self):
        self.base = paramiko.SSHClient()
        self.base.set_missing_host_key_policy(paramiko.AutoAddPolicy())


class Transport(object):
    def __init__(self):
        self.ip = None
        self.username = None
        self.password = None
        self.timeout = None
        self.port = None

    def connect(self, base, ip, username, password, timeout=3, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        self.port = port
        try:
            return base.base.connect(hostname=self.ip, username=self.username, password=self.password,
                                     timeout=self.timeout,
                                     port=self.port)
        except socket.timeout:
            pass
            # print 'socket error'
        except socket.error:
            pass
            # print 'socket timeout'
        except AttributeError:
            pass
            # print 'attribute error'


class Command(object):
    def __init__(self, chn, cmd, buf=65536, max_ctr=3):
        self.cmd = cmd
        self.chn = chn
        self.buf = buf
        self.ctr = 0
        self.max_ctr = max_ctr
        self.data = ''
        self.output = ''
        self.output_start = 'a'
        self.loop_control = True

    def main(self):

        time.sleep(.2)
        self._disable_paging()
        time.sleep(.1)
        self._send_cmd()
        time.sleep(.1)

        while self.loop_control:
            self._recv_loop()
            self._recv_loop_increment()
            self._recv_loop_check()
            time.sleep(0.200)
        return self.output

    def _disable_paging(self):
        try:
            self.chn.send("terminal length 0\n")
        except Exception as e:
            print 'error disabling paging' + str(e)

    def _send_cmd(self):
        try:
            self.chn.send(self.cmd)
        except Exception as e:
            print 'error sending command' + str(e)

    def _recv_loop(self):
        if self.chn.recv_ready():
            self.data = self.chn.recv(self.buf)
            self.output += self.data

    def _recv_loop_increment(self):
        if len(self.output) == len(self.output_start):
            self.ctr += 1
        self.output_start = self.output

    def _recv_loop_check(self):
        if self.ctr == self.max_ctr:
            self.loop_control = False


class Session(object):
    """
    ssh = Session(ip, username, password)
    print ssh.cmd('show ip int brief\n')
    """
    def __init__(self, ip, username, password):
        self.base = Base()
        print ip
        Transport().connect(self.base, ip, username, password)
        try:
            self.tst = self.base.base.invoke_shell()
        except AttributeError as e:
            print 'Wrong Attribute: error string: ' + str(e) +  + ip + ' ' + username

    def cmd(self, cmd):
        return Command(self.tst, cmd).main()


