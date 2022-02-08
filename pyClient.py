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

    count = 0
    current = ""
    messages = []
    for c in msg:
        if count == 200:
            messages.append(current)
            current = ""
            count = 0
        current += c
        count += 1

    messages.append(current)

    # Sending Search mobilenet message_count
    initial_msg = "Search mobile_net " + str(len(messages))
    print(initial_msg)
    message = initial_msg.encode('utf-8')
    client.send(message)
    client.recv(104857600)

    for m in messages:
        client.send(m.encode('utf-8'))
        client.recv(104857600)


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
print()
print("-----------------------------")
# print(message)
print()
print("-----------------------------")
# message += "TESTTESTTEST!!!"
send(message)
disconnect()