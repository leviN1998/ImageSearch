# -*- coding: utf-8 -*-

import socket
import ImageCrawling
from ImageCrawling import feature_interface
from PIL import Image
#import threading
from ImageCrawling import toolbox
from ImageCrawling import extractors
import time

# Auf dem Server
host, port = "134.2.56.169", 1234
# lokal
# host, port = "127.0.0.1", 1234
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def recv(): 
    try:
        client.bind((host, port))
    finally:
        pass
    client.listen(10) # how many connections can it receive at one time
    print("Start Listening...")
    
    while True:
        conn, addr = client.accept()
        print("client with address: ", addr, " is connected.")
        data = conn.recv(104857600) # 100 MB
        data = data.decode("utf-8")
        print("Recieved this data: <", data[0:30], "> from the client.")

        data_recieved = data.split()
        mode = data_recieved[0]
        

        if mode == "Search":
            network = data_recieved[1]
            message_count = int(data_recieved[2])
            print("recieving " + str(message_count) + " messages")
            query_image = ""
            # conn.send("Ok".encode("utf-8"))

            # for i in range(0, message_count):
            #     data = conn.recv(104857600)
            #     query_image += data.decode('utf-8')
            #     # conn.send("Ok".encode("utf-8"))
            #     print("Got message[" + str(i) + "]: " + data.decode('utf-8'))
            i = 0
            while True:
                data = conn.recv(104857600)
                if data.decode('utf-8') == "END":
                    print("End")
                    break
                query_image += data.decode('utf-8')
                print("Got message[" + str(i) + "]: " + data.decode('utf-8') + "|")
                i += 1

            # print(query_image)
            # print(network)
            # print()
            # print("-----------------------------")
            # print(query_image)
            # print()
            # print("-----------------------------")

            response = "Accepted"
            query_image = toolbox.base64_to_image(query_image)
            # query_image.show()
            
            mobilenet_extractor = extractors.MobileNet()
            feature = mobilenet_extractor.extractImage(query_image)

            # # at the moment network needs to be "mobile_net"
            images = ImageCrawling.get_nearest_images_2("final.db", query_image, "big", network, feature, count=10)
            # zum lokal testen
            # images = ImageCrawling.get_nearest_images_2("test.db", query_image, "big", network, feature, count=10)

            response = ""
            for i in images:
                response += i[0]
                response += " "

            
            count = 0
            current = ""
            messages = []
            for c in response:
                if count == 1000:
                    messages.append(current)
                    current = ""
                    count = 0
                current += c
                count += 1

            messages.append(current)

            # Sending Search mobilenet message_count
            initial_msg = str(len(messages))
            print(initial_msg)
            # message = initial_msg.encode('utf-8')
            # conn.send(message)
            # conn.recv(104857600)

            for m in messages:
                conn.send(m.encode('utf-8'))
                # conn.recv(104857600)
                time.sleep(0.02)


            conn.close()
            print("-----------------------------")

        elif mode == "Disconnect":
            reply = "Disconnected and the listen has Stopped"
            conn.send(reply.encode("utf-8"))
            conn.close()
            break
            # Testimplementation

        else:
            reply = "Failed"
            conn.send(reply.encode("utf-8"))
            conn.close()
            print("-----------------------------")

            
    client.close()
"""
You can use thread for the recieve operation so that the execution in main thread
isn't wait until complete the recieve operation. 
"""
#thread = threading.Thread(target = recvFromAndroid, args = ())
#thread.start()
recv()
#print "completed"

