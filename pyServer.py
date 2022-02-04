# -*- coding: utf-8 -*-

import socket
import ImageCrawling
from ImageCrawling import feature_interface
from PIL import Image
#import threading
from ImageCrawling import toolbox
from ImageCrawling import extractors


host, port = "134.2.56.169", 1234
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
        data = conn.recv(8256)
        data = data.decode("utf-8")
        print("Recieved this data: <", data, "> from the client.")

        data_recieved = data.split()
        mode = data_recieved[0]
        

        if mode == "Search":
            network = data_recieved[1]
            query_image = data_recieved[2]
            print(query_image)
            query_image = toolbox.base64_to_image(query_image)
            
            mobilenet_extractor = extractors.MobileNet()
            feature = mobilenet_extractor.extractImage(query_image)

            # at the moment network needs to be "mobile_net"
            images = ImageCrawling.get_nearest_images_2("final.db", query_image, "big", network, feature, count=10)

            response = ""
            for i in images:
                response += i[0]
                response += " "

            conn.send(response.encode("utf-8"))
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

