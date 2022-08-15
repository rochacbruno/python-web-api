import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9000))
server.listen()

try:
    while True:
        client, address = server.accept()
        data = client.recv(5000).decode()
        print(data)

        client.sendall(
            "HTTP/1.0 200 OK\r\n\r\n<html><body>Hello World</body></html>\r\n\r\n".encode()
        )
        client.shutdown(socket.SHUT_WR)
except:
    server.close()