import socket
import sys
from variables import *

# AF_INET -> IPv4, SOCK_STREAM -> TCP, SOCK_DGRAM -> UDP
def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host,port))
        s.send(request)
        s.shutdown(socket.SHUT_WR)
        result = s.recv(BYTES_TO_READ)

        while len(result) > 0:
            print(result)
            result = s.recv(BYTES_TO_READ)

# Commandline arguments for running the different clients
if __name__ == "__main__":
    if len(sys.argv) < 2:
        get("www.google.com", 80)
    elif len(sys.argv) == 2 and sys.argv[1] == "echo":
        get(ECHO_HOST, ECHO_PORT)
    else:
        print("Usage: python client.py [echo]")
    
