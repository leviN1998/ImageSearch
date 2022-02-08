import socket


ADDR = ("127.0.0.1", 1234)


def send(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Sending " + msg)
    message = msg.encode('utf-8')
    client.send(message)
    print(client.recv(104857600).decode('utf-8'))
    client.close()

send("Search")
send("Disconnect")