import socket

def server_program():
    # set the hostname to localhost
    host = '127.0.0.1'
    port = 3000  # initiate port no above 1024

    print("Host :", host)
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    clients = []
    for i in range(2):
        conn, address = server_socket.accept()  # accept new connection
        print(f"Connection from client{i+1}: " + str(address))
        clients.append((conn, f"client{i+1}"))

    while True:
        for conn, client_name in clients:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                continue
            print(f"from {client_name}: " + str(data))

            # Determine the recipient
            recipient_conn = clients[1][0] if client_name == "client1" else clients[0][0]

            # Send the message to the recipient
            recipient_conn.send(data.encode())

if __name__ == '__main__':
    server_program()
