from socket import *

NOT_FOUND_MESSAGE = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"

DEFAULT_BUFFER_SIZE = 1024
ADDRESS_FAMILY = AF_INET
SOCKET_TYPE = SOCK_STREAM
ADDRESS = ""
BACKLOG = 1
PORT = 3000

server_socket = socket(ADDRESS_FAMILY, SOCKET_TYPE)

server_socket.bind((ADDRESS, PORT))
server_socket.listen(BACKLOG)

while True:
    print("Ready to serve...")

    connection_socket, address = server_socket.accept()

    message = connection_socket.recv(DEFAULT_BUFFER_SIZE)

    if message is None:
        connection_socket.close()
        continue

    file_path = message.split()[1]

    # print("\n".join(f">> {line}" for line in message.decode().splitlines()) + "\n")

    try:
        file = open(file_path[1:])
        file_content = file.read() + "\r\n"
        file.close()

    except:
        connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connection_socket.send(NOT_FOUND_MESSAGE.encode())

    else:
        connection_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        connection_socket.send(file_content.encode())

    finally:
        connection_socket.close()

server_socket.close()
