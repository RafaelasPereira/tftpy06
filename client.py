"""
TFTPy - This module implements an interactive and command line TFTP 
client.

This client accepts the following options:
    $ python3 client.py [-p serv_port] server
    $ python3 client.py get [-p serv_port] server remote_file [local_file] 
    $ python3 client.py put [-p serv_port] server local_file [remote_file]

(C) Rafaela Pereira, 2023
"""

from docopt import docopt
import cmd
from socket import (
    socket,
    error,
    gaierror,
    gethostbyname,
)
from tftp import put_file, get_file

###############################################################
##
##      ERRORS AND EXCEPTIONS
##
###############################################################

class NetworkError(Exception):
    """
    Any network error, like "host not found", timeouts, etc.
    """
#:

def get_server_ip(hostname: str):
    try:
        IPAddr = gethostbyname(hostname)
        return IPAddr
    except gaierror:
        raise NetworkError(f"Unknown server: {hostname}.")
    except error:
        raise NetworkError(f"Error reaching the server '{hostname}'.")
#:

class Menu(cmd.Cmd):
    def __init__(self, hostname, ip_address, port):
        super().__init__()
        self.hostname = hostname
        self.ip_address = ip_address
        self.port = port
        self.prompt = "tftp client> "
        self.intro = f"Exchanging files with server '{self.hostname}' ({self.ip_address})."

    def do_put(self, args):
        """Put the specified file."""
        
        try:
            put_file((self.ip_address, int(self.port)))
        except Exception as e:
            print(f"An error occurred")

        print("Done!")

    def do_get(self, args):
        """Get the specified file."""
        args_split = args.split()
        try:
            if(len(args_split) >= 2):
                get_file((self.ip_address, int(self.port)), args_split[0], args_split[1])
            else:
                get_file((self.ip_address, int(self.port)), args_split[0], None)
        except Exception as e:
            print(f"An error occurred {e}")

        print("Done!")

    def do_quit(self, arg):
        """Exit the application."""
        print("Exiting TFTP client.")
        print("Goodbye!")
        return True
#:

def main():
    usage = """
    Usage:
        client.py (get|put) [-p] <server> <source_file> [dest_file]
        client.py [-p] <server>
        client.py get [-p] <server> <remote_file> [local_file]
        client.py put [-p] <server> <local_file> [remote_file]

    Options:
        -h --help
        -p --port  Server Port [default:69]
        -q --quit  Quit Client
    """

    arguments = docopt(usage)
    hostname = arguments["<server>"]
    port = arguments["--port"]
    ip_address = get_server_ip(hostname)
    #print(arguments)
    menu = Menu(hostname, ip_address, port)
    menu.cmdloop()
#:

if __name__ == '__main__':
    main()
#: