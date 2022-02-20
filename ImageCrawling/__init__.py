""" Module for crawling images from different Websites using
	a set of Keywords
	At the Moment only Google with BeautifulSoup is supported,
	which leads to ~80 Images per Keyword

Imports:
--------
    crawl_soup file with the BeautifulSoup-Image Crawler. Implements _get_image_urls to get urls of the images from google
    crawling_base provides functions for creating folders and saving images locally
    os is needed to get the current working directory's path

Functions:
----------
download_images(query, image_count, folder, verbose): str, int, str, bool -> None
	downloads images to a Keyword (query) into a specific folder (folder)
	path is relative to working directory

download_images_batch(): -> None
	optimized version of download_images to support using more than one Keyword

TODOS:
------
    TODO: implemet download_images_batch()
    TODO: add support for Selenium
    TODO: add Crawler for Google with Selenium
    TODO: add Crawler for Flickr with Selenium
    TODO: change Filestructure of Image-Databases
    TODO: add functionality to save images into Database (binary vs. path ??)
    TODO: add support for Feature Extraction
    TODO: add functionality of using 5 example images to measure how good results are

INFORMATION:
------------
	Every scraper needs to have a function get_image_urls(query, image_count, verbose)
	That collects all image urls on that website

"""
from .database_tools import *
from .toolbox import *
from .hashing_interface import *
from .crawl_shutterstock import *
from .extractors import *
import numpy as np
import io
import random
from queue import Queue


mobileNet = "mobile_net"
mobileV2 = "mobile_netV2"
nas = "nas"
vgg = "vgg16"
xcep = "xcep"


