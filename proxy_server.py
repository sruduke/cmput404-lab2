import socket
import argparse
from threading import Thread
from variables import *

def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.send(request)
        client_socket.shutdown(socket.SHUT_WR)

        # gather response
        data = client_socket.recv(BYTES_TO_READ) # block until data comes
        result = b'' + data
        while len(data) > 0:
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        return result

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
        response = send_request("www.google.com", 80, request)
        # send the response back to the client
        conn.sendall(response)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)
        conn, addr = server_socket.accept()

        # handle single client then close
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)

        # handle multiple clients
        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn,addr))
            thread.run()

# Process commandline arguments to start server instances
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="proxy_server")
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
