from base64 import b64decode, b64encode
import pickle
import os
import requests
import numpy as np
import io
from PIL import Image
from . import database_tools
import time

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


def base64_to_image(image):
    return binary_to_image(b64decode(image))


def binary_to_image(binary_image_data):
    return Image.open(io.BytesIO(binary_image_data)).convert("RGB")

def get_test_image():
    from . import database_tools
    conn = database_tools.connect("test.db")
    cur = conn.cursor()
    query_str =  "SELECT i.id, f.feature, i.data "
    query_str += "FROM images AS i, features AS f "
    query_str += "WHERE i.database_name = 'big' "
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

def cut_image(image):
    '''
    ''' # 300 x 216   25:18
        # 390 x 280   39:28
    width, height = image.size
    left = 0
    top = 0
    right = width
    bottom = height - 20
    return image.crop((left, top, right, bottom))


def extract_keywords(file: str):
    '''
    '''
    with open(file) as f:
        lines = f.readlines()

    keywords = []
    for l in lines:
        keywords.append(l.rstrip("\n"))
        
    return keywords


def write_keywords(file: str, keywords):
    '''
    '''
    with open(file, 'w') as f:
        f.writelines(keywords)


def combine_keyword_files(file1: str, file2: str):
    '''
    '''
    old = extract_keywords(file1)
    to_add = extract_keywords(file2)
    for k in to_add:
        found = False
        for existing_k in old:
            if k == existing_k:
                found = True
        if not found:
            old.append(k)
    # delete both txts
    os.remove(file1)
    os.remove(file2)
    write_keywords(file1, old)


def consume_queue(queue, database: str, running: bool):
    '''
    '''
    conn = database_tools.connect(database)
    while running() or not queue.empty():
        if queue.empty():
            time.sleep(10)
            # print("running: " + str(running()))
            # print("not empty: " + str(not queue.empty()))
            continue
        data = queue.get()
        database_tools.add_images(conn, data[0], data[1], data[2], data[3])
        print("[Info]      added " + data[1] + " to database")
