import argparse
import itertools
import socket


class PasswordHacker:
    DICTIONARY = r"/home/feztix/documents/coding/python/basic_project/passwords.txt"

    def __init__(self):
        # For unpcak using args.Ip/Port/Message
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

        # input_path = args.Path

        # if not os.path.isdir(input_path):
        #     print('The path specified does not exist')
        #     sys.exit()
        #
        # print('\n'.join(os.listdir(input_path)))
        return args

    def establish_connection(self, args):
        with socket.socket() as client_socket:
            hostname = args.Ip
            port = args.Port
            address = (hostname, port)

            client_socket.connect(address)

            # data = args.Message
            # data = data.encode()

            password_generator = self.password_generator()
            self.bruteforce(password_generator, client_socket)

            # client_socket.send(data)
            #
            # response = client_socket.recv(1024)
            # response = response.decode()
            # print(response)

    # Call custom generator
    def bruteforce(self, gen_password, client_socket):
        while True:
            password = next(gen_password)
            client_socket.send(password.encode())
            response = client_socket.recv(1024)
            response = response.decode()
            if response == "Connection success!":
                print(password)
                break

    # Custom generator
    def password_generator(self):
        with open(PasswordHacker.DICTIONARY, 'r') as file:
            for passwd_on_line in file:
                if not passwd_on_line.isdigit():
                    for var in itertools.product(
                            *([letter.lower(), letter.upper()] for letter in passwd_on_line.strip("\n"))):
                        yield "".join(var)

    def init(self):
        pass


if __name__ == "__main__":
    PasswordHacker().init()
