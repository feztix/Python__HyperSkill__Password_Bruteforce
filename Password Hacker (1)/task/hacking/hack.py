import argparse
import itertools
import socket
import json


class PasswordHacker:
    DICTIONARY = r"/home/feztix/documents/coding/python/basic_project/passwords.txt"
    _DICTIONARY = r"/home/feztix/documents/coding/python/Password_Hacker/Password Hacker (1)/task/hacking/logins.txt"

    def __init__(self):
        # For unpack using args.Ip/Port/Message
        args = self.init_cli()
        self.establish_connection(args)

    def init_cli(self):
        # Create the parser
        my_parser = argparse.ArgumentParser(description='Establishing a connection')

        # Add the arguments
        # my_parser.add_argument('Path', metavar='path', type=str,
        #                        help='the path to .py file')
        my_parser.add_argument("Ip", metavar='ip', choices=["localhost", "127.0.0.1"],
                               help="You need to choose only one IP address form the list.")
        my_parser.add_argument("Port", metavar="port", type=int,
                               help="You need to input port")
        # my_parser.add_argument("Message", metavar="message", type=str,
        #                        help="You need to input message for sending")

        # Execute the parse_args() method
        args = my_parser.parse_args()
        return args

    def establish_connection(self, args):
        with socket.socket() as client_socket:
            hostname = args.Ip
            port = args.Port
            address = (hostname, port)

            client_socket.connect(address)

            password_generator = self.password_generator()
            login_generator = self.login_generator()
            self.bruteforce(password_generator, login_generator, client_socket)
            
    # Send custom credentials
    def send_credentials(self, login, password, client_socket):
        # client_socket.send(password.encode())
        # response = client_socket.recv(1024)
        # response = response.decode()
        # if response == "Connection success!":
        #     print(password)
        #     return False

        data = json.dumps({"login": login, "password": password})
        client_socket.send(data.encode())
        response = client_socket.recv(1024)
        response = json.loads(response.decode()).get("result")
        return data, response

    # Call custom generator
    def bruteforce(self, gen_password, gen_login, client_socket):
        while True:
            # password = next(gen_password)
            password = ""
            login = next(gen_login)
            self.send_credentials(password, login, client_socket)

            data, resp = self.send_credentials(login, password, client_socket)
            print(data, resp)
            if resp != "Wrong login!":
                break

    # Custom generator
    def password_generator(self):
        with open(PasswordHacker.DICTIONARY, 'r') as file:
            for passwd_on_line in file:
                if not passwd_on_line.isdigit():
                    for var in itertools.product(
                            *([letter.lower(), letter.upper()] for letter in passwd_on_line.strip("\n"))):
                        yield "".join(var)

    def login_generator(self):
        with open(PasswordHacker._DICTIONARY, 'r') as file:
            for login_on_line in file:
                # if not login_on_line.isdigit():
                    # for var in itertools.product(
                            # *([letter.lower(), letter.upper()] for letter in login_on_line.strip("\n"))):
                        # yield "".join(var)
                yield "".join(login_on_line.strip("\n"))

    def init(self):
        pass


if __name__ == "__main__":
    PasswordHacker().init()



# # Custom generator
#     def password_generator(self, max_length=10):
#         # Set Complexity
#         lowercase = list(string.ascii_lowercase)
#         digits = list(string.digits)
#
#         for i in range(1, max_length):
#             complexity = itertools.chain(lowercase, digits)
#             for passwd in itertools.product(complexity, repeat=i):
#                 yield "".join(passwd)