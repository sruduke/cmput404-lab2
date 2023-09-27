import socket
import argparse
from threading import Thread
from variables import *


def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ) # wait for req
            # once we reach an empty byte array, the request is done
            if not data:
                break
            print(data)
            conn.sendall(data)

# single thread start
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ECHO_HOST, ECHO_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen()
        conn, addr = s.accept()
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ECHO_HOST, ECHO_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2) # allows backlog of size 2
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

# Process commandline arguments to start server instances
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="echo_server")
    parser.add_argument("mode", help='the mode to run the server as, one of [single, threaded]')
    args = parser.parse_args()

    try:
        mode = args.mode
        
        if mode == "single":
            start_server()
        elif mode == "threaded":
            start_threaded_server()
        else:
            raise Exception()
    except:
        parser.print_help()