def crawl_images(query: str, image_database_name: str, image_count: int, test_size: int, queue, thread_count: int=5):
    ''' TODO: implement
    crawls Images for one Keyword
    '''
    # print("[Info]      crawling " + query)
    links = crawl_shutterstock.crawl_links(query, image_count, thread_count)
    if len(links) == 0:
        print("[ERROR]     no images extracted")
        print("[FAILED]    stopped crawling for Keyword: " + query)
        return

    images = []
    threads = list()
    images_per_thread = math.ceil(image_count / thread_count)
    for i in range(0, thread_count):
        t = threading.Thread(target=toolbox.download_threaded, args=(links, i * images_per_thread, min(image_count, (i+1) * images_per_thread), images, ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Cut images
    cropped_images = []
    for i in images:
        # toolbox.binary_to_image(i).show()
        cropped_images.append(toolbox.image_to_binary(toolbox.cut_image(toolbox.binary_to_image(i))))

    # for i in cropped_images:
    #     toolbox.binary_to_image(i).show()

    # extract validation set
    validation = []
    while len(validation) < test_size:
        random_int = random.randint(0, len(cropped_images)-1)
        validation.append(cropped_images[random_int])
        cropped_images.pop(random_int)

    queue.put(((cropped_images, query, image_database_name, "shutterstock.com")))
    queue.put((validation, query, image_database_name + "_test", "shutterstock"))
    print("[Info]      finished crawling " + query)


def crawl_images_batch(keywords, database: str, image_database_name: str, image_count: int, test_size: int, main_threads: int=10, child_threads: int=1):
    ''' TODO: implement
    crawls images from array of keywords
    '''
    print("[Info]      Starting to crawl " + str(len(keywords)) + " Keywords")
    batch_size = math.ceil(len(keywords) / main_threads)
    batches = [keywords[i:i + batch_size] for i in range(0, len(keywords), batch_size)]
    print("[Info]      Using " + str(len(batches)) + " Threads with max " + str(batch_size) + " Keywords")
    
    threads = list()
    queue = Queue()
    running = True
    thread_queue = threading.Thread(target=toolbox.consume_queue, args=(queue, database, lambda: running))
    thread_queue.start()
    for i in range(0, len(batches)):
        t = threading.Thread(target=__crawl_images_batch, args=(batches[i], image_database_name, image_count, test_size, queue, child_threads, ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    running = False
    thread_queue.join()
    print_db_info(database)


def __crawl_images_batch(keywords, database: str, image_database_name: str, image_count: int, test_size: int, child_threads: int=1):
    for k in keywords:
        crawl_images(k, database, image_database_name, image_count, test_size, child_threads)


def crawl_from_txt(file: str, database: str, image_database_name: str, image_count: int, test_size: int, main_threads: int=10, child_threads: int=1):
    '''
    '''
    keywords = toolbox.extract_keywords(file)
    keywords_length = len(keywords)
    existing_keywords = database_tools.get_all_keywords(database)
    existing_length = len(existing_keywords)
    for k in existing_keywords:
        i = 0
        while i < len(keywords):
            if keywords[i] == k:
                del keywords[i]
            i += 1
    
    print("Keywords to crawl: " + str(keywords_length) + " existing Keywords: " + str(existing_length) + " crawling without duplicates: " + str(len(keywords)))
    crawl_images_batch(keywords, database, image_database_name, image_count, test_size, main_threads, child_threads)


def get_feature(feature_func, image):
    '''
    Takes binary Image
    '''
    return feature_func([image])[0]


def calculate_features(database: str, network: str, extractor, hashing_func, count:int=0):
    '''
    TODO calculate Features and Hashes for all Networks and Search algorithms
    '''
    conn = database_tools.connect(database)
    database_tools.calculate_features(conn, network, extractor, hashing_func, count)
    database_tools._print_db_info(conn)
    conn.close()


def calculate_all_features(database: str, count: int=0):
    mobile_extractor = extractors.MobileNet()
    mobile_v2_extractor = extractors.MobileNetV2()
    vgg_extractor = extractors.VGG16Extractor()
    xception_extractor = extractors.Xception()
    nasnet_extractor = extractors.NasNet()

    calculate_features(database, mobileNet, mobile_extractor, calculate_hashes, count)
    calculate_features(database, mobileV2, mobile_v2_extractor, calculate_hashes, count)
    calculate_features(database, vgg, vgg_extractor, calculate_hashes, count)
    calculate_features(database, xcep, xception_extractor, calculate_hashes, count)
    calculate_features(database, nas, nasnet_extractor, calculate_hashes, count)


def print_db_info(database: str):
    '''
    '''
    database_tools.print_db_info(database)


def get_keywords(database: str):
    '''
    '''
    return database_tools.get_all_keywords(database)


def get_image(database: str, id: int):
    '''
    Get Image from id
    '''
    conn = database_tools.connect(database)
    result = database_tools._get_image(conn, id)
    conn.close()
    return result[4]


def get_images(database: str, keyword: str):
    '''
    '''
    conn = database_tools.connect(database)
    result = database_tools.get_images(conn, keyword)
    conn.close()
    return result


def get_nearest_images(database: str, image, img_database_name: str, network: str, image_feature, count: int=10):
    '''
    Returns [(Image, Distance),()]
    image must be binary
    TODO comparison implementieren
    '''
    conn = database_tools.connect(database)
    features = database_tools.get_features_for_comparison(conn, img_database_name, network)
    closest_images = []
    #image_feature = np.load(io.BytesIO(get_feature(feature_func, image)))
    # features = features[0:30]
    # print(len(features))
    for f in features:
        feature = np.load(io.BytesIO(f[1]))
        distance = hashing_interface.dummy_calc_distance(feature, image_feature)
        if len(closest_images) < count:
            toolbox.insert_ordered(closest_images, (f[0], distance), count)
            # print(len(closest_images))
        elif distance < closest_images[-1][1]:
            toolbox.insert_ordered(closest_images, (f[0], distance), count)
            closest_images.pop()

    output = []
    # print(closest_images)
    for i in closest_images:
        img = database_tools._get_image(conn, i[0])[4]
        output.append((toolbox.image_to_base64(toolbox.binary_to_image(img)), i[1]))
    conn.close()
    return output


def get_nearest_images_2(database: str, image, img_database_name: str, network: str, image_feature, count: int=10, percentage: int=100):
    '''
    '''
    conn = database_tools.connect(database)
    buf = io.BytesIO()
    np.save(buf, image_feature)
    binary_feature =  buf.getvalue()
    hash = hashing_interface.calculate_hashes(network, [binary_feature])[0]
    features = database_tools.get_images_from_hash(conn, network, img_database_name, hash)

    print("found " + str(len(features)) + " features")
    used_length = math.ceil(len(features) * (percentage / 100.0))
    print("using " + str(used_length) + " features (" + str(percentage) + "%)")

    closest_images = []
    #image_feature = np.load(io.BytesIO(get_feature(feature_func, image)))
    # features = features[0:30]
    # print(len(features))
    for f in features:
        feature = np.load(io.BytesIO(f[1]))
        # print(feature)
        # print(image_feature)
        distance = hashing_interface.dummy_calc_distance(feature, image_feature)
        if len(closest_images) < count:
            toolbox.insert_ordered(closest_images, (f[0], distance), count)
            # print(len(closest_images))
        elif distance < closest_images[-1][1]:
            toolbox.insert_ordered(closest_images, (f[0], distance), count)
            closest_images.pop()

    output = []
    # print(closest_images)
    for i in closest_images:
        img = database_tools._get_image(conn, i[0])[4]
        output.append((toolbox.image_to_base64(toolbox.binary_to_image(img)), i[1]))
        # output.append((toolbox.binary_to_image(img), i[1]))
    conn.close()
    return output


def search_for_classes(database: str, img_database_name: str, network: str, image_feature, count: int=10):
    '''
    '''
    conn = database_tools.connect(database)
    binary_feature =  image_feature
    image_feature = np.load(io.BytesIO(binary_feature))
    hash = hashing_interface.calculate_hashes(network, [binary_feature])[0]
    features = database_tools.get_classes_from_hash(conn, network, img_database_name, hash)

    # print("found " + str(len(features)) + " features")

    closest_images = []
    #image_feature = np.load(io.BytesIO(get_feature(feature_func, image)))
    # features = features[0:30]
    # print(len(features))
    for f in features:
        feature = np.load(io.BytesIO(f[1]))
        # print(feature)
        # print(image_feature)
        distance = hashing_interface.dummy_calc_distance(feature, image_feature)
        if len(closest_images) < count:
            toolbox.insert_ordered(closest_images, (f[0], distance), count)
            # print(len(closest_images))
        elif distance < closest_images[-1][1]:
            toolbox.insert_ordered(closest_images, (f[0], distance), count)
            closest_images.pop()

    output = []
    # print(closest_images)
    for i in closest_images:
        output.append(i[0])

    conn.close()
    return output


def calculate_image_score(database: str, img_database_name: str, network: str, image_feature, image_class: str):
    '''
    '''
    classes = search_for_classes(database, img_database_name, network, image_feature, count=15)
    # print(classes)
    top_1 = 0
    top_5 = 0
    top_15 = 0.0
    if classes[0] == image_class:
        top_1 = 1

    for i in range(0, 5):
        if classes[i] == image_class:
            top_5 = 1

    for c in classes:
        if c == image_class:
            top_15 += 1

    top_15 /= 15
    return top_1, top_5, top_15


def calculate_class_score(database: str, img_database_name: str, network: str, image_class: str):
    '''
    '''
    test_images = database_tools.get_test_images_for_class(database, network, img_database_name, image_class)
    test_images = test_images[0:2]
    top_1 = 0.0
    top_5 = 0.0
    top_15 = 0.0
    for image in test_images:
        t1, t5, t15 = calculate_image_score(database, img_database_name, network, image, image_class)
        top_1 += t1
        top_5 += t5
        top_15 += t15

    top_1 /= len(test_images)
    top_5 /= len(test_images)
    top_15 /= len(test_images)
    return top_1, top_5, top_15


def calculate_network_score(database: str, img_database_name: str, network: str):
    '''
    '''
    keywords = get_keywords(database)

    with open("metric_detailed.txt") as f:
        lines = f.readlines()

    with open("metric.txt") as f:
        lines_simple = f.readlines()

    top_1 = 0.0
    top_5 = 0.0
    top_15 = 0.0
    for k in keywords:
        t1, t5, t15 = calculate_class_score(database, img_database_name, network, k)
        top_1 += t1
        top_5 += t5
        top_15 += t15
        lines.append("["  + network + "] (" + k + ") Top 1: " + str(t1) + "  Top 5: " + str(t5) + "  Top 15: " + str(t15) + "\n")

    top_1 /= len(keywords)
    top_5 /= len(keywords)
    top_15 /= len(keywords)
    lines.append("\n")
    lines.append("---------------------------------------------------------------------------------------------------------------------------------\n")
    lines.append("["  + network + "] Top 1: " + str(top_1) + "  Top 5: " + str(top_5) + "  Top 15: " + str(top_15) + "\n")
    lines.append("---------------------------------------------------------------------------------------------------------------------------------\n")
    lines.append("\n")
    lines_simple.append("["  + network + "] Top 1: " + str(top_1) + "  Top 5: " + str(top_5) + "  Top 15: " + str(top_15) + "\n")
    os.remove("metric_detailed.txt")
    os.remove("metric.txt")
    with open("metric_detailed.txt", 'w') as f:
        f.writelines(lines)
    with open("metric.txt", 'w') as f:
        f.writelines(lines_simple)
    return top_1, top_5, top_15


def calculate_metric(database: str, img_database_name: str):
    '''
    '''
    with open("metric.txt", 'w') as f:
        f.write("Metric:\n")
    with open("metric_detailed.txt", 'w') as f:
        f.write("Metric:\n")

    calculate_network_score(database, img_database_name, mobileNet)
    calculate_network_score(database, img_database_name, mobileV2)
    calculate_network_score(database, img_database_name, nas)
    calculate_network_score(database, img_database_name, vgg)
    calculate_network_score(database, img_database_name, xcep)