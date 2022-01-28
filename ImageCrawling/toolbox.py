from base64 import b64encode
import pickle
import os
import requests
import numpy as np
import io
from PIL import Image

def extract_classes():
    '''
    extract classes from txt
    '''
    pass


def unpickle(file: str):
    '''
    '''
    old_wd = os.getcwd()
    os.chdir("ImageDatabases")
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    os.chdir(old_wd)
    return dict


def cifar_convert_image(array):
    img = np.reshape(array, (3, 32, 32))
    img = np.transpose(img, (1,2,0))
    img =  Image.fromarray(img, "RGB")
    return image_to_binary(img)


def image_to_binary(image):
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()


def image_to_base64(image):
    return b64encode(image_to_binary(image)).decode('ascii')


def binary_to_image(binary_image_data):
    return Image.open(io.BytesIO(binary_image_data)).convert("RGB")

def get_test_image():
    from . import database_tools
    conn = database_tools.connect("test.db")
    cur = conn.cursor()
    query_str =  "SELECT i.id, f.feature, i.data "
    query_str += "FROM images AS i, features AS f "
    query_str += "WHERE i.database_name = 'cifar10_test' "
    query_str += "AND i.id = f.id "
    query_str += "AND f.network = 'mobile_net'"
    cur.execute(query_str)
    image = cur.fetchall()[0]
    conn.close()
    return image


def insert_ordered(list, element, count):
    '''
    Insert ordered by distance
    '''
    # print("Before: " + str(len(list)))
    if len(list) < count:
        list.append(element)
        # print("After: " + str(len(list)))
        return
    else:
        for i in range(0, len(list)):
            if list[i][1] > element[1]:
                list.insert(i, element)
                # print("After: " + str(len(list)))
                return

def download_image(url: str):
    '''
    returns binary image
    '''
    binary = requests.get(url).content
    return binary


def download_threaded(urls, start: int, stop: int, list):
    '''
    '''
    for i in range(start, stop):
        list.append(download_image(urls[i]))