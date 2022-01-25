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
import numpy as np
import io


def crawl_images():
    ''' TODO: implement
    crawls Images for one Keyword
    '''
    pass


def crawl_images_batch():
    ''' TODO: implement
    crawls images from array of keywords
    '''
    pass


def crawl_from_txt():
    '''
    '''
    pass


def get_feature(feature_func, image):
    '''
    Takes binary Image
    '''
    return feature_func([image])[0]


def calculate_features(database: str, network: str, feature_func, hashing_func, count:int=0):
    '''
    TODO calculate Features and Hashes for all Networks and Search algorithms
    '''
    conn = database_tools.connect(database)
    database_tools.calculate_features(conn, network, feature_func, hashing_func, count)
    database_tools._print_db_info(conn)
    conn.close()


def print_db_info(database: str):
    '''
    '''
    database_tools.print_db_info(database)


def get_image(database: str, id: int):
    '''
    Get Image from id
    '''
    conn = database_tools.connect(database)
    result = database_tools._get_image(conn, id)
    conn.close()
    return result[4]


def get_nearest_images(database: str, image, img_database_name: str, network: str, feature_func, count: int=10):
    '''
    Returns [(Image, Distance),()]
    image must be binary
    TODO comparison implementieren
    '''
    conn = database_tools.connect(database)
    features = database_tools.get_features_for_comparison(conn, img_database_name, network)
    closest_images = []
    image_feature = np.load(io.BytesIO(get_feature(feature_func, image)))
    features = features[0:30]
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
        output.append((toolbox.binary_to_image(img), i[1]))
    conn.close()
    return output