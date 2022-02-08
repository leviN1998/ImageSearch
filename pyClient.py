import socket
from ImageCrawling import toolbox

# lokal
# ADDR = ("127.0.0.1", 1234)
# server
ADDR = ("134.2.56.169", 1234)


def send(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Sending " + msg[0:30] + " ...")
    message = msg.encode('utf-8')
    client.send(message)
    response = client.recv(104857600).decode('utf-8')
    images = response.split()
    client.close()
    for i in images:
        toolbox.base64_to_image(i).show()

def disconnect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    message = "Disconnect".encode('utf-8')
    client.send(message)
    print(client.recv(104857600).decode('utf-8'))
    client.close()


image = toolbox.binary_to_image(toolbox.get_test_image()[2])
# image.show()
message = toolbox.image_to_base64(image)
# message += "TESTTESTTEST!!!"
send("Search mobile_net " + message)
disconnect()