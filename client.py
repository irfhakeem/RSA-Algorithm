import socket
from des import encryption_dynamic, decryption_dynamic


def client_program():
    host = '127.0.0.1'  # as both code is running on same pc
    port = 3000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(encryption_dynamic(message))  # send message
        data = client_socket.recv(1024)
        data = decryption_dynamic(data)

        print('Received from server: ' + data)

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
